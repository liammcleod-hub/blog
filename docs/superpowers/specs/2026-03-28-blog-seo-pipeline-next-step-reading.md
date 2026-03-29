# Blog SEO Pipeline Next-Step Reading

Read these files in this order before continuing the last-mile work on the plugin.

## 1. V1 Design

- `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-v1-design.md`

Why:

- this is the scoped source of truth for what v1 is and is not

## 2. V1 Implementation Plan

- `docs/superpowers/plans/2026-03-27-blog-seo-pipeline-plugin-v1-implementation-plan.md`

Why:

- this shows the intended build order and the verification expectations

## 3. Current State Snapshot

- `docs/superpowers/specs/2026-03-28-blog-seo-pipeline-plugin-v1-current-state.md`

Why:

- this shows what has already been built and what still remains blocked

## 4. Retool API Reality Check

- `docs/reference/content-pipeline/2026-03-28-retool-api-reality-check.md`

Why:

- this explains the current blocker clearly: there is no live content-pipeline HTTP API yet

## 5. Content-Pipeline References

- `docs/reference/content-pipeline/README.md`
- `docs/reference/content-pipeline/v1-ingest-contract.md`
- `docs/reference/content-pipeline/run-modes.md`
- `docs/reference/content-pipeline/retool-readonly-access-plan.md`
- `docs/reference/content-pipeline/retool-readonly-api-spec.md`

Why:

- these define the Codex-side workflow, accepted artifact contract, run-mode rules, and the intended read-only integration shape

## 6. Retool Process References

- `docs/reference/retool/README.md`
- `docs/reference/retool/process.md`
- `docs/reference/retool/integration-contract.md`

Why:

- these explain the real operator workflow and how Retool artifacts are meant to flow into the plugin

## 7. Plugin Runtime

- `plugins/blog-seo-pipeline/README.md`
- `plugins/blog-seo-pipeline/scripts/blog_me_this.py`
- `plugins/blog-seo-pipeline/scripts/discovery.py`
- `plugins/blog-seo-pipeline/scripts/external_sources.py`

Why:

- these are the main runtime entrypoint and the most important integration points for the final steps

## 8. Test Coverage

- `plugins/blog-seo-pipeline/tests/test_external_sources.py`
- `plugins/blog-seo-pipeline/tests/test_discovery.py`
- `plugins/blog-seo-pipeline/tests/test_blog_me_this.py`

Why:

- these show the verified behavior for the adapter and the end-to-end command path

## Final Orientation

After reading the files above, the next question should be:

`Where will the real read-only API live, and what exact live routes/auth details should the plugin use?`
