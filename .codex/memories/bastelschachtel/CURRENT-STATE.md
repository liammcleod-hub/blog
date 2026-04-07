# Current State
#memory

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

## Obsidian State

- The repo now has a first-pass Obsidian-friendly visible graph layer across the main Bastelschachtel docs
- Visible note targets should use Obsidian wikilinks
- Hidden or non-clickable targets such as `.agents/...` should stay plain text/code paths, not fake clickable links
- Folder entrypoints were tightened around `README.md` notes in the main visible doc areas
- Visible repo docs may use simple hashtag tags under the H1
- Visible skill notes in `repo-skills/marketing-library/skills/*/SKILL.md` use bottom-only `#skills`
- `docs/superpowers/specs/` and `docs/superpowers/plans/` were intentionally left out of the narrowed tag filter surface

## Obsidian This

- A portable `obsidian-this` framework now exists
- Repo-local source bundle lives at `.agents/skills/obsidian-this/`
- Global installed copy lives at `C:\Users\Hp\.agents\skills\obsidian-this`
- Neutral command surface:
  - `python C:\Users\Hp\.agents\skills\obsidian-this\scripts\obsidian_this.py init --repo <path>`
  - `python C:\Users\Hp\.agents\skills\obsidian-this\scripts\obsidian_this.py check --repo <path>`
  - `python C:\Users\Hp\.agents\skills\obsidian-this\scripts\obsidian_this.py fix --repo <path>`
- The framework is agent-agnostic by design:
  - `SKILL.md` is a Codex-friendly wrapper
  - `AGENT.md` documents neutral use for Claude, Gemini, or other CLI agents
- Durable repo learning for `obsidian-this` lives in `.obsidian-this/config.json`
- `fix` is graph hygiene only in v1
- File-format normalization is report-only in v1 and not part of `fix`
- Current implementation status:
  - full local test suite passed in-session: `21 passed`
  - end-to-end `init/check/fix` flow was verified on a writable copied fixture repo

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

## Related Docs

- [[.codex/memories/bastelschachtel/README]]
- [[docs/reference/skill-guides/blogs|Blogs]]
- [[docs/seo/README]]
- [[docs/customer reviews/README]]
- `.agents/product-marketing-context.md`
