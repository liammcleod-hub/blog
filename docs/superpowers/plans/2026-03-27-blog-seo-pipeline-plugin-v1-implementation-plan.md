# Blog SEO Pipeline Plugin V1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a repo-local `blog-seo-pipeline` plugin v1 that discovers Bastelschachtel content-job state from local and external artifacts, selects the correct mode, renders canonical local outputs, and establishes the first base-plus-family template system.

**Architecture:** The implementation should create a repo-local plugin under `plugins/blog-seo-pipeline/` with a thin command entrypoint, a discovery/normalization core, a mode selector, a template renderer, and a controlled template-learning loop. The plugin remains read-only against external sources, writes only to local job folders and plugin-owned template files, and explicitly scopes itself to single-job execution.

**Tech Stack:** Local Codex plugin manifest, plugin-local scripts, plugin-owned Markdown templates, repo docs under `docs/reference/retool/` and `docs/reference/content-pipeline/`, content-job artifacts under `output/content-jobs/`, the existing compatibility skeleton under `output/content-jobs/_template/`, and test fixtures in a plugin-local test directory.

---

## File Structure

This plan assumes the plugin will be repo-local and live at:

- `plugins/blog-seo-pipeline/`

Planned file map:

- Create: `plugins/blog-seo-pipeline/.codex-plugin/plugin.json`
  Responsibility: plugin manifest and command exposure.
- Create: `plugins/blog-seo-pipeline/README.md`
  Responsibility: plugin operator reference and local development notes.
- Create: `plugins/blog-seo-pipeline/scripts/blog_me_this.py`
  Responsibility: primary command entrypoint for `blog me this`.
- Create: `plugins/blog-seo-pipeline/scripts/discovery.py`
  Responsibility: external/local artifact lookup and state assembly.
- Create: `plugins/blog-seo-pipeline/scripts/job_state.py`
  Responsibility: normalized job-state model and inference helpers.
- Create: `plugins/blog-seo-pipeline/scripts/mode_selection.py`
  Responsibility: choose `qa-article`, `revise-article`, or `audit-brief`.
- Create: `plugins/blog-seo-pipeline/scripts/family_classification.py`
  Responsibility: classify `deep-dive-guide`, `product-comparison`, or `curation-listicle`.
- Create: `plugins/blog-seo-pipeline/scripts/analysis_engine.py`
  Responsibility: evaluate dossier, brief, selected products, and article content into structured QA findings.
- Create: `plugins/blog-seo-pipeline/scripts/revision_engine.py`
  Responsibility: generate revised article content using family rules, mode, and structured analysis output.
- Create: `plugins/blog-seo-pipeline/scripts/render_outputs.py`
  Responsibility: render `qa-report.md` and `revision-plan.md` from templates.
- Create: `plugins/blog-seo-pipeline/scripts/revision_writer.py`
  Responsibility: write revised article HTML when the mode requires it.
- Create: `plugins/blog-seo-pipeline/scripts/external_sources.py`
  Responsibility: define the read-only external fetch adapter boundary for Retool-backed artifact lookup.
- Create: `plugins/blog-seo-pipeline/scripts/template_learning.py`
  Responsibility: derive proposed template deltas from completed runs.
- Create: `plugins/blog-seo-pipeline/scripts/template_seed.py`
  Responsibility: inspect latest job folders and produce initial canonical templates.
- Create: `plugins/blog-seo-pipeline/templates/base/qa-report.plugin-base.tmpl`
  Responsibility: canonical base QA output.
- Create: `plugins/blog-seo-pipeline/templates/base/revision-plan.plugin-base.tmpl`
  Responsibility: canonical base revision-plan output.
- Create: `plugins/blog-seo-pipeline/templates/families/deep-dive-guide.plugin-family.tmpl`
  Responsibility: deep-dive overlay rules.
- Create: `plugins/blog-seo-pipeline/templates/families/product-comparison.plugin-family.tmpl`
  Responsibility: comparison overlay rules.
- Create: `plugins/blog-seo-pipeline/templates/families/curation-listicle.plugin-family.tmpl`
  Responsibility: listicle overlay rules.
- Create: `plugins/blog-seo-pipeline/tests/fixtures/`
  Responsibility: fixed content-job bundles and sample Retool-derived payloads.
- Create: `plugins/blog-seo-pipeline/tests/test_discovery.py`
  Responsibility: artifact discovery and normalization tests.
- Create: `plugins/blog-seo-pipeline/tests/test_mode_selection.py`
  Responsibility: mode selection tests.
