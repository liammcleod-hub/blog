# Obsidian This Portable Skill Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable `obsidian-this` framework that can be copied to other repos, generate a small repo-local config from discovery, and then maintain Obsidian graph hygiene through `init`, `check`, and `fix` from Codex, Claude, Gemini, or another CLI agent.

**Architecture:** The implementation should split cleanly between agent-agnostic core artifacts and optional agent-specific wrappers. The core is a neutral script plus repo-readable markdown instructions plus a repo-local config model. `init` performs bounded discovery and writes config, `check` audits against config, and `fix` applies only deterministic graph-hygiene fixes. Format normalization remains report-only in v1 and is never part of `fix`.

**Tech Stack:** Repo-readable markdown instructions, neutral local script entrypoint, repo-local config under `.obsidian-this/`, Python or PowerShell scripts for scanning, markdown fixture trees for tests, and `rg` for repo verification.

---

## File Structure

Planned file map:

- Create: `.agents/skills/obsidian-this/`
  Responsibility: repo-local copyable source bundle.
- Create: `.agents/skills/obsidian-this/SKILL.md`
  Responsibility: Codex-readable wrapper instructions.
- Create: `.agents/skills/obsidian-this/AGENT.md`
  Responsibility: agent-agnostic usage note describing how any CLI agent should invoke the script and config.
- Create: `.agents/skills/obsidian-this/scripts/obsidian_this.py`
  Responsibility: main neutral entrypoint for `init`, `check`, and `fix`.
- Create: `.agents/skills/obsidian-this/scripts/config_schema.py`
  Responsibility: config model, defaults, and validation helpers.
- Create: `.agents/skills/obsidian-this/scripts/discovery.py`
  Responsibility: bounded repo scan for visible markdown roots, forbidden zones, navigation docs, skill-note trees, and normalization candidates.
- Create: `.agents/skills/obsidian-this/scripts/scope.py`
  Responsibility: classify files into graph-fixable, report-only, forbidden, and normalization-candidate classes from config.
- Create: `.agents/skills/obsidian-this/scripts/link_parser.py`
  Responsibility: extract wikilinks, markdown links, relative paths, and link-shape findings.
- Create: `.agents/skills/obsidian-this/scripts/checks.py`
  Responsibility: graph hygiene, tag hygiene, and hidden-target misuse checks.
- Create: `.agents/skills/obsidian-this/scripts/fix_engine.py`
  Responsibility: deterministic `fix` behavior for configured graph-fixable notes only.
- Create: `.agents/skills/obsidian-this/scripts/reporting.py`
  Responsibility: stable output for `init`, `check`, and `fix`.
- Create: `.agents/skills/obsidian-this/tests/`
  Responsibility: unit and fixture-backed tests for the portable behavior.
- Create: `.agents/skills/obsidian-this/tests/fixtures/`
  Responsibility: generic repo fixture trees covering title-first notes, titleless notes, skill-note trees, forbidden outputs, and normalization candidates.
- Create later if needed: `.agents/skills/obsidian-this/README.md`
  Responsibility: maintainer reference only if `SKILL.md` grows too large.

Repo-local runtime outputs:

- Create on `init`: `.obsidian-this/`
  Responsibility: repo-local persistent state for obsidianification.
- Create on `init`: `.obsidian-this/config.json`
  Responsibility: explicit repo lesson used by future `check` and `fix`.

## Chunk 1: Portable Skill Scaffold And Config Model

### Task 1: Scaffold the portable skill bundle

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/SKILL.md`
- Create: `$HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_smoke.py`

- [ ] **Step 1: Create the portable skill directory skeleton**

Create:

- `C:/Users/Hp/.agents/skills/obsidian-this/`
- `C:/Users/Hp/.agents/skills/obsidian-this/scripts/`
- `C:/Users/Hp/.agents/skills/obsidian-this/tests/`
- `C:/Users/Hp/.agents/skills/obsidian-this/tests/fixtures/`

- [ ] **Step 2: Write the initial `SKILL.md`**

Document:

- when to use `obsidian-this`
- `init`
- `check`
- `fix`
- the rule that repo-local config is the only durable lesson
- the rule that format normalization is not part of `fix` in v1

- [ ] **Step 3: Write `AGENT.md`**

Document:

- neutral invocation pattern
- how Codex, Claude, Gemini, or another CLI agent should read the bundle
- that the script is the real execution surface
- that agent-specific wrappers are optional and secondary

- [ ] **Step 4: Write the failing smoke test**

Cover:

- `obsidian_this.py` exists
- command parsing recognizes `init`, `check`, and `fix`
- the module exits cleanly with help or placeholder messaging

- [ ] **Step 5: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_smoke.py -v`

Expected: FAIL because the scaffold does not exist yet.

- [ ] **Step 6: Write minimal entrypoint implementation**

The entrypoint should:

- parse the three commands
- dispatch to placeholder handlers
- return stable exit codes

