# Repo Wikilink Incorporation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add simple, selective Obsidian wikilinks across the agreed Bastelschachtel target folders and files so the important notes reference each other cleanly.

**Architecture:** This rollout is doc-only and additive. Start by making or tightening folder entrypoints, then add upward and lateral wikilinks in the most important child notes, then finish with artifact/template notes and a repo-wide verification pass. Do not introduce new metadata systems, traversal rules, or broad content rewrites while implementing this plan.

**Tech Stack:** Markdown files under `docs/`, `.codex/memories/`, `.agents/`, and `output/content-jobs/`; PowerShell; `rg` for verification; Git for small checkpoint commits.

---

## File Structure

Planned file map for this rollout:

- Create: `docs/superpowers/specs/README.md`
  Responsibility: entrypoint for the specs folder, linking the key current specs and the wikilink design spec.
- Create: `.codex/memories/bastelschachtel/README.md`
  Responsibility: folder entrypoint for Bastelschachtel memory notes, linking to the real session-start docs.
- Modify: `docs/seo/README.md`
  Responsibility: add explicit wikilinks to the highest-value SEO docs.
- Modify: `docs/customer reviews/README.md`
  Responsibility: add explicit wikilinks to the highest-value VOC docs.
- Modify: `output/content-jobs/README.md`
  Responsibility: add explicit wikilinks to the stable local template and the most relevant adjacent context.
- Modify: `docs/seo/master-article-plan-2026-03-29.md`
  Responsibility: add upward link to `docs/seo/README.md` and a few high-signal related links.
- Modify: `docs/seo/priority-category-intros-2026-03-29.md`
  Responsibility: add upward link and related SEO/VOC links.
- Modify: `docs/seo/live-seo-audit-2026-03-27.md`
  Responsibility: add upward link and related planning links.
- Modify: `docs/seo/seo-execution-checklist-2026-03-27.md`
  Responsibility: add upward link and related planning links.
- Modify: `docs/customer reviews/category-voc-priority-map.md`
  Responsibility: add upward link and related VOC/SEO links.
- Modify: `docs/customer reviews/voc-product-family-bank.md`
  Responsibility: add upward link and related VOC/context links.
- Modify: `docs/customer reviews/voc-split-bank.md`
  Responsibility: add upward link and related VOC/context links.
- Modify: `.agents/product-marketing-context.md`
  Responsibility: add a small related-docs block linking back to the key entrypoints and strategy docs it depends on.
- Modify: `.codex/memories/bastelschachtel/START-HERE.md`
  Responsibility: link to the new local README without breaking the current session-start behavior.
- Modify: `.codex/memories/bastelschachtel/CURRENT-STATE.md`
  Responsibility: add upward link and links to the relevant folder entrypoints and skill guide.
- Modify: `.codex/memories/bastelschachtel/WORKFLOWS.md`
  Responsibility: add upward link and related workflow/context links.

Files intentionally out of scope for this implementation pass:

- raw exports such as `.csv`, `.txt`, `.docx`, `.json`, and `.html`
- copied or generated workflow artifacts under `output/content-jobs/_template/` and job-bundle child files
- non-target folders outside the approved wikilink spec
- broad filename renames or structural moves

## Chunk 1: Entrypoints And Local Hubs

### Task 0: Record the start ref for later verification

**Files:**
- Modify: none

- [ ] **Step 1: Record the implementation start ref**

Run: `git rev-parse HEAD`

Save the result as `<start-ref>` for the final verification steps in this plan.

- [ ] **Step 2: Confirm the planned file list before editing**

Run:

`git diff --name-only`

Expected: review the current dirty worktree before starting so later verification can distinguish planned wikilink edits from unrelated local changes.

### Task 1: Create the missing entrypoint for `docs/superpowers/specs/`

**Files:**
- Create: `docs/superpowers/specs/README.md`
- Modify: `docs/superpowers/specs/2026-03-29-repo-wikilink-knowledge-graph-design.md`

- [ ] **Step 1: Inspect current spec filenames and decide the selective hub list**

Use these files as the initial candidate set:

- `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-design.md`
- `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-v1-design.md`
- `docs/superpowers/specs/2026-03-28-blog-seo-pipeline-next-step-reading.md`
- `docs/superpowers/specs/2026-03-28-blog-seo-pipeline-plugin-v1-current-state.md`
- `docs/superpowers/specs/2026-03-29-blog-cluster-engine-briefing-model.md`
- `docs/superpowers/specs/2026-03-29-blog-seo-pipeline-plugin-next-step-memo.md`
- `docs/superpowers/specs/2026-03-29-repo-wikilink-knowledge-graph-design.md`

