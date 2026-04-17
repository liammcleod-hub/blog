# Shopify Collections Cleanup — Overview

This folder (`Code/shopify_api_work/`) contains a **read-mostly, approval-gated** workflow for auditing and improving Shopify collections (especially the **MAIN menu**) using the Shopify Admin GraphQL API.

The goal is to:

- **Observe** whether each collection’s products match the collection’s intent (usually implied by its title/handle).
- **Propose** safe, reviewable changes (rulesets, converts, redirects, menu updates) without writing to Shopify.
- **Apply** only the changes a human explicitly approves (and re-verify after writes).

This is intended as a repeatable operational tool: generate reports → decide → apply → re-run to confirm improvements.

---

## Mental model

Think of the system as a loop with a hard approval gate:

1. **Fetch scope** (primarily MAIN-menu collections)
2. **Observe** (metrics + findings)
3. **Propose** (action plan per collection)
4. **Approval** (human edits an approvals JSON)
5. **Apply** (writes to Shopify, guarded by `--yes`)
6. **Re-observe** (confirm deltas / no regressions)

The “alma mater canary” idea is a *process choice outside the loop*: pick a worst-behaving collection (e.g. very high outlier ratio) to validate that the loop + metrics are actually useful before scaling changes broadly.

---

## What “collections” means here

Shopify collections come in two main forms:

- **SMART collections**: have a `ruleSet` (rules like “TAG equals X” / “TITLE contains Y”). Shopify computes membership.
- **MANUAL collections**: membership is curated by humans.

In this repo:

- We treat MAIN-menu collections as the primary operational surface.
- “Curated” vs “taxonomy” vs “never touch” is tracked in config and used to decide what automation is allowed.

---

## Key concepts and metrics (the “observe” vocabulary)

These metrics appear in reports (notably `orchestrate --mode propose`) and are used to prioritize work:

### `outlier_ratio`
Fraction of products in the collection that look **irrelevant** to the collection intent.

- Computed by `verify_logic.verify_congruency(...)`.
- “Irrelevant” is judged by matching product titles against a keyword set derived from the collection title/handle (and sometimes ruleSet keywords for umbrella cases).
- High `outlier_ratio` means the collection is “noisy”.

### `coverage_ratio`
Fraction of products that look **relevant** (i.e. `1 - outlier_ratio`).

- Useful because you can improve outliers by either tightening (reducing noise) *or* by getting too strict and losing coverage.
- Together, `outlier_ratio` and `coverage_ratio` allow you to reason about tradeoffs.

### `rule_breadth`
Proxy for “how broad/complex the SMART rule definition is”.

- For SMART collections: number of rules in the rule set.
- For MANUAL collections: `0` (no rules).

This is *not* a quality metric by itself; it’s a diagnostic signal. Very broad rules can be correct for “umbrella” collections, but they can also be a source of noise.

### `manual_rule_breadth_80` (MANUAL-only)
Proxy for “how complex the *implicit* membership logic is” for MANUAL collections.

Since MANUAL collections have no Shopify `ruleSet`, we infer a lightweight approximation from current members:

- We generate candidate SMART-style rules (e.g. `TAG == X`, `TYPE == Y`, `VENDOR == Z`, `TITLE contains K`).
- We compute how many current members each candidate would match (“member coverage”).
- We greedily pick the smallest set of candidates that covers **≥ 80% of current members**.

`manual_rule_breadth_80` is the size of that picked set.

Interpretation:

- Small (e.g. 1–3): membership is cohesive and often convertible to SMART taxonomy.
- Large: membership is curated/heterogeneous; conversion to SMART is riskier and usually not worth automating without additional guardrails.

### `disj` / `appliedDisjunctively`
How Shopify combines SMART rules:

- `True` usually corresponds to **OR** logic (a product may match any rule).
- `False` usually corresponds to **AND** logic (a product must match all rules).

AND logic on many rules often yields empty or overly strict collections; OR logic on broad rules can yield noisy collections.

### “Tighten candidates” (actionable rule intelligence)
When diagnosing a SMART collection, we can estimate which rules are likely admitting outliers by comparing how often each rule matches:

- outlier products vs inlier products
- and computing a simple “precision” proxy

This shows up via `diagnose` (and is designed to be used by “propose” work).

---