- Create: `plugins/blog-seo-pipeline/tests/test_family_classification.py`
  Responsibility: family selection tests.
- Create: `plugins/blog-seo-pipeline/tests/test_analysis_engine.py`
  Responsibility: structured QA finding generation tests.
- Create: `plugins/blog-seo-pipeline/tests/test_revision_engine.py`
  Responsibility: revised article generation tests.
- Create: `plugins/blog-seo-pipeline/tests/test_render_outputs.py`
  Responsibility: template-driven output rendering tests.
- Create: `plugins/blog-seo-pipeline/tests/test_template_learning.py`
  Responsibility: learning-loop proposal tests.
- Modify: `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-v1-design.md`
  Responsibility: note implementation status or clarifications only if needed.
- Optionally create later: `.agents/plugins/marketplace.json`
  Responsibility: repo marketplace registration if you want the plugin to appear in Codex UI ordering.

Canonical manifest reference:

- `C:\Users\Hp\.codex\skills\.system\plugin-creator\references\plugin-json-spec.md`

## Chunk 1: Plugin Scaffold and Command Boundary

### Task 1: Create the plugin scaffold

**Files:**
- Create: `plugins/blog-seo-pipeline/.codex-plugin/plugin.json`
- Create: `plugins/blog-seo-pipeline/README.md`

- [ ] **Step 1: Create the plugin directory skeleton**

Create:

- `plugins/blog-seo-pipeline/`
- `plugins/blog-seo-pipeline/.codex-plugin/`
- `plugins/blog-seo-pipeline/scripts/`
- `plugins/blog-seo-pipeline/templates/base/`
- `plugins/blog-seo-pipeline/templates/families/`
- `plugins/blog-seo-pipeline/tests/fixtures/`

- [ ] **Step 2: Write the initial plugin manifest with placeholders replaced for local use**

The manifest should define:

- plugin name: `blog-seo-pipeline`
- local source path
- command entry exposure for `blog me this`
- a short description matching the v1 spec
- all required manifest schema fields from the canonical plugin manifest spec

- [ ] **Step 3: Validate the manifest shape against the plugin manifest reference**

Before proceeding, confirm the created `plugin.json` follows the exact required shape from:

- `C:\Users\Hp\.codex\skills\.system\plugin-creator\references\plugin-json-spec.md`

- [ ] **Step 4: Write the README**

Document:

- plugin purpose
- v1 scope
- supported run modes
- local-only write behavior
- where templates live

- [ ] **Step 5: Verify the scaffold exists**

Run: `Get-ChildItem -Recurse plugins/blog-seo-pipeline`

Expected: plugin root, manifest directory, scripts, templates, and tests folders all present.

- [ ] **Step 6: Commit**

```bash
git add plugins/blog-seo-pipeline
git commit -m "feat: scaffold blog seo pipeline plugin"
```

### Task 2: Implement the command entrypoint shell

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/blog_me_this.py`
- Test: `plugins/blog-seo-pipeline/tests/test_discovery.py`

- [ ] **Step 1: Write the failing test for command input parsing**

Test the minimal accepted inputs:

- latest keyword from retool
- dossier id
- local folder path
- local article path

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_discovery.py -v`

Expected: FAIL because the entrypoint/parser does not exist yet.

- [ ] **Step 3: Write minimal command parsing implementation**

The parser should produce a seed target object, not full job state.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_discovery.py -v`

Expected: PASS for parser-level cases only.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/blog_me_this.py plugins/blog-seo-pipeline/tests/test_discovery.py
git commit -m "feat: add blog me this command parser"
```

## Chunk 2: Discovery, Normalization, and Mode Logic

### Task 3: Implement normalized job-state model

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/job_state.py`
- Test: `plugins/blog-seo-pipeline/tests/test_discovery.py`

- [ ] **Step 1: Write the failing test for normalized job-state defaults**

Cover:

- required v1 fields
- reserved metadata fields
- provenance tracking
- confidence flags

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_discovery.py -v`

Expected: FAIL because `job_state.py` is missing.

- [ ] **Step 3: Write minimal normalized job-state implementation**

The model should include:

- `topic`
- `locale`
- `primary_keyword`
- `format`
- `archetype`
- `family`
- `subformat`
- `awareness_level`
- `cluster_role`
- `dossier`
- `brief`
- `selected_products`
- `article_html`
- `artifact_provenance`
- `confidence_flags`
- `mode`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_discovery.py -v`

Expected: PASS for normalization structure.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/job_state.py plugins/blog-seo-pipeline/tests/test_discovery.py
git commit -m "feat: add normalized job state model"
```

