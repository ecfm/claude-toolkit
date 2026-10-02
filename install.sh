#!/bin/bash
# Install Claude Code and Codex config files by symlinking from this repo.
# Run once per server after cloning:
#   git clone git@github.com:ecfm/claude-toolkit.git ~/Mao/claude-toolkit
#   bash ~/Mao/claude-toolkit/install.sh

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing from: ${REPO_DIR}"

# Create ~/.claude directories
mkdir -p ~/.claude/commands
mkdir -p ~/.claude/agents

# Symlink CLAUDE.md (global instructions)
if [ -L ~/.claude/CLAUDE.md ]; then
    echo "~/.claude/CLAUDE.md already symlinked"
elif [ -f ~/.claude/CLAUDE.md ]; then
    echo "~/.claude/CLAUDE.md exists (not a symlink). Backing up to ~/.claude/CLAUDE.md.bak"
    mv ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak
    ln -sf "${REPO_DIR}/claude/CLAUDE.md" ~/.claude/CLAUDE.md
    echo "Symlinked ~/.claude/CLAUDE.md"
else
    ln -sf "${REPO_DIR}/claude/CLAUDE.md" ~/.claude/CLAUDE.md
    echo "Symlinked ~/.claude/CLAUDE.md"
fi

# settings.json: each machine keeps its own copy. Copy the shared one only if none exists.
if [ -e ~/.claude/settings.json ]; then
    echo "~/.claude/settings.json exists; left unchanged (compare with ${REPO_DIR}/claude/settings.json)"
else
    cp "${REPO_DIR}/claude/settings.json" ~/.claude/settings.json
    echo "Copied ~/.claude/settings.json"
fi

# Codex reads the same global AGENTS.md
mkdir -p ~/.codex
if [ -L ~/.codex/AGENTS.md ]; then
    echo "~/.codex/AGENTS.md already symlinked"
else
    if [ -f ~/.codex/AGENTS.md ]; then
        mv ~/.codex/AGENTS.md ~/.codex/AGENTS.md.bak
        echo "Backed up ~/.codex/AGENTS.md to ~/.codex/AGENTS.md.bak"
    fi
    ln -s "${REPO_DIR}/AGENTS.md" ~/.codex/AGENTS.md
    echo "Symlinked ~/.codex/AGENTS.md"
fi

# Symlink all commands
for cmd in "${REPO_DIR}"/claude/commands/*.md; do
    [ -f "$cmd" ] || continue
    name=$(basename "$cmd")
    ln -sf "$cmd" ~/.claude/commands/"$name"
    echo "Symlinked ~/.claude/commands/${name}"
done

# Rules were folded into AGENTS.md; remove old links that pointed into this repo
for link in ~/.claude/rules/*.md; do
    [ -L "$link" ] || continue
    case "$(readlink "$link")" in
        "${REPO_DIR}"/*|"$(cd "${REPO_DIR}" && pwd -P)"/*) rm "$link"; echo "Removed old rule link ${link}" ;;
    esac
done

# Symlink all agents
for agent in "${REPO_DIR}"/claude/agents/*.md; do
    [ -f "$agent" ] || continue
    name=$(basename "$agent")
    ln -sf "$agent" ~/.claude/agents/"$name"
    echo "Symlinked ~/.claude/agents/${name}"
done

# Symlink all skills (entire directories)
mkdir -p ~/.claude/skills
for skill_dir in "${REPO_DIR}"/claude/skills/*/; do
    [ -d "$skill_dir" ] || continue
    name=$(basename "$skill_dir")
    if [ -L ~/.claude/skills/"$name" ]; then
        echo "~/.claude/skills/${name} already symlinked"
    elif [ -d ~/.claude/skills/"$name" ]; then
        echo "~/.claude/skills/${name} exists (not a symlink). Backing up."
        mv ~/.claude/skills/"$name" ~/.claude/skills/"${name}.bak"
        ln -sf "$skill_dir" ~/.claude/skills/"$name"
        echo "Symlinked ~/.claude/skills/${name}"
    else
        ln -sf "$skill_dir" ~/.claude/skills/"$name"
        echo "Symlinked ~/.claude/skills/${name}"
    fi
done

echo ""
echo "Done. Verify with:"
echo "  ls -la ~/.claude/CLAUDE.md"
echo "  ls -la ~/.claude/settings.json"
echo "  ls -la ~/.claude/commands/"
echo "  ls -la ~/.codex/AGENTS.md"
echo "  ls -la ~/.claude/agents/"
echo "  ls -la ~/.claude/skills/"