- [ ] **Step 2: Create `docs/superpowers/specs/README.md`**

The README should include:

- `Purpose`
- `Key Specs`
- `Related Docs`
- only the most relevant current specs as path-qualified wikilinks

- [ ] **Step 3: Add a backlink from the wikilink design spec**

Add a small `Related Docs` or `See Also` section in:

- `docs/superpowers/specs/2026-03-29-repo-wikilink-knowledge-graph-design.md`

Include at minimum:

- `[[docs/superpowers/specs/README]]`

- [ ] **Step 4: Verify the new specs entrypoint links are present**

Run: `rg -n "\[\[" docs/superpowers/specs/README.md docs/superpowers/specs/2026-03-29-repo-wikilink-knowledge-graph-design.md`

Expected: both files show explicit wikilinks.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/README.md docs/superpowers/specs/2026-03-29-repo-wikilink-knowledge-graph-design.md
git commit -m "docs: add specs wikilink entrypoint"
```

### Task 2: Create the missing entrypoint for `.codex/memories/bastelschachtel/`

**Files:**
- Create: `.codex/memories/bastelschachtel/README.md`
- Modify: `.codex/memories/bastelschachtel/START-HERE.md`

- [ ] **Step 1: Read the current memory notes and preserve the session-start contract**

Use these files as the hub targets:

- `.codex/memories/bastelschachtel/START-HERE.md`
- `.codex/memories/bastelschachtel/CURRENT-STATE.md`
- `.codex/memories/bastelschachtel/WORKFLOWS.md`

- [ ] **Step 2: Create `.codex/memories/bastelschachtel/README.md`**

The README should:

- act as the Obsidian folder entrypoint
- link to `START-HERE.md`, `CURRENT-STATE.md`, and `WORKFLOWS.md`
- keep `START-HERE.md` as the actual session-start file

- [ ] **Step 3: Update `START-HERE.md` lightly**

Add a path-qualified wikilink to:

- `[[.codex/memories/bastelschachtel/README]]`

Do not remove the current literal startup instruction.

- [ ] **Step 4: Verify the memory entrypoint links are present**

Run: `rg -n "\[\[" .codex/memories/bastelschachtel/README.md .codex/memories/bastelschachtel/START-HERE.md`

Expected: both files show explicit wikilinks.

- [ ] **Step 5: Commit**

```bash
git add .codex/memories/bastelschachtel/README.md .codex/memories/bastelschachtel/START-HERE.md
git commit -m "docs: add Bastelschachtel memory wikilink entrypoint"
```

### Task 3: Upgrade the existing stable entrypoints

**Files:**
- Modify: `docs/seo/README.md`
- Modify: `docs/customer reviews/README.md`
- Modify: `output/content-jobs/README.md`

- [ ] **Step 1: Verify current files are mostly plain text references**

Run: `rg -n "\[\[" docs/seo/README.md "docs/customer reviews/README.md" output/content-jobs/README.md`

Expected: few or no internal wikilinks yet.

- [ ] **Step 2: Add selective path-qualified wikilinks to `docs/seo/README.md`**

Link at minimum to:

- `[[docs/seo/master-article-plan-2026-03-29|master-article-plan-2026-03-29]]`
- `[[docs/seo/priority-category-intros-2026-03-29|priority-category-intros-2026-03-29]]`
- `[[docs/seo/live-seo-audit-2026-03-27|live-seo-audit-2026-03-27]]`
- `[[docs/seo/seo-execution-checklist-2026-03-27|seo-execution-checklist-2026-03-27]]`

- [ ] **Step 3: Add selective path-qualified wikilinks to `docs/customer reviews/README.md`**

Link at minimum to:

- `[[docs/customer reviews/category-voc-priority-map|category-voc-priority-map]]`
- `[[docs/customer reviews/voc-product-family-bank|voc-product-family-bank]]`
- `[[docs/customer reviews/voc-split-bank|voc-split-bank]]`

- [ ] **Step 4: Add selective path-qualified wikilinks to `output/content-jobs/README.md`**

Link at minimum to:

- `[[output/content-jobs/_template/brief]]`
- `[[output/content-jobs/_template/qa-report]]`
- `[[output/content-jobs/_template/revision-plan]]`
- `[[docs/reference/skill-guides/blogs|Blogs]]`

- [ ] **Step 5: Verify the three entrypoints now expose real wikilinks**

Run: `rg -n "\[\[" docs/seo/README.md "docs/customer reviews/README.md" output/content-jobs/README.md`

Expected: all three files contain explicit internal wikilinks.

- [ ] **Step 6: Commit**

```bash
git add docs/seo/README.md "docs/customer reviews/README.md" output/content-jobs/README.md
git commit -m "docs: add wikilinks to Bastelschachtel entrypoints"
```

## Chunk 2: Canonical SEO, VOC, And Context Notes

### Task 4: Link the key SEO planning documents

**Files:**
- Modify: `docs/seo/master-article-plan-2026-03-29.md`
- Modify: `docs/seo/priority-category-intros-2026-03-29.md`
- Modify: `docs/seo/live-seo-audit-2026-03-27.md`
- Modify: `docs/seo/seo-execution-checklist-2026-03-27.md`

- [ ] **Step 1: Add upward links to the folder entrypoint**

Each file should gain:

- `[[docs/seo/README]]`

- [ ] **Step 2: Add a few high-signal lateral links**

Use only direct relationships, for example:

- `master-article-plan` <-> `priority-category-intros`
- `live-seo-audit` -> `master-article-plan`
- `seo-execution-checklist` -> `live-seo-audit`
- SEO files -> `[[docs/customer reviews/category-voc-priority-map|category-voc-priority-map]]` where the document explicitly depends on VOC/category priority context

- [ ] **Step 3: Verify the four SEO docs now link cleanly**

Run: `rg -n "\[\[" docs/seo/master-article-plan-2026-03-29.md docs/seo/priority-category-intros-2026-03-29.md docs/seo/live-seo-audit-2026-03-27.md docs/seo/seo-execution-checklist-2026-03-27.md`

Expected: each file contains at least one upward link and at least one meaningful related-doc link.

- [ ] **Step 4: Commit**

```bash
git add docs/seo/master-article-plan-2026-03-29.md docs/seo/priority-category-intros-2026-03-29.md docs/seo/live-seo-audit-2026-03-27.md docs/seo/seo-execution-checklist-2026-03-27.md
git commit -m "docs: wire key SEO planning notes with wikilinks"
```

### Task 5: Link the key VOC synthesis documents

**Files:**
- Modify: `docs/customer reviews/category-voc-priority-map.md`
- Modify: `docs/customer reviews/voc-product-family-bank.md`
- Modify: `docs/customer reviews/voc-split-bank.md`

- [ ] **Step 1: Add upward links to the customer reviews entrypoint**

Each file should gain:

- `[[docs/customer reviews/README]]`

- [ ] **Step 2: Add a few high-signal lateral links**

Use only direct relationships, for example:

- `category-voc-priority-map` <-> `voc-product-family-bank`
- `category-voc-priority-map` -> `[[docs/seo/master-article-plan-2026-03-29|master-article-plan-2026-03-29]]`
- `voc-product-family-bank` <-> `voc-split-bank`

- [ ] **Step 3: Verify the three VOC docs now link cleanly**

Run: `rg -n "\[\[" "docs/customer reviews/category-voc-priority-map.md" "docs/customer reviews/voc-product-family-bank.md" "docs/customer reviews/voc-split-bank.md"`

Expected: each file contains at least one upward link and at least one meaningful related-doc link.

- [ ] **Step 4: Commit**

```bash
git add "docs/customer reviews/category-voc-priority-map.md" "docs/customer reviews/voc-product-family-bank.md" "docs/customer reviews/voc-split-bank.md"
git commit -m "docs: wire key VOC notes with wikilinks"
```

### Task 6: Link the product context and memory notes

**Files:**
- Modify: `.agents/product-marketing-context.md`
- Modify: `.codex/memories/bastelschachtel/CURRENT-STATE.md`
- Modify: `.codex/memories/bastelschachtel/WORKFLOWS.md`

- [ ] **Step 1: Add a small related-docs block to `.agents/product-marketing-context.md`**

Link at minimum to:

- `[[docs/seo/README]]`
- `[[docs/customer reviews/README]]`
- `[[docs/reference/skill-guides/blogs|Blogs]]`

Keep this block short and near the top or bottom so it does not disturb the main context body.

- [ ] **Step 2: Add upward and lateral links inside the memory notes**

Add:

- from `CURRENT-STATE.md` to `[[.codex/memories/bastelschachtel/README]]`
- from `WORKFLOWS.md` to `[[.codex/memories/bastelschachtel/README]]`
- from both memory docs to the relevant stable entrypoints such as `docs/seo/README`, `docs/customer reviews/README`, and `docs/reference/skill-guides/blogs`

- [ ] **Step 3: Verify the context and memory notes now link cleanly**

Run: `rg -n "\[\[" .agents/product-marketing-context.md .codex/memories/bastelschachtel/CURRENT-STATE.md .codex/memories/bastelschachtel/WORKFLOWS.md`

Expected: each file contains explicit internal wikilinks.

- [ ] **Step 4: Commit**

```bash
git add .agents/product-marketing-context.md .codex/memories/bastelschachtel/CURRENT-STATE.md .codex/memories/bastelschachtel/WORKFLOWS.md
git commit -m "docs: connect context and memory notes with wikilinks"
```

## Chunk 3: Final Verification

### Task 7: Run the final implementation review pass

**Files:**
- Modify: any targeted file above only if verification reveals a gap

- [ ] **Step 1: Run a scoped wikilink coverage check**

Run:

`rg -n "\[\[" docs/seo "docs/customer reviews" docs/superpowers/specs output/content-jobs .codex/memories/bastelschachtel .agents/product-marketing-context.md`

Expected: explicit wikilinks appear across the targeted folders and file.

- [ ] **Step 2: Manually review the new entrypoints**

Open and read:

- `docs/seo/README.md`
- `docs/customer reviews/README.md`
- `docs/superpowers/specs/README.md`
- `output/content-jobs/README.md`
- `.codex/memories/bastelschachtel/README.md`

Confirm:

- links are selective
- no obvious link stuffing
- path-qualified links are used in entrypoints

- [ ] **Step 3: Fix any noisy or redundant links discovered during review**

Only touch already targeted files.

- [ ] **Step 4: Run the final diff check**

Run:

`git diff --name-only <start-ref>..HEAD -- docs/seo "docs/customer reviews" docs/superpowers/specs output/content-jobs .codex/memories/bastelschachtel .agents/product-marketing-context.md`

Expected: only the exact planned markdown files changed within the scoped target paths.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/README.md docs/superpowers/specs/2026-03-29-repo-wikilink-knowledge-graph-design.md .codex/memories/bastelschachtel/README.md .codex/memories/bastelschachtel/START-HERE.md docs/seo/README.md "docs/customer reviews/README.md" output/content-jobs/README.md docs/seo/master-article-plan-2026-03-29.md docs/seo/priority-category-intros-2026-03-29.md docs/seo/live-seo-audit-2026-03-27.md docs/seo/seo-execution-checklist-2026-03-27.md "docs/customer reviews/category-voc-priority-map.md" "docs/customer reviews/voc-product-family-bank.md" "docs/customer reviews/voc-split-bank.md" .agents/product-marketing-context.md .codex/memories/bastelschachtel/CURRENT-STATE.md .codex/memories/bastelschachtel/WORKFLOWS.md
git commit -m "docs: implement Bastelschachtel wikilink incorporation"
```

