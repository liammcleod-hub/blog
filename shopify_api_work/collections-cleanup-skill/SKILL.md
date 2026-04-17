---
name: shopify-collections-cleanup
description: "Audit Shopify collections for relevance to their names, separate curated vs taxonomy collections, generate approval-gated proposals, and (after approval) apply ruleSet fixes and safe collection membership changes via the Admin GraphQL API."
---

# Shopify Collections Cleanup

## Safety + credentials

- Never store tokens in markdown/config. Read from a local `.env` file.
- Default `.env` location in this repo: `Code/shopify_api_work/.env`
- Runner docs: `Code/shopify_api_work/collections_cleanupingestion.md`

## Core workflow (approval gate)

1) List/inspect collections (read-only)
2) Generate proposal JSON for a specific collection
3) Human reviews the proposal JSON
4) Apply the proposal with `--yes`

## Commands

- Infer curated vs taxonomy vs never-touch (MAIN menu only):
  - `python Code/shopify_api_work/collections_cleanup_runner.py curation --mode propose`
  - In the generated approval file in `Code/shopify_api_work/out/`, set `"decision"` to one of:
    - `never_touch` (excluded from all future automation),
    - `curated` (manual/curated collections list),
    - `taxonomy` (safe to automate)
  - Apply decisions to `collections_cleanup_config.json`:
    - `python Code/shopify_api_work/collections_cleanup_runner.py curation --mode apply --approval-file <file> --yes`

- Orchestrate the full MAIN-only loop (prioritized report + approval gate):
  - `python Code/shopify_api_work/collections_cleanup_runner.py orchestrate --mode propose`
  - Edit the generated approval file in `Code/shopify_api_work/out/` and mark approvals by setting either:
    - `"approve": "X"` (recommended), or
    - `"approved": true`
  - Apply approved items + re-pull + regenerate audits:
    - `python Code/shopify_api_work/collections_cleanup_runner.py orchestrate --mode apply --approval-file <file> --yes`

- List all collections:
  - `python Code/shopify_api_work/collections_cleanup_runner.py list`

- Generate “question queue” for MAIN menu collections (read-only):
  - `python Code/shopify_api_work/collections_cleanup_runner.py menu-audit`
  - Outputs: `Code/shopify_api_work/out/menu_audit_questions.md`

- Suggest umbrella-mode verifications (MAIN menu only, read-only):
  - `python Code/shopify_api_work/collections_cleanup_runner.py umbrella-suggest`
  - Outputs: `Code/shopify_api_work/out/umbrella_suggest_<timestamp>.md`
  - Then add approved handles into `verify_umbrella_handles` in `Code/shopify_api_work/collections_cleanup_config.json`

- Inspect one collection:
  - `python Code/shopify_api_work/collections_cleanup_runner.py inspect --handle <handle>`

- Propose rule fixes (writes nothing):
  - `python Code/shopify_api_work/collections_cleanup_runner.py propose --handle <handle> --menu-only`

- Apply an approved proposal (writes):
  - `python Code/shopify_api_work/collections_cleanup_runner.py apply --proposal Code/shopify_api_work/out/proposal_<handle>.json --yes`

## Curated vs taxonomy

- Curated collections are defined explicitly by handle in `Code/shopify_api_work/collections_cleanup_config.json`.
- If the config file is missing, copy from `Code/shopify_api_work/collections_cleanup_config.example.json`.

## “Taste profile” for the store

- Manual collections in the MAIN menu that are **not** in the curated allowlist are flagged for human classification in `menu-audit`.
- To convert a specific MANUAL collection to SMART, add a `manual_to_smart_overrides.<handle>` ruleSet in `collections_cleanup_config.json`, then run `propose` + `apply`.