### Task 4: Implement external source adapter boundary and discovery against local and external sources

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/external_sources.py`
- Create: `plugins/blog-seo-pipeline/scripts/discovery.py`
- Test: `plugins/blog-seo-pipeline/tests/test_discovery.py`
- Create: `plugins/blog-seo-pipeline/tests/fixtures/peddigrohr-anfaenger-guide/`

- [ ] **Step 1: Build fixture bundles from existing job folders**

Create a compact fixture copied or reduced from:

- `output/content-jobs/peddigrohr-anfaenger-guide-de-at/`

Also inspect and preserve compatibility with:

- `output/content-jobs/_template/`

Include:

- `job.json`
- `brief.md`
- `research-dossier.json`
- `selected-products.json`
- `article.html` or `article-revised.html`

- [ ] **Step 2: Write failing tests for the external source adapter boundary**

Cover:

- read-only query input shape
- external adapter result shape
- explicit “not found” response
- provenance markers for externally sourced artifacts
- no write behavior under any adapter path

- [ ] **Step 3: Write failing tests for discovery precedence**

Cover:

- local folder bundle
- direct article path
- partial bundle with missing artifacts
- external-hint path that resolves through the read-only adapter
- external miss that falls back cleanly to local discovery

- [ ] **Step 4: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_discovery.py -v`

Expected: FAIL because the external adapter and discovery logic are incomplete.

- [ ] **Step 5: Write minimal external adapter and discovery implementation**

The external adapter should:

- define a stable read-only interface for external artifact lookup
- return typed result objects or explicit misses
- never write externally

Important:

- do not lock final method names yet
- the real adapter method names should be finalized only after the Retool API exists
- in v1 planning and early implementation, use provisional adapter boundaries and stable result shapes

Minimum provisional adapter contract:

- accept a typed lookup request object
- return a typed result object with:
  - `status`
  - `artifacts`
  - `provenance`
  - `errors`

The discovery implementation should:

- inspect external hints first
- inspect local job folders next
- assemble a normalized job state
- record provenance for each artifact
- avoid writing anywhere during discovery

- [ ] **Step 6: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_discovery.py -v`

Expected: PASS for adapter-boundary and local/external discovery handling.

- [ ] **Step 7: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/external_sources.py plugins/blog-seo-pipeline/scripts/discovery.py plugins/blog-seo-pipeline/tests/test_discovery.py plugins/blog-seo-pipeline/tests/fixtures
git commit -m "feat: add external adapter boundary and content job discovery"
```

### Task 5: Implement mode selection

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/mode_selection.py`
- Test: `plugins/blog-seo-pipeline/tests/test_mode_selection.py`

- [ ] **Step 1: Write failing tests for mode rules**

Cover:

- article present + no edit intent -> `qa-article`
- brief only -> `audit-brief`
- explicit edit intent -> `revise-article`
- article present alone must not auto-imply `revise-article`

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_mode_selection.py -v`

Expected: FAIL because mode selector is missing.

- [ ] **Step 3: Write minimal mode selection implementation**

Use the exact rules from:

- `repo-skills/blog-seo-pipeline/references/run-modes.md`
- `docs/reference/content-pipeline/run-modes.md`
- `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-v1-design.md`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_mode_selection.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/mode_selection.py plugins/blog-seo-pipeline/tests/test_mode_selection.py
git commit -m "feat: add deterministic mode selection"
```

### Task 6: Implement family classification

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/family_classification.py`
- Test: `plugins/blog-seo-pipeline/tests/test_family_classification.py`

- [ ] **Step 1: Write failing tests for v1 family classification**

Cover:

- deep-dive guide
- product comparison
- curation listicle

Use job-state cues such as:

- `format`
- `archetype`
- brief wording
- title patterns

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_family_classification.py -v`

Expected: FAIL because classifier is missing.

- [ ] **Step 3: Write minimal family classifier**

The classifier should:

- return one of the three canonical families
- record low-confidence cases
- avoid over-claiming when evidence is thin

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_family_classification.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/family_classification.py plugins/blog-seo-pipeline/tests/test_family_classification.py
git commit -m "feat: add v1 family classification"
```

### Task 7: Implement structured analysis engine

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/analysis_engine.py`
- Test: `plugins/blog-seo-pipeline/tests/test_analysis_engine.py`

- [ ] **Step 1: Write failing tests for structured QA analysis output**

Cover:

- dossier grounding checks
- brief alignment checks
- product-truth checks
- internal-link placement checks
- publishability and residual-risk output
- family-aware passed-check and finding generation

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_analysis_engine.py -v`

