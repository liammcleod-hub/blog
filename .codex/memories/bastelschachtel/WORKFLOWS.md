# Workflows

## Blog Posts

Primary guide:

- `docs/reference/skill-guides/blogs.md`

Recommended sequence:

1. Read `README.md` in the relevant Bastelschachtel reference folders first
2. Read relevant materials in `docs/customer reviews/`
3. Read relevant planning materials in `docs/seo/`
4. Use `content-strategy` if topic selection is still open
5. Use `blog-seo-pipeline`
6. Use `copywriting`
7. Use `copy-editing`
8. Use `ai-seo` or `schema-markup` if relevant

Additional rule:

- Do not hard-code one dated file as the permanent entrypoint when a Bastelschachtel reference folder has a `README.md`

## Plugins

- `blog-seo-pipeline` = single-job truth engine
- future second plugin / cluster engine = topic expansion, spinoff orchestration, sequencing, and cluster planning
- repo docs should own the template library for spinoff article styles
- the second plugin should consume that template library and emit lean, context-referencing briefs

## Skill Hygiene

- Prefer `.agents\skills` as the only active global skill source
- Treat `.codex\skills-disabled` as archive/disabled storage, not an active source
