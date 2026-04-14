---
name: "Bastelschachtel Project Operating Manual"
description: "Project-specific config for Bastelschachtel marketing ops and content"
type: project-config
version: 1.0
project: bastelschachtel
created: 2026-04-06
status: "Production + Growth"
modified: 2026-04-06
---
# _CLAUDE.md — Bastelschachtel

**Status:** Production + Growth
**Owner:** Bastelschachtel Team
**Last Updated:** 2026-04-06

---

## What This Is

Bastelschachtel is a Tirolean arts & crafts store. This project focuses on marketing ops, content strategy, SEO, customer research, and growth experiments.

---

## Start Here

- **Operating Context**: `Code/.agents/product-marketing-context.md` (full context)
- **SEO & Research**: `Code/docs/seo/README` + `Code/docs/customer reviews/README`
- **Strategy & Specs**: `Code/docs/superpowers/specs/README` + `Code/docs/superpowers/plans/`
- **Skill Routing**: `Code/docs/reference/skill-guides/README`
- **Content Output**: `Code/output/content-jobs/README`

---

## Key Directories

```
Code/
├── .agents/
│   ├── product-marketing-context.md    (source of truth)
│   ├── marketingskills/                (real skill source)
│   └── skills/
├── docs/
│   ├── seo/                            (SEO planning & content)
│   ├── customer reviews/               (customer research)
│   ├── strategy/                       (business strategy)
│   ├── superpowers/
│   │   ├── specs/                      (implementation specs)
│   │   └── plans/                      (execution plans)
│   └── reference/
│       ├── skill-guides/               (routing guides)
│       ├── content-pipeline/
│       └── retool/
├── output/
│   ├── content-jobs/                   (operational output)
│   └── playwright/                     (visual testing)
├── repo-skills/
│   ├── blog-seo-pipeline/
│   └── marketing-library/
├── brand_assets/                       (brand voice & guidelines)
├── sessionstart.md                     (minimal startup pointer)
└── README.md
```

---

## Operating Rules

1. **Source of truth**: `.agents/product-marketing-context.md` — read first
2. **Visible docs**: Maintain wikilinks in `docs/` and `output/`
3. **Hidden files**: No Obsidian tags in `.agents/` files
4. **Skill docs**: Use bottom-only `#skills` tag in `repo-skills/*/SKILL.md`
5. **Core workflows**: SEO → Customer Research → Specs → Plans → Output
6. **Fixable zones**: `docs/seo/`, `docs/customer reviews/`, `docs/superpowers/specs/`

---

**Ready to help with marketing ops, content, SEO, and growth!** 🚀
