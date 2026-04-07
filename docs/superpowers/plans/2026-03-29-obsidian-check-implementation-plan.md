# Obsidian Check Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement an `obsidian-check` maintenance skill that audits Bastelschachtel wikilink hygiene, reports skill-library link health, and only applies deterministic fixes in the approved Bastelschachtel zones.

**Architecture:** The implementation should be a small repo-local maintenance workflow with a deterministic scanner, a scope classifier, a report formatter, and a tightly constrained fix engine. The scanner must treat Bastelschachtel wikilink zones, visible skill-library trees, and forbidden artifact zones as separate domains with different permissions. `check` is read-only everywhere, and `check --fix` may only touch the approved Bastelschachtel markdown files.

**Tech Stack:** Markdown files under `docs/`, `.codex/memories/`, `.agents/`, `output/content-jobs/README.md`, and `repo-skills/marketing-library/`; PowerShell or Python for the scanner; repo-local tests; `rg` for verification.

---

## Rule Model

Implementation should encode three link classes:

- `visible_note_target`
  Meaning: visible vault markdown note intended for Obsidian navigation. Expected syntax: Obsidian wikilink.
- `hidden_or_nonclickable_target`
  Meaning: hidden dotfolder path or other target that should not pretend to be clickable in Obsidian. Expected syntax: plain code path or plain text path.
- `reference_syntax`
  Meaning: implementation/spec mention of a path or command rather than navigation. Expected syntax: plain code formatting is acceptable.

The implementation must apply this model only in repo-facing navigation docs and approved Bastelschachtel fixable zones, not blindly across every markdown file in the repo.

## File Structure

Planned file map:

- Create: `.agents/skills/obsidian-check/`
  Responsibility: skill root.
- Create: `.agents/skills/obsidian-check/SKILL.md`
  Responsibility: user-facing skill contract, run modes, and operating instructions.
- Create: `.agents/skills/obsidian-check/scripts/obsidian_check.py`
  Responsibility: main entrypoint for `check` and `check --fix`.
- Create: `.agents/skills/obsidian-check/scripts/scope.py`
  Responsibility: classify files into Bastelschachtel fixable zones, skill-library report-only zones, forbidden report-only zones, and out-of-scope areas.
- Create: `.agents/skills/obsidian-check/scripts/discovery.py`
  Responsibility: discover candidate markdown files in approved locations.
- Create: `.agents/skills/obsidian-check/scripts/config.py`
  Responsibility: hold explicit approved roots, forbidden-zone roots, report-only skill-library root configuration, and an explicit `repo_facing_navigation_docs` list for link-class enforcement.
- Create: `.agents/skills/obsidian-check/scripts/link_parser.py`
  Responsibility: extract wikilinks, markdown links, and relative link targets.
- Create: `.agents/skills/obsidian-check/scripts/bastel_checks.py`
  Responsibility: Bastelschachtel graph-hygiene checks.
- Create: `.agents/skills/obsidian-check/scripts/skill_library_checks.py`
  Responsibility: report-only skill-library link-health checks.
- Create: `.agents/skills/obsidian-check/scripts/forbidden_zone_scan.py`
  Responsibility: read-only scan for accidental wikilinks in forbidden artifact locations.
- Create: `.agents/skills/obsidian-check/scripts/fix_engine.py`
  Responsibility: deterministic Bastelschachtel-only auto-fixes.
- Create: `.agents/skills/obsidian-check/scripts/reporting.py`
  Responsibility: structured output rendering for `Graph Hygiene`, `Skill Library Link Health`, and `Auto-Fix Summary`.
- Create: `.agents/skills/obsidian-check/tests/test_scope.py`
  Responsibility: scope and permission tests.
- Create: `.agents/skills/obsidian-check/tests/test_link_parser.py`
  Responsibility: link extraction and target resolution tests.
- Create: `.agents/skills/obsidian-check/tests/test_bastel_checks.py`
  Responsibility: Bastelschachtel hygiene rule tests.
- Create: `.agents/skills/obsidian-check/tests/test_skill_library_checks.py`
  Responsibility: report-only skill-library audit tests.
