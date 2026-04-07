# Workflows
#memory

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

## Obsidian Graph Maintenance

- For Bastelschachtel repo graph work, use the portable `obsidian-this` framework
- Neutral commands:
  - `python C:\Users\Hp\.agents\skills\obsidian-this\scripts\obsidian_this.py init --repo <path>`
  - `python C:\Users\Hp\.agents\skills\obsidian-this\scripts\obsidian_this.py check --repo <path>`
  - `python C:\Users\Hp\.agents\skills\obsidian-this\scripts\obsidian_this.py fix --repo <path>`
- `init` discovers the repo and writes `.obsidian-this/config.json`
- Ongoing behavior should come from repo-local config, not fresh guesswork
- `fix` is limited to deterministic graph hygiene in v1
- File-format normalization is excluded from `fix` in v1

## Related Docs

- [[.codex/memories/bastelschachtel/README]]
- [[docs/reference/skill-guides/blogs|Blogs]]
- [[docs/seo/README]]
- [[docs/customer reviews/README]]