- [ ] **Step 7: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_smoke.py -v`

Expected: PASS.

### Task 2: Implement the repo-local config model

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/scripts/config_schema.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_config_schema.py`

- [ ] **Step 1: Write the failing config-schema tests**

Cover:

- default config shape
- required keys:
  - `graph_roots`
  - `forbidden_roots`
  - `repo_facing_navigation_docs`
  - `tag_rules`
  - `skill_note_rules`
  - `normalization_candidates`
  - `normalization_exclusions`
  - `fix_permissions`
- validation rejects missing required keys
- validation rejects invalid tag placement values
- validation rejects unknown `fix_permissions` keys

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_config_schema.py -v`

Expected: FAIL because the config model is missing.

- [ ] **Step 3: Write minimal config-schema implementation**

The schema should:

- create a stable default config object
- validate loaded config
- expose helpers for reading and writing `.obsidian-this/config.json`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_config_schema.py -v`

Expected: PASS.

## Chunk 2: Discovery And Scope

### Task 3: Implement bounded repo discovery for `init`

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/scripts/discovery.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_discovery.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo/`

- [ ] **Step 1: Write the failing discovery tests**

Cover:

- visible markdown-heavy folders are proposed as graph roots
- output/template/test/fixture style folders are proposed as forbidden roots
- root and folder `README.md` files are proposed as navigation docs
- visible skill-note trees are proposed as report-only or special skill-note roots
- non-markdown docs are classified as:
  - normalization candidates
  - explicit exclusions

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_discovery.py -v`

Expected: FAIL because discovery is missing.

- [ ] **Step 3: Write minimal discovery implementation**

The discovery layer should:

- scan only the visible repo tree under the current working directory
- ignore hidden-dotfolder contents for graph participation unless explicitly allowed by config
- identify proposals rather than silently activating behavior
- produce a structured `init` proposal object

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_discovery.py -v`

Expected: PASS.

### Task 4: Implement explicit scope classification from config

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/scripts/scope.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_scope.py`

- [ ] **Step 1: Write the failing scope tests**

Cover:

- graph-fixable note classification
- report-only note classification
- forbidden zone classification
- format-normalization candidate classification
- `repo_facing_navigation_docs` drives link-class enforcement boundaries
- titleless notes are not auto-upgraded into taggable notes

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_scope.py -v`

Expected: FAIL because scope classification is missing.

- [ ] **Step 3: Write minimal scope implementation**

The classifier must:

- use config, not heuristics, for active behavior
- keep normalization candidates separate from graph-fixable notes
- expose helpers for:
  - `is_graph_fixable`
  - `is_report_only`
  - `is_forbidden`
  - `is_normalization_candidate`
  - `is_repo_facing_navigation_doc`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_scope.py -v`

Expected: PASS.

## Chunk 3: Read-Only Checking

### Task 5: Implement link parsing and link-shape checks

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/scripts/link_parser.py`
- Create: `$HOME/.agents/skills/obsidian-this/scripts/checks.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_link_parser.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_checks.py`

- [ ] **Step 1: Write the failing parser and check tests**

Cover:

- visible note targets using wikilinks
- hidden or non-clickable targets using plain paths
- reference syntax paths in implementation notes
- fake clickable hidden targets
- visible note paths written as plain code in configured navigation docs
- titleless-note tag ambiguity

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_link_parser.py $HOME/.agents/skills/obsidian-this/tests/test_checks.py -v`

Expected: FAIL because parsing and checks are missing.

- [ ] **Step 3: Write minimal parser and check implementation**

The check layer should produce structured findings for:

- missing upward links
- missing entrypoint links
- wrong link class usage
- tag placement mismatch
- bottom-only skill-tag absence
- normalization candidate vs exclusion reporting

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_link_parser.py $HOME/.agents/skills/obsidian-this/tests/test_checks.py -v`

Expected: PASS.

### Task 6: Implement `init` and `check` reporting

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/scripts/reporting.py`
- Modify: `$HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_reporting.py`

- [ ] **Step 1: Write the failing reporting tests**

Cover:

- `init` proposal report
- `check` graph hygiene report
- forbidden-zone summary
- normalization-candidate summary
- no-op clean output

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_reporting.py -v`

Expected: FAIL because reporting is missing.

- [ ] **Step 3: Write minimal reporting implementation**

The formatter should clearly show:

- discovered proposals during `init`
- active config during `check`
- findings grouped by class
- files or zones never touched

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_reporting.py -v`

Expected: PASS.

## Chunk 4: Safe Fixes And End-To-End Wiring

### Task 7: Implement deterministic `fix` behavior

**Files:**
- Create: `$HOME/.agents/skills/obsidian-this/scripts/fix_engine.py`
- Create: `$HOME/.agents/skills/obsidian-this/tests/test_fix_engine.py`

- [ ] **Step 1: Write the failing fix-engine tests**

