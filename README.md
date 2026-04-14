# Bastelschachtel

Working repo for Bastelschachtel’s SEO/AEO research, content pipeline, and Shopify publishing integration.

## Start Here

- `README_START_HERE.md` (pipeline overview + next tasks)
- `SHOPIFY_INTEGRATION_STRATEGY.md` (architecture + integration plan)
- `.agents/product-marketing-context.md` (source-of-truth context)
- Key doc entrypoints:
  - `docs/seo/README.md`
  - `docs/customer reviews/README.md`
  - `docs/superpowers/specs/README.md`
  - `docs/reference/skill-guides/README.md`
  - `output/content-jobs/README.md`

## Secrets & Environment

This repo uses GitHub push protection. Do not commit secrets.

- `.env` is gitignored
- Copy `.env.example` → `.env` and set `SHOPIFY_ACCESS_TOKEN`

PowerShell example:

```powershell
Copy-Item .env.example .env
$env:SHOPIFY_ACCESS_TOKEN = "<your token>"
```

Several scripts under `docs/core tech seo/` read `SHOPIFY_ACCESS_TOKEN` from the environment and exit if it’s missing.

## Obsidian Tags

- Visible repo docs that use tags should keep the note title first and put the tag line directly under the `#` heading.
- Visible skill notes in `repo-skills/marketing-library/skills/*/SKILL.md` should keep a bottom-only `#skills` tag.
- Do not add Obsidian tags to hidden `.agents/` files.
- Do not add Obsidian tags to generated artifacts or `output/content-jobs/_template/`.

## Repo Tree

This is a names-only orientation map. If it drifts, refresh it from current folder and file names only. Do not read file contents to update this section.

```text
./
|- .agents/
|  |- marketingskills/
|  |- skills/
|  `- product-marketing-context.md
|- .anton/
|- .claude/
|- .codex/
|- .obsidian/
|- .skill-backups/
|- bastelschachtel.agents/
|- brand_assets/
|- docs/
|  |- customer reviews/
|  |- deep research reports/
|  |- reference/
|  |  |- content-pipeline/
|  |  |- retool/
|  |  `- skill-guides/
|  |- seo/
|  |- strategy/
|  `- superpowers/
|     |- plans/
|     `- specs/
|- output/
|  |- content-jobs/
|  |- playwright/
|  `- README.md
|- plugins/
|- public/
|- repo-skills/
|  |- blog-seo-pipeline/
|  |- marketing-library/
|  `- README.md
|- README.md
|- README_START_HERE.md
`- sessionstart.md
```

## Source Of Truth

- `.agents/product-marketing-context.md` is Bastelschachtel's full operating context note.
- `.agents/marketingskills/` is the real marketing skill source tree.
- `repo-skills/marketing-library/` is a visible report-only mirror and may contain broken shared-tool links if the mirror is incomplete.
- Repo docs and repo-owned notes are the place where Bastelschachtel Obsidian graph maintenance is allowed.

## Core Workflows

- Research and SEO planning live under [[docs/seo/README]] and [[docs/customer reviews/README]].
- Repo specs and implementation plans live under [[docs/superpowers/specs/README]] and `docs/superpowers/plans/`.
- Skill-guide routing lives under [[docs/reference/skill-guides/README]].
- Content-job operational output lives under [[output/content-jobs/README]].

## Obsidian Rules

- Bastelschachtel fixable zones:
  - [[docs/seo/README]]
  - [[docs/customer reviews/README]]
  - [[docs/superpowers/specs/README]]
  - `.codex/memories/bastelschachtel/`
  - `.agents/product-marketing-context.md`
  - [[docs/reference/skill-guides/README]]
  - [[docs/reference/skill-guides/blogs]]
  - [[output/content-jobs/README]]
- Skill-library trees are report-only in v1.
- New visible skill-library roots must be registered in `.agents/skills/obsidian-check/scripts/config.py` and covered by `obsidian-check` tests.
- Never add wikilinks to `output/content-jobs/_template/` or copied/generated content-job bundle files.

## Key Commands

- `python .agents/skills/obsidian-check/scripts/obsidian_check.py check`
- `python .agents/skills/obsidian-check/scripts/obsidian_check.py check --fix`
- `python .agents/skills/obsidian-check/scripts/obsidian_check.py check --print-verification-roots`

## Git / Branch Workflow

This repo is pushed to GitHub at `liammcleod-hub/blog` (remote: `origin`/`origin-https`).

```powershell
git status
git add README.md
git commit -m "docs: update README"
git -c http.sslBackend=openssl push -u origin-https bastelschachtel-2026-04-14
```