Expected: FAIL because the analysis engine does not exist yet.

- [ ] **Step 3: Write minimal analysis engine**

The engine should produce structured objects for:

- findings
- passed checks
- residual risks
- publishability status
- revision instructions

It must consume:

- normalized job state
- selected family
- selected mode

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_analysis_engine.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/analysis_engine.py plugins/blog-seo-pipeline/tests/test_analysis_engine.py
git commit -m "feat: add structured article analysis engine"
```

### Task 8: Implement revision engine

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/revision_engine.py`
- Test: `plugins/blog-seo-pipeline/tests/test_revision_engine.py`

- [ ] **Step 1: Write failing tests for revised article generation**

Cover:

- revision only runs in `revise-article`
- revision respects family expectations
- revision uses analysis output
- revision preserves commerce constraints and selected-products ceiling

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_revision_engine.py -v`

Expected: FAIL because the revision engine is missing.

- [ ] **Step 3: Write minimal revision engine**

The engine should:

- consume normalized job state + family + structured analysis output
- pass a validation layer before approving a full rewrite
- allow a full rewrite only after validation says the revision is acceptable
- avoid inventing unsupported product claims

The validation layer should at minimum confirm:

- family fit remains intact
- product-truth ceiling is respected
- brand voice is still in bounds
- the revised draft still satisfies the selected mode and article purpose

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_revision_engine.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/revision_engine.py plugins/blog-seo-pipeline/tests/test_revision_engine.py
git commit -m "feat: add article revision engine"
```

## Chunk 3: Templates, Rendering, and Learning Loop

### Task 9: Seed initial canonical templates

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/template_seed.py`
- Create: `plugins/blog-seo-pipeline/templates/base/qa-report.md.tmpl`
- Create: `plugins/blog-seo-pipeline/templates/base/revision-plan.md.tmpl`
- Create: `plugins/blog-seo-pipeline/templates/families/deep-dive-guide.md.tmpl`
- Create: `plugins/blog-seo-pipeline/templates/families/product-comparison.md.tmpl`
- Create: `plugins/blog-seo-pipeline/templates/families/curation-listicle.md.tmpl`

- [ ] **Step 1: Inspect the latest content-job folders**

Read from:

- `output/content-jobs/`
- `output/content-jobs/_template/`
- `docs/reference/content-pipeline/qa-report-template.md`
- `docs/reference/content-pipeline/revision-plan-template.md`

Use the newest finished job folders as the calibration set for template shape, and use `_template/` plus the content-pipeline template docs as seed and compatibility baselines.

The goal is not to copy them verbatim.
The goal is to create plugin-owned enhanced templates that remain compatible with the existing repo workflow.

- [ ] **Step 2: Write the base templates**

The base QA template should inherit the minimum structure from:

- `docs/reference/content-pipeline/qa-report-template.md`

That means it must preserve these sections at minimum:

- findings
- coverage checks
- priority fixes
- residual risks

The plugin-owned enhanced base QA template may then add:

- publishability
- structured passed-check detail
- validation metadata
- plugin-specific quality-layer fields

The base revision-plan template should inherit the minimum structure from:

- `docs/reference/content-pipeline/revision-plan-template.md`

That means it must preserve these sections at minimum:

- objective
- required fixes
- recommended improvements
- edit strategy

The plugin-owned enhanced base revision-plan template may then add:

- validation gate notes
- family-specific execution notes
- plugin-owned metadata fields

- [ ] **Step 3: Write the three family overlays**

Each overlay should define:

- required sections
- family-specific risk checks
- family-specific SEO/commercial expectations

- [ ] **Step 4: Add a seed script to validate template presence**

The script does not need full smart generation in the first iteration.
It can initially validate that the canonical templates exist and report the calibration sources used.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/template_seed.py plugins/blog-seo-pipeline/templates
git commit -m "feat: add canonical base and family templates"
```

### Task 10: Implement template rendering for QA and revision plan outputs

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/render_outputs.py`
- Test: `plugins/blog-seo-pipeline/tests/test_render_outputs.py`

- [ ] **Step 1: Write failing tests for QA report rendering**

Cover:

- base sections always present
- family overlay content injected
- publishability line always rendered

- [ ] **Step 2: Write failing tests for revision-plan rendering**

Cover:

- objective present
- required fixes present
- recommended improvements present
- family overlay notes injected where applicable

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_render_outputs.py -v`

Expected: FAIL because rendering logic is missing.

- [ ] **Step 4: Write minimal renderer**

The renderer should:

