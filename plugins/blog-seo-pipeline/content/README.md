# Blog SEO Pipeline - Content Folder

**Purpose:** Central repository for all published and draft articles in the Bastelschachtel content pipeline.

---

## Structure

```
content/
├── published/                    ← Articles live on WordPress
│   ├── korbflechten/
│   │   ├── article.html
│   │   ├── metadata.json
│   │   ├── research-brief.md
│   │   ├── product-linkage.md
│   │   ├── publishing-log.md
│   │   └── analytics.json        (added post-publication)
│   │
│   └── [more articles]/
│
└── drafts/                       ← Articles in progress
    ├── [article-name]/
    └── [more draft articles]/
```

---

## Article Folder Contents

Each article folder MUST contain:

| File | Purpose | Required |
|------|---------|----------|
| `article.html` | Final article (HTML) | ✅ Yes |
| `metadata.json` | SEO + publishing metadata | ✅ Yes |
| `research-brief.md` | Research summary | ✅ Yes |
| `product-linkage.md` | Product linking report | ⚠️ If products linked |
| `publishing-log.md` | Publication history | ✅ Yes |
| `analytics.json` | Traffic metrics | (post-publication) |
| `qa-report.md` | QA findings | (if QA run) |

---

## Metadata File Reference

```json
{
  "article_id": "unique-slug",
  "title": "Display title",
  "seo_title": "SEO title (50-60 chars)",
  "meta_description": "Meta description (150-160 chars)",
  "canonical_url": "https://bastelschachtel.at/blog/...",
  "primary_keyword": "main keyword",
  "secondary_keywords": ["kw1", "kw2"],
  "language": "de",
  "word_count": 2000,
  "status": "published | draft",
  "publishing": {
    "wordpress_post_id": 12345,
    "publish_date": "2026-04-09",
    "published_url": "https://bastelschachtel.at/blog/..."
  }
}
```

---

## Workflow

### 1. **Source:** seomachine/articles/{name}/
All articles originate in the seomachine repository under `articles/` folder.

### 2. **Sync to Pipeline:**
```bash
# Copy article to Bastelschachtel draft folder
cp seomachine/articles/{name}/* \
   bastelschachtel/Code/plugins/blog-seo-pipeline/content/drafts/{name}/
```

### 3. **Review & Optimize:**
Run skills in Claude Code (if needed):
- `/qa-article` — Quality assurance
- `/optimize` — SEO + readability improvements
- Update files in `drafts/{name}/`

### 4. **Publish:**
- Copy article HTML to WordPress
- Add Yoast metadata
- Set publication date
- Update `metadata.json` with `wordpress_post_id`
- Move folder: `drafts/{name}/` → `published/{name}/`

### 5. **Monitor:**
- Add `analytics.json` with GA4 metrics after 7 days
- Track engagement, clicks, search performance

---

## Current Articles

### Published

| Article | Status | Published Date | Post ID |
|---------|--------|---|---|
| Korbflechten Material Anfänger | Ready | (pending) | (pending) |

### Drafts

(None yet)

---

## Integration Points

**← seomachine**: Articles copied from seomachine/articles/ to this folder
**→ WordPress**: Articles published to WordPress REST API + Yoast SEO metadata

---

## Notes

- Each article is self-contained (all supporting files in one folder)
- `metadata.json` is the single source of truth for article status
- Analytics are populated post-publication in `analytics.json`
- Drafts are work-in-progress; published are live articles

---

*Last updated: 2026-04-09*