## Final Verification

- [ ] Run the scoped wikilink coverage check:

`rg -n "\[\[" docs/seo "docs/customer reviews" docs/superpowers/specs output/content-jobs .codex/memories/bastelschachtel .agents/product-marketing-context.md`

Expected: all targeted areas show explicit internal wikilinks.

- [ ] Read the five entrypoint files end to end:

- `docs/seo/README.md`
- `docs/customer reviews/README.md`
- `docs/superpowers/specs/README.md`
- `output/content-jobs/README.md`
- `.codex/memories/bastelschachtel/README.md`

Expected: each reads naturally, links selectively, and clearly points to the next likely note.

- [ ] Confirm no out-of-scope file types were edited:

Run: `git diff --name-only <start-ref>..HEAD -- docs/seo "docs/customer reviews" docs/superpowers/specs output/content-jobs .codex/memories/bastelschachtel .agents/product-marketing-context.md`

Expected: only `.md` files from the planned scope are listed.

## Notes for the Implementer

- Keep each file edit as small as possible.
- Prefer `Related Docs` or `See Also` over inventing new sections unless the file genuinely needs one.
- Do not rewrite the meaning of the documents to justify links.
- Do not add links to every nearby note; only link the next likely note.
- Preserve `START-HERE.md` as the session-start instruction even after adding the memory README.
- Preserve existing plain-text instructions where they are still operationally useful.

Plan complete and saved to `docs/superpowers/plans/2026-03-29-repo-wikilink-incorporation-implementation-plan.md`. Ready to execute?