- take structured analysis output
- merge base template + family overlay
- write `qa-report.md`
- write `revision-plan.md`

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_render_outputs.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/render_outputs.py plugins/blog-seo-pipeline/tests/test_render_outputs.py
git commit -m "feat: add template-driven output rendering"
```

### Task 11: Implement revised article writer for `revise-article`

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/revision_writer.py`
- Test: `plugins/blog-seo-pipeline/tests/test_render_outputs.py`

- [ ] **Step 1: Write the failing test for revised article output pathing**

Cover:

- revised HTML goes to the target job folder
- QA modes do not write revised HTML

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_render_outputs.py -v`

Expected: FAIL because the revision writer is missing.

- [ ] **Step 3: Write minimal revision writer**

The writer should:

- accept revised article content
- write the output only when the mode is `revise-article`
- preserve local job-folder conventions

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_render_outputs.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/revision_writer.py plugins/blog-seo-pipeline/tests/test_render_outputs.py
git commit -m "feat: add revised article writer"
```

### Task 12: Implement template-learning proposal generator

**Files:**
- Create: `plugins/blog-seo-pipeline/scripts/template_learning.py`
- Test: `plugins/blog-seo-pipeline/tests/test_template_learning.py`

- [ ] **Step 1: Write failing tests for learning-loop proposals**

Cover:

- classify finished job by family
- compare job outputs against current templates
- produce structured proposal objects
- never auto-rewrite templates in ordinary runs

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest plugins/blog-seo-pipeline/tests/test_template_learning.py -v`

Expected: FAIL because learning-loop logic is missing.

- [ ] **Step 3: Write minimal proposal generator**

Proposal objects should support shapes such as:

- promote section to base
- promote section to family overlay
- reject as job-specific

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest plugins/blog-seo-pipeline/tests/test_template_learning.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline/scripts/template_learning.py plugins/blog-seo-pipeline/tests/test_template_learning.py
git commit -m "feat: add template learning proposal system"
```

### Task 13: Wire the end-to-end command path

**Files:**
- Modify: `plugins/blog-seo-pipeline/scripts/blog_me_this.py`
- Test: `plugins/blog-seo-pipeline/tests/test_discovery.py`
- Test: `plugins/blog-seo-pipeline/tests/test_mode_selection.py`
- Test: `plugins/blog-seo-pipeline/tests/test_family_classification.py`
- Test: `plugins/blog-seo-pipeline/tests/test_analysis_engine.py`
- Test: `plugins/blog-seo-pipeline/tests/test_revision_engine.py`
- Test: `plugins/blog-seo-pipeline/tests/test_render_outputs.py`
- Test: `plugins/blog-seo-pipeline/tests/test_template_learning.py`

- [ ] **Step 1: Add end-to-end orchestration in the entrypoint**

The command path should:

1. parse seed input
2. discover artifacts
3. normalize state
4. classify family
5. choose mode
6. analyze dossier/brief/article into structured findings
7. render outputs
8. optionally generate revised article content
9. optionally write revised HTML
10. generate template-learning proposals

- [ ] **Step 2: Run the focused test suite**

Run:

`pytest plugins/blog-seo-pipeline/tests -v`

Expected: PASS.

- [ ] **Step 3: Run one fixture-backed dry run**

Use the peddigrohr fixture and confirm:

- job state resolves
- mode resolves correctly
- outputs render to the expected local target

- [ ] **Step 4: Document the dry-run invocation in the plugin README**

- [ ] **Step 5: Commit**

```bash
git add plugins/blog-seo-pipeline
git commit -m "feat: wire blog seo pipeline plugin v1 flow"
```

## Final Verification

- [ ] Run the full plugin-local test suite:

`pytest plugins/blog-seo-pipeline/tests -v`

Expected: all PASS

- [ ] Run a manual fixture-backed dry run through `blog me this`

Expected:

- discovery works
- mode is correct
- family is classified
- `qa-report.md` and `revision-plan.md` are written from templates
- no external write occurs

- [ ] Confirm template proposal output is generated but not silently promoted for ordinary runs

## Notes for the Implementer

- Do not build cluster generation in this plan.
- Do not add Retool write-back.
- Do not operationalize full `subformat`, `awareness_level`, or `cluster_role` behavior yet.
- Keep those fields in the data model, but do not let them expand scope.
- Favor smaller files with one clear responsibility.
- Prefer deterministic logic over clever prompt behavior.

Plan complete and saved to `docs/superpowers/plans/2026-03-27-blog-seo-pipeline-plugin-v1-implementation-plan.md`. Ready to execute?