## MANUAL rule inference (what it is and what it is not)

MANUAL inference is intentionally **member-only**:

- It does **not** estimate “leakage” against the full catalog yet.
- It is used as a conservative signal for “convertibility” rather than a guarantee.

Inference output (when available) includes:

- Candidate rules in Shopify ruleSet shape: `{column, relation, condition}`
- `selected_rules_80` / `selected_rules_90`
- `suggested_ruleSet` (preferred ruleset proposal, may use AND logic to narrow leakage)
- A `convertibility` level: `HIGH | MED | LOW` with reasons

When `convertibility=HIGH`, `propose` may emit a `replace_with_smart` action that uses the inferred rules (still approval-gated).

### Proposal dry-run (member-only)

For proposals that include a ruleSet change (`replace_with_smart` or `update_ruleSet`), orchestrate now attaches a small **dry_run** simulation:

- It evaluates the proposed ruleSet against the current collection members only.
- It reports `members_matched / members_total` and an excluded sample.
- This answers “what happens to the current members if we apply this ruleset?” (but it still does not measure catalog-wide leakage).

### SEO handle normalization (title-derived handle)

For MANUAL→SMART swaps (`replace_with_smart`), proposals may include a `final_handle` derived from the collection title:

- Lowercase slug, ASCII-only; German umlauts are removed (`ä→a`, `ö→o`, `ü→u`, `ß→ss`).
- On apply, after the SMART collection is promoted, the handle is updated to `final_handle`, redirects are created, and MAIN menu URLs are rewritten (best-effort) to the final handle.

### Publishing (Online Store)

Write operations that change collections are expected to keep the resulting collection visible on the storefront:

- `replace_with_smart` apply publishes the newly created SMART collection to **Online Store**.
- `update_ruleSet` apply also publishes the collection to **Online Store** as a safe default.

---

## Safety model

This tool is designed to be safe-by-default:

- Most commands are **read-only**.
- Any write requires `--yes` (and typically an explicit approval file).
- After applying ruleSet changes to SMART collections, the system **re-verifies**. If verification fails and the write was a ruleSet update, it may roll back to the pre-change ruleset snapshot.

Never commit secrets:

- Credentials live in `Code/shopify_api_work/.env` (local only).

---

## Configuration

`collections_cleanup_config.json` controls policy and behavior, including:

- `menu_id` (MAIN menu)
- `curated_handles` (manual/curated allowlist)
- `never_touch_handles` (excluded from automation)
- optional overrides for converting MANUAL → SMART
- verification tuning (umbrella handles, synonym expansions, exemptions)

See:

- `shopify_api_work/collections_cleanup_config.example.json`
- `shopify_api_work/collections_cleanup_config.json`

---

## Commands (what runs and what it produces)

All commands go through:

`python shopify_api_work/collections_cleanup_runner.py <command> [args...]`

### Read-only commands

- `list`
  - Lists collections (implementation in `list_collections.py`).

- `inspect --handle <handle>`
  - Fetches and prints raw collection details.

- `explain --handle <handle>`
  - Explains which SMART rules match which products (rule-by-product matching).

- `verify --handle <handle>`
  - Computes `outlier_ratio` + `coverage_ratio` (+ other details).
  - Primary implementation: `verify_logic.py`.

- `diagnose --handle <handle>`
  - For SMART collections: reports noisy rules (“tighten candidates”) and outlier examples.
  - Primary implementation: `diagnose_logic.py`.

- `menu-audit`
  - MAIN-menu focused: produces a “question queue” about MANUAL collections and suspicious SMART cases.
  - Outputs:
    - `shopify_api_work/out/menu_audit_questions.json`
    - `shopify_api_work/out/menu_audit_questions.md`

- `umbrella-suggest`
  - MAIN-menu focused: suggests which collections should be verified using umbrella (ruleSet) keyword mode.
  - Outputs a timestamped report in `shopify_api_work/out/`.

### Proposal + approval-gated workflows

- `propose --handle <handle> [--menu-only]`
  - Generates a proposal JSON for one collection.
  - Writes: `shopify_api_work/out/proposal_<handle>.json`
  - No Shopify writes.

- `apply --proposal <path> --yes`
  - Applies one approved proposal to Shopify.
  - Writes to Shopify; guarded by `--yes`.