- Create: `.agents/skills/obsidian-check/tests/test_forbidden_zone_scan.py`
  Responsibility: forbidden-zone scan tests.
- Create: `.agents/skills/obsidian-check/tests/test_fix_engine.py`
  Responsibility: deterministic auto-fix safety tests.
- Create: `.agents/skills/obsidian-check/tests/test_reporting.py`
  Responsibility: report output shape tests.
- Create: `.agents/skills/obsidian-check/tests/fixtures/`
  Responsibility: small markdown fixture trees for good, broken, and ambiguous cases.

Optional later file:

- Create later if needed: `.agents/skills/obsidian-check/README.md`
  Responsibility: maintainer reference only if `SKILL.md` becomes too crowded.

## Chunk 1: Skill Scaffold And Scope Boundaries

### Task 1: Scaffold the skill and freeze the scope contract

**Files:**
- Create: `.agents/skills/obsidian-check/SKILL.md`
- Create: `.agents/skills/obsidian-check/scripts/obsidian_check.py`
- Create: `.agents/skills/obsidian-check/scripts/scope.py`
- Create: `.agents/skills/obsidian-check/scripts/config.py`
- Test: `.agents/skills/obsidian-check/tests/test_scope.py`

- [ ] **Step 1: Create the skill directory skeleton**

Create:

- `.agents/skills/obsidian-check/`
- `.agents/skills/obsidian-check/scripts/`
- `.agents/skills/obsidian-check/tests/`
- `.agents/skills/obsidian-check/tests/fixtures/`

- [ ] **Step 2: Write the initial `SKILL.md`**

Document:

- `check`
- `check --fix`
- Bastelschachtel auto-fix zones
- skill-library report-only zones
- explicit never-touch areas such as `output/content-jobs/_template/`

- [ ] **Step 3: Write the failing scope tests**

Cover:

- approved fixable paths:
  - `docs/seo/...`
  - `docs/customer reviews/...`
  - `docs/superpowers/specs/...`
  - `.codex/memories/bastelschachtel/...`
  - `.agents/product-marketing-context.md`
  - `docs/reference/skill-guides/blogs.md`
  - `docs/reference/skill-guides/README.md`
  - `output/content-jobs/README.md`
- report-only skill-library paths:
  - `repo-skills/marketing-library/...`
  - one additional configured visible skill-library root fixture
- forbidden paths:
  - `output/content-jobs/_template/...`
  - copied/generated job bundle notes
- explicit repo-facing navigation docs:
  - approved entrypoint `README.md` notes
  - configured stable navigation notes such as `docs/reference/skill-guides/blogs.md`

- [ ] **Step 4: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_scope.py -v`

Expected: FAIL because the scope classifier does not exist yet.

- [ ] **Step 5: Write minimal scope classifier implementation**

The classifier must return one of:

- `bastel_fixable`
- `skill_library_report_only`
- `forbidden_report_only`
- `out_of_scope`

The config layer must also expose an explicit `repo_facing_navigation_docs` list so link-class enforcement does not rely on runtime heuristics.

- [ ] **Step 6: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_scope.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/obsidian-check
git commit -m "feat: scaffold obsidian check skill"
```

### Task 2: Implement deterministic file discovery

**Files:**
- Create: `.agents/skills/obsidian-check/scripts/discovery.py`
- Create: `.agents/skills/obsidian-check/scripts/forbidden_zone_scan.py`
- Test: `.agents/skills/obsidian-check/tests/test_scope.py`
- Test: `.agents/skills/obsidian-check/tests/test_forbidden_zone_scan.py`

- [ ] **Step 1: Write the failing tests for discovery**

Cover:

- Bastelschachtel approved zones are discovered
- configured visible skill-library trees are discovered
- forbidden artifact paths are excluded from normal discovery
- forbidden artifact paths are discovered by the separate read-only forbidden-zone scan
- only `.md` and `SKILL.md` are surfaced

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_scope.py -v`

Expected: FAIL because discovery is missing.

- [ ] **Step 3: Write minimal discovery implementation**

The discovery layer should:

- walk only the approved roots
- walk configured report-only skill-library roots
- feed results through the scope classifier
- never infer new roots from random folders

Repo-facing navigation-doc enforcement should consume the explicit configured `repo_facing_navigation_docs` list plus approved entrypoint docs, not freeform inference from arbitrary note structure.

The forbidden-zone scan should:

- walk only the configured forbidden roots
- remain read-only in all modes
- surface markdown files for accidental-wikilink checks without ever marking them fixable

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_scope.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check/scripts/config.py .agents/skills/obsidian-check/scripts/discovery.py .agents/skills/obsidian-check/scripts/forbidden_zone_scan.py .agents/skills/obsidian-check/tests/test_scope.py .agents/skills/obsidian-check/tests/test_forbidden_zone_scan.py
git commit -m "feat: add obsidian check file discovery"
```

## Chunk 2: Parsing And Read-Only Reporting

### Task 3: Implement link parsing and target resolution

**Files:**
- Create: `.agents/skills/obsidian-check/scripts/link_parser.py`
- Test: `.agents/skills/obsidian-check/tests/test_link_parser.py`

- [ ] **Step 1: Write the failing parser tests**

Cover:

- Obsidian wikilinks:
  - `[[target-note]]`
  - `[[path/to/target-note]]`
  - `[[path/to/target-note#Heading]]`
  - `[[path/to/target-note|Display Text]]`
- markdown links:
  - `[tools registry](../../tools/REGISTRY.md)`
  - `[ad-copy-templates.md](references/ad-copy-templates.md)`
- relative target resolution from the real file path

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_link_parser.py -v`

Expected: FAIL because the parser is missing.

- [ ] **Step 3: Write minimal parser implementation**

The parser should output structured link items with:

- source file
- link type
- raw target
- normalized resolved target when applicable

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_link_parser.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check/scripts/link_parser.py .agents/skills/obsidian-check/tests/test_link_parser.py
git commit -m "feat: add obsidian check link parser"
```

### Task 4: Implement Bastelschachtel report-only checks

**Files:**
- Create: `.agents/skills/obsidian-check/scripts/bastel_checks.py`
- Test: `.agents/skills/obsidian-check/tests/test_bastel_checks.py`

- [ ] **Step 1: Write the failing Bastelschachtel check tests**

Cover:

- missing folder `README.md`
- missing upward link to local `README.md`
- entrypoint doc missing internal wikilinks
- entrypoint doc using bare/ambiguous link where path-qualified is expected
- repo-facing navigation doc using plain code formatting for a visible note target that should be a wikilink
- repo-facing navigation doc using clickable note syntax for a hidden `.agents/...` target
- isolated approved note with no meaningful internal links

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_bastel_checks.py -v`

Expected: FAIL because the Bastelschachtel checks do not exist.

- [ ] **Step 3: Write minimal Bastelschachtel checks**

These checks should produce structured findings only and no fixes yet. Forbidden-zone findings should come from the separate read-only forbidden-zone scan and then be rendered under `Graph Hygiene`.

The Bastelschachtel checks should also classify link-shape mismatches in repo-facing navigation docs:

- visible note target written as plain code path
- hidden `.agents/...` or other non-clickable target written as wikilink
- absolute filesystem markdown links used where Obsidian wikilinks or plain paths are expected

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_bastel_checks.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check/scripts/bastel_checks.py .agents/skills/obsidian-check/tests/test_bastel_checks.py
git commit -m "feat: add Bastelschachtel wikilink hygiene checks"
```

### Task 5: Implement report-only skill-library checks

**Files:**
- Create: `.agents/skills/obsidian-check/scripts/skill_library_checks.py`
- Test: `.agents/skills/obsidian-check/tests/test_skill_library_checks.py`

- [ ] **Step 1: Write the failing skill-library audit tests**

Cover:

- broken relative markdown links in `SKILL.md`
- structural missing-tools cases like `../../tools/REGISTRY.md`
- healthy local `references/*.md` links
- skill notes with no Obsidian wikilinks reported as opportunities

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_skill_library_checks.py -v`

Expected: FAIL because the skill-library checks are missing.

- [ ] **Step 3: Write minimal skill-library check implementation**

The implementation should:

- audit configured visible skill-library roots only
- never classify findings from those trees as auto-fixable
- group structural mirror issues separately from isolated bad links
- prove via tests that newly added configured skill-library roots also stay report-only

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_skill_library_checks.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check/scripts/skill_library_checks.py .agents/skills/obsidian-check/tests/test_skill_library_checks.py
git commit -m "feat: add report-only skill library link audits"
```

### Task 6: Implement the report formatter

**Files:**
- Create: `.agents/skills/obsidian-check/scripts/reporting.py`
- Test: `.agents/skills/obsidian-check/tests/test_reporting.py`
- Test: `.agents/skills/obsidian-check/tests/test_forbidden_zone_scan.py`

- [ ] **Step 1: Write the failing reporting tests**

Cover:

- `Graph Hygiene` section
- `Skill Library Link Health` section
- forbidden-zone artifact findings rendered inside `Graph Hygiene`
- optional `Auto-Fix Summary` section only when fixes exist
- clean no-op output when no issues are found

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_reporting.py -v`

Expected: FAIL because reporting is missing.

- [ ] **Step 3: Write minimal report formatter**

The formatter should be stable and easy to scan, not verbose.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_reporting.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check/scripts/reporting.py .agents/skills/obsidian-check/tests/test_reporting.py
git commit -m "feat: add obsidian check reporting"
```

## Chunk 3: Safe Auto-Fix Engine And End-To-End Wiring

### Task 7: Implement Bastelschachtel-only deterministic fixes

**Files:**
- Create: `.agents/skills/obsidian-check/scripts/fix_engine.py`
- Test: `.agents/skills/obsidian-check/tests/test_fix_engine.py`

- [ ] **Step 1: Write the failing fix-engine tests**

Cover:

- add missing upward link to local `README.md`
- add minimal `Related Docs` block in deterministic cases
- normalize entrypoint links to path-qualified wikilinks
- rewrite hidden `.agents/...` fake clickable targets to deterministic plain code paths in approved fixable docs
- reject fixes in:
  - `repo-skills/marketing-library`
  - `output/content-jobs/_template/`
  - copied/generated job artifacts
- reject ambiguous relationship cases

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/skills/obsidian-check/tests/test_fix_engine.py -v`

Expected: FAIL because fix logic is missing.

- [ ] **Step 3: Write minimal fix engine**

The engine should:

- only touch files classified as `bastel_fixable`
- apply one small edit per finding
- return touched files for re-verification
- never convert spec/plan reference syntax just because it looks like a path

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/skills/obsidian-check/tests/test_fix_engine.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check/scripts/fix_engine.py .agents/skills/obsidian-check/tests/test_fix_engine.py
git commit -m "feat: add safe Bastelschachtel wikilink fixes"
```

### Task 8: Wire the end-to-end `check` and `check --fix` flow

**Files:**
- Modify: `.agents/skills/obsidian-check/scripts/obsidian_check.py`
- Test: `.agents/skills/obsidian-check/tests/test_scope.py`
- Test: `.agents/skills/obsidian-check/tests/test_link_parser.py`
- Test: `.agents/skills/obsidian-check/tests/test_bastel_checks.py`
- Test: `.agents/skills/obsidian-check/tests/test_skill_library_checks.py`
- Test: `.agents/skills/obsidian-check/tests/test_forbidden_zone_scan.py`
- Test: `.agents/skills/obsidian-check/tests/test_fix_engine.py`
- Test: `.agents/skills/obsidian-check/tests/test_reporting.py`

- [ ] **Step 1: Add command-line mode parsing**

Support:

- `check`
- `check --fix`

- [ ] **Step 2: Wire the read-only flow**

The `check` path should:

1. discover files
2. classify scope
3. parse links
4. run Bastelschachtel checks
5. run skill-library checks
6. run forbidden-zone read-only scan
7. print the report

- [ ] **Step 3: Wire the constrained fix flow**

The `check --fix` path should:

1. run the same discovery and checks
2. apply allowed fixes in Bastelschachtel zones only
3. re-run relevant checks on touched files
4. re-run forbidden-zone and skill-library reporting without applying fixes there
5. print the report with `Auto-Fix Summary`

- [ ] **Step 4: Run the focused test suite**

Run:

`pytest .agents/skills/obsidian-check/tests -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/obsidian-check
git commit -m "feat: wire obsidian check end-to-end flow"
```

### Task 9: Run fixture-backed smoke tests against the live repo

**Files:**
- Modify: none unless a real bug is discovered

- [ ] **Step 1: Capture a baseline for configured forbidden and report-only zones**

Run:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check --print-verification-roots`

Then record:

- configured `skill_library_roots`
- configured `forbidden_roots`
- the current changed-file baseline for those roots

Expected:

- baseline is recorded before live smoke tests
- pre-existing dirt is separated from anything introduced by `obsidian-check`
- the same configured roots drive both scanning and smoke verification

- [ ] **Step 2: Run read-only mode against the live repo**

Run:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check`

Expected:

- reports Bastelschachtel graph hygiene
- reports skill-library link health
- reports forbidden-zone artifact findings if any exist
- reports wrong link-class usage in repo-facing navigation docs when present
- no file edits occur

- [ ] **Step 3: Run fix mode against the live repo**

Run:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check --fix`

Expected:

- only approved Bastelschachtel files may be touched
- skill-library findings remain report-only
- forbidden zones remain untouched
- hidden `.agents/...` fake-click targets in approved fixable docs may be downgraded to plain paths when deterministic

- [ ] **Step 4: Verify touched-file scope after fix mode against the baseline**

Run:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check --print-verification-roots`

Then compare the post-run changed-file set against the recorded baseline for:

- all configured `skill_library_roots`
- all configured `forbidden_roots`
- approved Bastelschachtel fixable roots

Expected:

- no new files were added under any configured skill-library root relative to the recorded baseline
- no new files were added under any configured forbidden root relative to the recorded baseline
- only approved Bastelschachtel markdown files were added to the changed-file set by `obsidian-check`

- [ ] **Step 5: Commit only if a legitimate implementation bug needed fixing**

If live smoke testing exposed a real implementation bug:

```bash
git add .agents/skills/obsidian-check
git commit -m "fix: tighten obsidian check live repo behavior"
```

## Final Verification

- [ ] Run the full skill-local test suite:

`pytest .agents/skills/obsidian-check/tests -v`

Expected: all PASS

- [ ] Run live read-only mode:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check`

Expected:

- no edits
- two report domains visible
- clear no-op messaging if clean

- [ ] Run live constrained fix mode:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check --fix`

Expected:

- fixes only deterministic Bastelschachtel issues
- re-verifies touched files
- still treats all skill-library trees as report-only

- [ ] Confirm forbidden zones remain untouched:

Run:

`python .agents/skills/obsidian-check/scripts/obsidian_check.py check --print-verification-roots`

Then compare the final changed-file set against the recorded baseline for configured report-only and forbidden roots.

Expected:

- no new changed files in configured report-only skill-library trees relative to the recorded baseline
- no new changed files in configured forbidden artifact locations relative to the recorded baseline

## Notes for the Implementer

- Keep the implementation deterministic. This is not an AI doc improver.
- Prefer explicit config or hardcoded approved roots over clever discovery.
- Keep skill-library roots explicit and extensible so future visible skill trees remain report-only by configuration, not by accident.
- Make smoke verification consume the same configured root lists as the scanner so config and verification cannot drift apart.
- Group structurally identical skill-library failures to reduce report noise.
- Keep forbidden artifact scanning separate from normal fixable discovery.
- Keep link-class enforcement limited to repo-facing navigation docs and approved fixable Bastelschachtel notes so specs and plans can still mention paths as plain code when they are describing implementation rather than navigation.
- Bastelschachtel fixes should be tiny and local.
- If a relationship is ambiguous, report it and skip the fix.
- `check --fix` should remain working-tree local and should never stage files automatically.

Plan complete and saved to `docs/superpowers/plans/2026-03-29-obsidian-check-implementation-plan.md`. Ready to execute?
