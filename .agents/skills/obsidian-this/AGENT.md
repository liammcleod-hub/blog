# Obsidian This Agent Note

This bundle is meant to be usable from more than one CLI agent.

The neutral execution surface is:

- `python .agents/skills/obsidian-this/scripts/obsidian_this.py init --repo <path>`
- `python .agents/skills/obsidian-this/scripts/obsidian_this.py check --repo <path>`
- `python .agents/skills/obsidian-this/scripts/obsidian_this.py fix --repo <path>`

Agent-specific markdown files such as `SKILL.md` are wrappers, not the real portability boundary.

The real durable repo lesson lives in:

- `.obsidian-this/config.json`

Any CLI agent that can:

- read markdown instructions
- run a local command
- operate on repo-local files

can use this framework.

v1 rule:

- `fix` is for graph hygiene only
- file-format normalization is not part of `fix`