### Orchestrated loop (MAIN menu only)

- `orchestrate --mode propose`
  - MAIN-menu sweep: for each menu handle, observes (verification) and builds proposals and a prioritized report.
  - Writes multiple timestamped artifacts in `shopify_api_work/out/`, including:
    - `orchestrate_report_<ts>.md` (human-readable)
    - `orchestrate_approval_<ts>.json` (approval gate)
    - `orchestrate_sorted_<ts>.md/.json` (airtight vs not-airtight)
    - `observe_<ts>.json` (observe snapshot, verification + MANUAL inference)
    - `orchestrate_proposals_<ts>.md` (human-readable list of proposed actions)
    - `orchestrate_proposals_<ts>.json` (structured proposals derived from the observe snapshot)

- `orchestrate --mode apply --approval-file <file> --yes`
  - Applies only approved rows from the approval file.
  - Re-verifies SMART collections after writes.
  - Approval items include `collection_id` and apply resolves collections by ID to avoid handle drift during swaps.

### Curation workflow (MAIN menu only)

- `curation --mode propose`
  - Generates an approval file to classify MAIN-menu collections as:
    - `never_touch`, `curated`, or `taxonomy`

- `curation --mode apply --approval-file <file> --yes`
  - Applies those classification decisions into config.

### Other write commands (guarded)

- `publish --handle <handle> --yes`
  - Publishes a collection to a named publication.

- `seo --handle <handle> ... --yes`
  - Updates SEO/title/description, optional handle updates, optional menu update.

- `redirect --path <path> --target <target> --yes`
  - Creates a URL redirect.

---

## File map (where to look)

### Entrypoints

- `shopify_api_work/collections_cleanup_runner.py`
  - Thin runner that calls `collections_cleanup_core.main()`.

- `shopify_api_work/collections_cleanup_core.py`
  - Intentionally small dispatcher; defers to `collections_cleanup_impl.py`.

### Core implementation

- `shopify_api_work/collections_cleanup_impl.py`
  - CLI argument parsing, orchestrate loop, coordination between modules.

### Observe/verify/diagnose logic

- `shopify_api_work/verify_logic.py`
  - Keyword building and congruency verification.

- `shopify_api_work/diagnose_logic.py`
  - Rule-level diagnosis (“tighten candidates”), outlier breakdown.

### Propose/apply logic

- `shopify_api_work/proposal_logic.py`
  - Builds proposals (what changes to recommend).

- `shopify_api_work/apply_logic.py`
  - Executes proposal actions (writes to Shopify).

### Reporting/output

- `shopify_api_work/orchestrate_reporting.py`
  - Generates orchestrate reports + approval files in `shopify_api_work/out/`.

### Shopify access

- `shopify_api_work/shopify_client.py`
  - GraphQL client + read operations.

- `shopify_api_work/shopify_writes.py`
  - GraphQL write operations (guarded upstream by `--yes`).

---

## How to run “the loop on the loop” (sanity check)

Typical operational cadence:

1. `python shopify_api_work/collections_cleanup_runner.py orchestrate --mode propose`
2. Review `shopify_api_work/out/orchestrate_report_<ts>.md`
3. Edit `shopify_api_work/out/orchestrate_approval_<ts>.json` and mark approvals
4. `python shopify_api_work/collections_cleanup_runner.py orchestrate --mode apply --approval-file <that file> --yes`
5. Re-run step (1) to confirm metrics improved and nothing regressed

---

## Observe snapshots → reproducible propose

`orchestrate --mode propose` now writes a timestamped observe snapshot:

- `shopify_api_work/out/observe_<ts>.json`

This snapshot captures the MAIN-menu scope and the observe outputs per handle (verification + MANUAL inference).

Single-handle `propose` prefers the most recent snapshot for MANUAL inference, so you can get proposals that are consistent with the last observed state:

- `python shopify_api_work/collections_cleanup_runner.py propose --handle <handle> --menu-only`
- Optional: `--observe-file <path>` to pin to a specific snapshot.

---

## Skill integration

This folder also includes a Codex skill definition:

- `shopify_api_work/collections-cleanup-skill/SKILL.md`

That skill describes how to operate the workflow and reinforces:

- secrets in `.env`
- approval-gated writes
- orchestrate and curation loops
