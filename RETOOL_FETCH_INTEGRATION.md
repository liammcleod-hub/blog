# Retool Database Fetch Integration for Blog SEO Pipeline

**Status:** ✅ Live and tested (March 30, 2026)

## What This Solves

Previously, when you created a new blog article in Retool:
1. Generate research dossier → **manually copy JSON**
2. Generate brief → **manually copy text**
3. Generate article → **manually copy HTML**
4. Select products → **manually create JSON**
5. Paste all 4 files into `bastelschachtel/output/content-jobs/`
6. Run blog-seo-pipeline skill for QA

**Now:** One command does all the fetching automatically:

```bash
npm run create-blog-job latest
```

The blog-seo-pipeline receives a complete, ready-to-QA folder. No copy-paste needed.

## Quick Start

### 1. In your Bastelschachtel directory:

```bash
cd bastelschachtel/

# Fetch the latest Retool dossier and create a job folder
npm run create-blog-job latest
```

**Output:**
```json
{
  "success": true,
  "job_folder": "...\bastelschachtel\output\content-jobs\oster-bastel-ideen-2026-03-30",
  "job_slug": "oster-bastel-ideen-2026-03-30",
  "topic": "oster bastel ideen",
  "dossier_id": 16,
  "products_count": 0,
  "has_brief": false,
  "has_article": false,
  "files_created": [
    "job.json",
    "research-dossier.json",
    "selected-products.json"
  ]
}
```

### 2. Job folder is now ready

```
output/content-jobs/oster-bastel-ideen-2026-03-30/
├── job.json                 # metadata: topic, dossier_id, created_at
├── research-dossier.json    # full research (citations, competitors, intents)
├── selected-products.json   # approved products from Retool
├── brief.md                 # (if persisted in Retool)
└── article.html             # (if persisted in Retool)
```

### 3. Run blog-seo-pipeline

Ask me (Codex) to review the job:
```
/blog-seo-pipeline qa output/content-jobs/oster-bastel-ideen-2026-03-30/
```

Or if you want revisions applied:
```
/blog-seo-pipeline revise output/content-jobs/oster-bastel-ideen-2026-03-30/
```

## How It Works

### Technology

- **Database:** Retool PostgreSQL (hosted at `ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com`)
- **Client:** Node.js `pg` library (installed via `npm install`)
- **Script:** `.agents/scripts/create-blog-job-from-retool.js`

### Workflow

1. Script connects to Retool DB using hardcoded credentials
2. Queries `research_dossiers` table for latest (or specified) dossier
3. Queries `product_keyword_approvals` for products matching the keyword
4. Optionally queries `content_briefs` and `staged_articles` (if persisted)
5. Creates job folder with standardized structure
6. Outputs JSON summary

### Database Tables Used

- **`research_dossiers`** - Research runs with `result_json`, `topic`, `research_type`, timestamps
- **`product_keyword_approvals`** - Approved products with `product_handle`, `product_url`, `image_url`
- **`content_briefs`** - Strategic briefs (optional; may not be persisted yet)
- **`staged_articles`** - Article HTML (optional; may not be persisted yet)

## Commands

### Main command (recommended)

```bash
npm run create-blog-job latest
# Creates output/content-jobs/<topic>-<date>/ with all artifacts
```

### With specific dossier ID

```bash
npm run create-blog-job 16
# Fetch dossier #16 specifically
```

### Lower-level fetch (just shows JSON, doesn't create files)

```bash
npm run fetch-retool latest
# Outputs full artifact bundle as JSON
```

## What Gets Created

### `job.json`
Metadata about the run:
```json
{
  "slug": "oster-bastel-ideen-2026-03-30",
  "topic": "oster bastel ideen",
  "dossier_id": 16,
  "research_type": "general_dossier",
  "locale": "de-AT",
  "created_at": "2026-03-30T17:39:12.345Z",
  "created_from_retool": true
}
```

### `research-dossier.json`
Full research output from Retool Research Lab:
```json
{
  "locale": "de-AT",
  "topic": "oster bastel ideen",
  "research_type": "general_dossier",
  "summary": "...",
  "citations": [...],
  "competitor_blueprints": [...],
  "competitor_findings": [...],
  "search_intents": [...]
}
```

### `selected-products.json`
Approved products from Retool product selection:
```json
[
  {
    "product_handle": "bastelset-ostern-123",
    "product_name": "Bastelset Ostern Hasengirlande",
    "product_url": "https://...",
    "image_url": "https://...",
    "status": "Use Product Link"
  }
]
```

### `brief.md` (if persisted)
Strategic brief text (only if Content Factory brief was saved to DB)

### `article.html` (if persisted)
Final article HTML (only if Content Factory article was saved to DB)

## Integration with Blog SEO Pipeline Skill

The **blog-seo-pipeline** skill expects exactly this folder structure. Simply point it at the job folder:

```bash
/blog-seo-pipeline qa <job-folder-path>
# or
/blog-seo-pipeline revise <job-folder-path>
```

The skill will:
1. Load `job.json` for context
2. Load `research-dossier.json` for fact-checking
3. Load `selected-products.json` for link validation
4. Load `brief.md` (if present) for structure validation
5. Load `article.html` (if present) for final QA

## Configuration

Database credentials are currently hardcoded in:
- `.agents/scripts/create-blog-job-from-retool.js`
- `.agents/scripts/fetch-retool-artifacts.js`

**Connection string:**
```
postgresql://retool:npg_nGJpXRcD2Mh5@ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com/retool?sslmode=require
```

If you need to change the database or credentials, update the `DB_CONFIG` object in either script.

## Limitations

1. **Brief persistence:** Briefs are generated in Retool but may not be saved to DB. If not found, the script warns but doesn't fail.
2. **Article persistence:** Same as briefs—only created if Retool Content Factory saves to `staged_articles`.
3. **Product matching:** Only fetches products explicitly marked as `Use Product Link` in `product_keyword_approvals`.
4. **Read-only:** Scripts only fetch; they don't modify Retool DB.

## Future Improvements

- [ ] Move DB credentials to `.env` file
- [ ] Add filtering/search for older dossiers
- [ ] Auto-generate brief.md if not persisted (using AI)
- [ ] Auto-generate article.html if not persisted (using AI)
- [ ] One-command flow: fetch → QA → publish
- [ ] Integration with IES (email intelligence) to suggest topics

## Troubleshooting

**"No recent dossier found"**
- Ensure you've created at least one research dossier in Retool Research Lab

**"0 approved products"**
- Go to Retool Content Factory → select products → ensure status is `Use Product Link`

**"Connection timeout"**
- Network issue reaching `ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com`
- Check your internet connection and firewall

**"npm: command not found"**
- Node.js/npm not installed or not in PATH
- Install Node.js from nodejs.org

## Files Modified

- `package.json` - Added npm scripts: `fetch-retool`, `create-blog-job`
- `.agents/skills/blog-seo-pipeline/SKILL.md` - Added Mode 3 intake documentation
- `.agents/scripts/` - New scripts and README

## References

- [Blog SEO Pipeline Skill](/bastelschachtel/.agents/skills/blog-seo-pipeline/SKILL.md)
- [Script Documentation](/bastelschachtel/.agents/scripts/README.md)
- [Retool Content Pipeline Docs](/bastelschachtel/docs/reference/retool/)
