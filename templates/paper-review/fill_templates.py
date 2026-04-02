#!/usr/bin/env python3
"""Fill review prompt templates from project config.

Reads project_config.yaml and generates ready-to-use prompt files
in the output directory.

Usage:
    python fill_templates.py project_config.yaml
    python fill_templates.py project_config.yaml --out-dir ./my_prompts
    python fill_templates.py project_config.yaml --tracks E1,A1,M1
    python fill_templates.py project_config.yaml --list  # show what would be generated
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml required: pip install pyyaml")
    sys.exit(1)

TEMPLATE_DIR = Path(__file__).resolve().parent / "prompts"


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def fill_execute(cfg, track_id):
    """Generate an E-track prompt from config."""
    template = (TEMPLATE_DIR / "E_execute.md").read_text()
    track = cfg["execute_tracks"][track_id]

    values_table = "\n".join(
        f"| {v['metric']} | {v['value']} | {v['source']} |"
        for v in track.get("expected_values", [])
    )
    output_files = ", ".join(f"`{f}`" for f in track.get("output_files", []))

    return (
        template
        .replace("[PIPELINE_NAME]", track["pipeline_name"])
        .replace("[SCRIPT_PATH]", track["script_path"])
        .replace("[REPO_DIR]", cfg.get("analysis_dir", cfg["repo_dir"]))
        .replace("[RUN_COMMAND]", track["run_command"])
        .replace("| [METRIC_1] | [VALUE_1] | [TEX_LOCATION] |\n| [METRIC_2] | [VALUE_2] | [TEX_LOCATION] |", values_table)
        .replace("[OUTPUT_FILES]", output_files)
    )


def fill_m1(cfg):
    """Generate M1 metric validity prompt."""
    template = (TEMPLATE_DIR / "M1_metric_validity.md").read_text()
    scripts = "\n".join(f"- `{s}`" for s in cfg.get("analysis_scripts", []))
    metrics = "\n".join(
        f"- **{m['name']}**: {m['definition']}"
        for m in cfg.get("metrics_to_examine", [])
    )
    return (
        template
        .replace("[LIST_SCRIPTS_AND_METHODS_SECTION]", scripts)
        .replace("[LIST_EACH_METRIC_WITH_PAPER_DEFINITION]", metrics)
    )


def fill_m2(cfg):
    """Generate M2 train/test integrity prompt."""
    template = (TEMPLATE_DIR / "M2_train_test.md").read_text()
    scripts = "\n".join(f"{i+1}. `{s}`" for i, s in enumerate(cfg.get("analysis_scripts", [])))
    fixes = "\n".join(f"- {f}" for f in cfg.get("known_fixes", []))
    return (
        template
        .replace("[LIST_ALL_ANALYSIS_SCRIPTS]", scripts)
        .replace("[LIST_KNOWN_FIXES_FROM_DECISIONS_MD]", fixes or "None from prior rounds.")
    )


def fill_m3(cfg):
    """Generate M3 statistical claims prompt."""
    template = (TEMPLATE_DIR / "M3_statistical.md").read_text()
    scripts = "\n".join(f"- `{s}`" for s in cfg.get("analysis_scripts", []))
    tex = "\n".join(f"- `{t}`" for t in cfg.get("tex_files", []))
    return (
        template
        .replace("[LIST_SCRIPTS_WITH_BOOTSTRAP_OR_PVALUES]", scripts)
        .replace("[MAIN_TEX_FOR_CLAIMS]", tex)
    )


def fill_a1(cfg):
    """Generate A1 break-argument prompt."""
    template = (TEMPLATE_DIR / "A1_break_argument.md").read_text()
    candidates = "\n".join(
        f"{i+1}. **{c['name']}**: {c['description']}"
        for i, c in enumerate(cfg.get("escape_candidates", []))
    )
    tex_files = "\n".join(f"- `{t}`" for t in cfg.get("tex_files", []))
    return (
        template
        .replace("[MAIN_CLAIM]", cfg.get("main_claim", "[fill in]"))
        .replace("[MAIN_TEX_PATH — especially the core argument sections]", tex_files)
        .replace("[SI_PATH — scope and limitations]", "")
        .replace("1. [CANDIDATE_1: describe a specific scenario]\n2. [CANDIDATE_2: describe another]\n3. [CANDIDATE_3: ...]", candidates)
    )


def fill_a2(cfg):
    """Generate A2 baseline fairness prompt."""
    template = (TEMPLATE_DIR / "A2_baseline_fairness.md").read_text()
    pairs = cfg.get("comparison_pairs", [{}])
    p = pairs[0] if pairs else {}
    scripts = "\n".join(f"- `{s}`" for s in p.get("scripts", []))
    return (
        template
        .replace("[METHOD_A]", p.get("method_a", "[method A]"))
        .replace("[METHOD_B]", p.get("method_b", "[method B]"))
        .replace("[CONCLUSION]", p.get("conclusion", "[conclusion]"))
        .replace("[LIST_COMPARISON_SCRIPTS_AND_TEX_SECTIONS]", scripts)
    )


def fill_a3(cfg):
    """Generate A3 missing analyses prompt."""
    template = (TEMPLATE_DIR / "A3_missing_analyses.md").read_text()
    existing = ", ".join(cfg.get("existing_analyses", []))
    tex = ", ".join(f"`{t}`" for t in cfg.get("tex_files", []))
    prov = f"`{cfg.get('provenance_file', 'provenance.yaml')}`"
    return (
        template
        .replace("[TARGET_VENUE]", cfg.get("target_venue", "a top journal"))
        .replace("[MAIN_TEX, SI_TEX, PROVENANCE_FILE]", f"{tex}, {prov}")
        .replace("[LIST_EXISTING]", existing)
    )


def fill_naive_reader(cfg):
    """Generate naive reader prompt."""
    template = (TEMPLATE_DIR / "naive_reader.md").read_text()
    return (
        template
        .replace("[TARGET_AUDIENCE_DESCRIPTION]", cfg.get("target_audience", "[target audience]"))
        .replace("[ASSUMED_BACKGROUND]", cfg.get("assumed_background", "[background]"))
        .replace("[PAPER_SPECIFIC_CONCEPTS]", cfg.get("paper_specific_concepts", "[concepts]"))
        .replace("[MAIN_TEX_PATH]", cfg.get("tex_files", ["main.tex"])[0])
        .replace("[TARGET_AUDIENCE]", cfg.get("target_audience", "").split(" who ")[0] if " who " in cfg.get("target_audience", "") else "target audience")
    )


def fill_citation(cfg):
    """Generate citation verification prompt."""
    template = (TEMPLATE_DIR / "citation_verify.md").read_text()
    tex = ", ".join(f"`{t}`" for t in cfg.get("tex_files", []))
    bib = f"`{cfg.get('bib_file', 'references.bib')}`"
    return template.replace("[MAIN_TEX, SI_TEX, REFERENCES_BIB]", f"{tex}, {bib}")


def fill_known_issues_preamble(cfg):
    """Generate the known-issues preamble for M/A tracks."""
    fixes = cfg.get("known_fixes", [])
    if not fixes:
        return ""
    items = "\n".join(f"- {f}" for f in fixes)
    return f"""## Known Issues (DO NOT re-report as new findings)

