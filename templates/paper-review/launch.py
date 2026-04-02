#!/usr/bin/env python3
"""Paper review orchestrator.

Launches LLM review tracks in parallel with timeout, validation, and retry.
Replaces bash-based launchers which break on wait/PID tracking.

Usage:
    python launch.py --parallel 2 --layer exec
    python launch.py --parallel 2 --layer method --reasoning high
    python launch.py --tracks E1,A1,M1 --force
    python launch.py --parallel 3  # all tracks
    python launch.py --reasoning low --layer exec  # fast mechanical checks

Reasoning levels (GPT-5.4):
    minimal  — fastest, cheapest, for trivial checks
    low      — mechanical tasks (number cross-check, re-verify scripts)
    medium   — moderate complexity (leakage audit, statistical claims)
    high     — judgment tasks (adversarial, metric validity, SI review)

Configuration:
    Set REPO_DIR, PROMPTS_DIR, REVIEWS_DIR below, or override via CLI.
"""

import argparse
import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

# ── CONFIGURE THESE ──

REPO_DIR = Path(__file__).resolve().parent.parent  # adjust
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
REVIEWS_DIR = Path(__file__).resolve().parent / "reviews"
STATUS_LOG = REVIEWS_DIR / "status.log"

# Default reasoning level per layer (override with --reasoning)
LAYER_REASONING = {
    "exec": "low",
    "method": "medium",
    "adversarial": "high",
    "special": "medium",
    "consistency": "low",
    "data": "medium",
}

# Track definitions by layer
LAYERS = {
    "exec": ["E1", "E2", "E3", "E4"],
    "method": ["M1", "M2", "M3"],
    "adversarial": ["A1", "A2", "A3"],
    "special": ["naive_reader", "citation_verify"],
}

# Per-track reasoning overrides (optional)
TRACK_REASONING = {
    # "A1": "high",
    # "E1": "low",
}

# Known issues preamble (injected into M/A tracks)
KNOWN_ISSUES_FILE = None  # Set to Path("DECISIONS.md") if available


# ── Helpers ──

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"{ts} {msg}"
    print(line)
    STATUS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(STATUS_LOG, "a") as f:
        f.write(line + "\n")


def validate_output(path):
    if not path.exists() or path.stat().st_size == 0:
        return False, "empty or missing"
    lines = path.read_text().count("\n")
    if lines < 3:
        return False, f"only {lines} lines"
    return True, f"{lines} lines"


def get_track_layer(track):
    """Find which layer a track belongs to."""
    for layer, tracks in LAYERS.items():
        if track in tracks:
            return layer
    return None


def get_reasoning_level(track, override=None):
    """Determine reasoning level for a track."""
    if override:
        return override
    if track in TRACK_REASONING:
        return TRACK_REASONING[track]
    layer = get_track_layer(track)
    if layer and layer in LAYER_REASONING:
        return LAYER_REASONING[layer]
    return "medium"


def build_codex_cmd(repo_dir, output_path, reasoning_level):
    """Build codex exec command with reasoning level."""
    return [
        "codex", "exec",
        "-C", str(repo_dir),
        "--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox",
        "-c", f'model_reasoning_effort="{reasoning_level}"',
        "-o", str(output_path),
    ]


