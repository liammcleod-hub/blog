# Current State

## Skill Source Of Truth

- Active global skills live under `C:\Users\Hp\.agents\skills`
- Duplicate active copies under `C:\Users\Hp\.codex\skills` were disabled and moved under `C:\Users\Hp\.codex\skills-disabled`
- Repo-local gstack skill copies were moved out of the project skill scan path

## GStack Notes

- Global `gstack` skill in `.agents\skills` was fixed to use a Codex-safe short description
- `office-hours` and the rest of the gstack skills now follow the same global install pattern

## Repo Notes

- Bastelschachtel-specific blog skill guide lives at `docs/reference/skill-guides/blogs.md`
- That guide should be used for blog-post workflow selection
- Existing VOC inputs live under `docs/customer reviews/`
- Existing SEO planning inputs live under `docs/seo/`

## README-First Rule

- `docs/customer reviews/README.md` now exists and should be read first when using that folder
- `docs/seo/README.md` now exists and should be read first when using that folder
- `output/README.md` now exists and should be read first when using `output/`
- `output/content-jobs/README.md` remains the source of truth for content-job bundle structure

## Product Marketing Context

- `.agents/product-marketing-context.md` was refreshed on `2026-03-29`
- It now includes:
  - review-backed customer language
  - direct testimonial snippets
  - category priority and master-article SEO strategy
  - sharper category-level competition notes
- Treat that file as the main Bastelschachtel positioning/context source before marketing work

## SEO / VOC Artifacts

- Current VOC layer is organized under `docs/customer reviews/`
- Current SEO planning layer is organized under `docs/seo/`
- Important recent additions include:
  - category VOC priority mapping
  - product-family VOC bank
  - priority category intros
  - master-article planning

## Plugin State

- `plugins/blog-seo-pipeline/` is locally real and verified
- Local plugin tests pass:
  - `pytest plugins/blog-seo-pipeline/tests -q -p no:cacheprovider`
  - result last verified in-session: `31 passed`
- The main blocker is no longer local plugin architecture
- The blocker is the live read-only Retool/content-pipeline wrapper:
  - real base URL
  - auth method
  - exact live routes
  - known-good live IDs/topics/keywords

## Second Plugin Direction

- The future second plugin is the cluster/scale engine, not the single-article truth engine
- Repo docs should own the spinoff article template library
- The second plugin should consume repo-defined templates rather than inventing its own
- The second plugin should generate lean, structured, context-referencing briefs rather than bloated self-contained ones

## Practical Rule

- For Bastelschachtel blog work, do not start from zero
- Read VOC and SEO docs first, then use `blog-seo-pipeline`, then `copywriting`, then `copy-editing`