The following issues were found in prior rounds and are already tracked.
Verify fixes where relevant, but do not report these as new discoveries:

{items}

If you find that a fix listed above is INCOMPLETE or INCORRECT, report that.

---

"""


# ── Track registry ──

GENERATORS = {
    "M1": lambda cfg: fill_m1(cfg),
    "M2": lambda cfg: fill_m2(cfg),
    "M3": lambda cfg: fill_m3(cfg),
    "A1": lambda cfg: fill_a1(cfg),
    "A2": lambda cfg: fill_a2(cfg),
    "A3": lambda cfg: fill_a3(cfg),
    "naive_reader": lambda cfg: fill_naive_reader(cfg),
    "citation_verify": lambda cfg: fill_citation(cfg),
}


def main():
    parser = argparse.ArgumentParser(description="Fill review templates from config")
    parser.add_argument("config", help="Path to project_config.yaml")
    parser.add_argument("--out-dir", default=None, help="Output directory (default: ./prompts_filled)")
    parser.add_argument("--tracks", default=None, help="Comma-separated track IDs")
    parser.add_argument("--list", action="store_true", help="List tracks without generating")
    parser.add_argument("--inject-known", action="store_true",
                        help="Prepend known-issues preamble to M/A tracks")
    args = parser.parse_args()

    cfg = load_config(args.config)
    out_dir = Path(args.out_dir) if args.out_dir else Path("prompts_filled")

    # Build track list
    all_tracks = []
    for track_id in cfg.get("execute_tracks", {}):
        all_tracks.append(track_id)
    all_tracks.extend(GENERATORS.keys())

    if args.tracks:
        tracks = args.tracks.split(",")
    else:
        tracks = all_tracks

    if args.list:
        print("Available tracks:")
        for t in all_tracks:
            print(f"  {t}")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    preamble = fill_known_issues_preamble(cfg) if args.inject_known else ""

    generated = 0
    for track in tracks:
        if track in cfg.get("execute_tracks", {}):
            content = fill_execute(cfg, track)
        elif track in GENERATORS:
            content = GENERATORS[track](cfg)
        else:
            print(f"SKIP {track}: unknown track")
            continue

        # Inject preamble for M/A tracks
        if args.inject_known and track[0] in ("M", "A"):
            content = preamble + content

        out_path = out_dir / f"{track}.md"
        out_path.write_text(content)
        generated += 1
        print(f"  Generated {out_path.name}")

    print(f"\n{generated} prompts written to {out_dir}/")


if __name__ == "__main__":
    main()