Cover:

- add missing upward link to configured entrypoint
- add minimal related-doc block in deterministic cases
- normalize visible note target to wikilink in configured navigation docs
- downgrade fake clickable hidden target to plain path
- place tags below H1 when configured and H1 exists
- append bottom-only `#skills` in configured skill-note roots
- reject fixes in forbidden zones
- reject fixes in report-only roots
- reject all file-format normalization attempts
- reject titleless-note top-tag insertion

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_fix_engine.py -v`

Expected: FAIL because the fix engine is missing.

- [ ] **Step 3: Write minimal fix-engine implementation**

The engine should:

- touch only graph-fixable notes
- apply one small edit per finding
- return touched files for re-verification
- never mutate the config during `fix`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests/test_fix_engine.py -v`

Expected: PASS.

### Task 8: Wire end-to-end `init`, `check`, and `fix`

**Files:**
- Modify: `$HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_smoke.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_config_schema.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_discovery.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_scope.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_link_parser.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_checks.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_reporting.py`
- Test: `$HOME/.agents/skills/obsidian-this/tests/test_fix_engine.py`

- [ ] **Step 1: Wire `init`**

`init` should:

1. run discovery
2. build proposal object
3. write `.obsidian-this/config.json`
4. print proposal summary

- [ ] **Step 2: Wire `check`**

`check` should:

1. load config
2. classify scope
3. parse links
4. run checks
5. print report

- [ ] **Step 3: Wire `fix`**

`fix` should:

1. load config
2. run checks
3. apply allowed deterministic fixes
4. re-run relevant checks on touched files
5. print report and fix summary

- [ ] **Step 4: Run full skill-local test suite**

Run: `pytest $HOME/.agents/skills/obsidian-this/tests -v`

Expected: PASS.

## Chunk 5: Verification And Copyability

### Task 9: Verify copyable behavior in a fixture-backed repo

**Files:**
- Modify: none unless a real bug is found

- [ ] **Step 1: Run `init` against the generic fixture repo**

Run: `python $HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py init --repo $HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo`

Expected:

- `.obsidian-this/config.json` is created in the target fixture repo
- graph roots are proposed
- forbidden roots are proposed
- normalization candidates and exclusions are reported separately

- [ ] **Step 2: Run `check` against the configured fixture repo**

Run: `python $HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py check --repo $HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo`

Expected:

- link-class findings are reported correctly
- titleless-note tag ambiguity is reported but not fixed
- report-only and forbidden zones are not treated as fixable

- [ ] **Step 3: Run `fix` against the configured fixture repo**

Run: `python $HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py fix --repo $HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo`

Expected:

- only graph-fixable notes change
- bottom-only `#skills` is appended in configured skill-note roots
- hidden fake-click targets are downgraded where deterministic
- no file-format normalization occurs

- [ ] **Step 4: Verify the fixture diff**

Use a file diff or git status in the fixture environment.

Expected:

- no forbidden-zone files changed
- no report-only files changed
- no non-markdown files changed
- only approved graph-fixable markdown notes changed

## Final Verification

- [ ] Run the full skill-local test suite:

`pytest $HOME/.agents/skills/obsidian-this/tests -v`

Expected: all PASS

- [ ] Run `init` in a generic fixture repo:

`python $HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py init --repo $HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo`

Expected:

- config created
- proposals are visible
- no content files rewritten yet

- [ ] Run `check` in the configured fixture repo:

`python $HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py check --repo $HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo`

Expected:

- findings grouped clearly
- forbidden and report-only boundaries visible
- normalization candidates remain report-only

- [ ] Run `fix` in the configured fixture repo:

`python $HOME/.agents/skills/obsidian-this/scripts/obsidian_this.py fix --repo $HOME/.agents/skills/obsidian-this/tests/fixtures/generic-repo`

Expected:

- only deterministic graph fixes
- no format normalization
- no forbidden/report-only changes

## Notes for the Implementer

- Keep the framework agent-agnostic. Codex-specific files can exist as wrappers, but the real execution surface must remain the neutral script plus repo-local config.
- Keep the skill portable. No Bastelschachtel-specific roots, tags, or paths inside runtime logic.
- Keep config explicit. Active behavior should come from config, not fresh heuristics after `init`.
- Keep `init` heuristic, but keep `check` and `fix` config-driven.
- Keep repo targeting explicit in verification and fixture runs. Do not rely on the current working directory by accident.
- Keep titleless-note handling conservative: report ambiguity, do not invent titles or top-tag placement.
- Keep format normalization out of `fix` in v1.
- Keep hidden or non-clickable targets as plain paths, never fake clickable notes.
- Keep the repo lesson small and inspectable in `.obsidian-this/config.json`.

Plan complete and saved to `docs/superpowers/plans/2026-03-29-obsidian-this-portable-skill-implementation-plan.md`. Ready to execute?