async def run_track(track, prompt_path, output_path, timeout_min, repo_dir,
                    reasoning_level):
    """Run a single review track with timeout."""
    cmd = build_codex_cmd(repo_dir, output_path, reasoning_level)

    log(f"LAUNCH {track} (reasoning={reasoning_level})")
    start = time.time()

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=open(prompt_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout_min * 60
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            elapsed = int(time.time() - start)
            log(f"TIMEOUT {track} after {elapsed}s")
            return False

        elapsed = int(time.time() - start)

        if proc.returncode != 0:
            log(f"ERROR {track}: exit code {proc.returncode} ({elapsed}s)")
            err_path = output_path.with_suffix(".err")
            err_path.write_bytes(stderr or b"")
            return False

        ok, detail = validate_output(output_path)
        if ok:
            log(f"DONE {track}: {detail} ({elapsed}s)")
            return True
        else:
            log(f"FAIL {track}: {detail} ({elapsed}s)")
            return False

    except Exception as e:
        log(f"ERROR {track}: {e}")
        return False


async def run_batch(tracks, prompts_dir, reviews_dir, parallel, timeout_min,
                    repo_dir, force, inject_known, reasoning_override):
    """Run tracks in batches of `parallel`."""
    reviews_dir.mkdir(parents=True, exist_ok=True)

    # Build queue
    queue = []
    for track in tracks:
        prompt = prompts_dir / f"{track}.md"
        output = reviews_dir / f"{track}.md"

        if not prompt.exists():
            log(f"SKIP {track}: no prompt at {prompt.name}")
            continue
        if not force and output.exists() and output.stat().st_size > 0:
            log(f"SKIP {track}: exists (--force to re-run)")
            continue
        if output.exists():
            output.unlink()

        # Inject known issues for M/A tracks
        if inject_known and KNOWN_ISSUES_FILE and track[0] in ("M", "A"):
            combined = reviews_dir / f".prompt_{track}.tmp"
            preamble = KNOWN_ISSUES_FILE.read_text() if KNOWN_ISSUES_FILE.exists() else ""
            combined.write_text(preamble + "\n---\n\n" + prompt.read_text())
            prompt = combined

        reasoning = get_reasoning_level(track, reasoning_override)
        queue.append((track, prompt, output, reasoning))

    log(f"Queued {len(queue)} tracks (parallel={parallel}, timeout={timeout_min}m)")

    # Process in batches
    for i in range(0, len(queue), parallel):
        batch = queue[i:i + parallel]
        tasks = [
            run_track(track, prompt, output, timeout_min, repo_dir, reasoning)
            for track, prompt, output, reasoning in batch
        ]
        results = await asyncio.gather(*tasks)

        # Retry failed tracks once
        for j, (success, (track, prompt, output, reasoning)) in enumerate(
            zip(results, batch)
        ):
            if not success and not output.exists():
                log(f"RETRY {track}")
                await run_track(track, prompt, output, timeout_min, repo_dir,
                                reasoning)

    # Cleanup temp files
    for f in reviews_dir.glob(".prompt_*.tmp"):
        f.unlink()


def main():
    parser = argparse.ArgumentParser(description="Paper review orchestrator")
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=20, help="minutes per track")
    parser.add_argument("--tracks", type=str, help="comma-separated track names")
    parser.add_argument("--layer", type=str, choices=list(LAYERS.keys()),
                        help="run all tracks in a layer")
    parser.add_argument("--reasoning", type=str,
                        choices=["minimal", "low", "medium", "high"],
                        help="override reasoning level for all tracks")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-inject", action="store_true",
                        help="skip known-issues injection")
    args = parser.parse_args()

    if args.tracks:
        tracks = args.tracks.split(",")
    elif args.layer:
        tracks = LAYERS[args.layer]
    else:
        tracks = [t for layer_tracks in LAYERS.values() for t in layer_tracks]

    log(f"=== Paper Review Launch ===")
    log(f"Tracks: {' '.join(tracks)}")
    if args.reasoning:
        log(f"Reasoning override: {args.reasoning}")

    asyncio.run(run_batch(
        tracks, PROMPTS_DIR, REVIEWS_DIR, args.parallel, args.timeout,
        REPO_DIR, args.force, inject_known=not args.no_inject,
        reasoning_override=args.reasoning,
    ))

    # Summary
    done = sum(1 for t in tracks if (REVIEWS_DIR / f"{t}.md").exists())
    log(f"=== Complete: {done}/{len(tracks)} tracks ===")


if __name__ == "__main__":
    main()
