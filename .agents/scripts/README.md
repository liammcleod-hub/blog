# Bastelschachtel Content Pipeline Scripts

Automation tools for fetching and managing Bastelschachtel blog content from Retool.

## Quick Start

### Create a blog job from the latest Retool dossier

```bash
cd bastelschachtel/
npm run create-blog-job latest
```

This creates a complete job folder under `output/content-jobs/<job-slug>/` with:
- Research dossier JSON
- Approved products
- Brief (if persisted in Retool)
- Article HTML (if persisted in Retool)

The folder is ready to pass to the **blog-seo-pipeline** skill for QA or revision.

### Or use a specific dossier ID

```bash
npm run create-blog-job 16
```

## What It Does

The `create-blog-job-from-retool.js` script:

1. Connects to the Retool PostgreSQL database
2. Fetches the latest (or specified) research dossier
3. Queries approved products for that keyword
4. Attempts to fetch persisted brief and article (if available)
5. Creates a structured job folder with all artifacts
6. Outputs JSON metadata about what was created

## Job Folder Structure

```
output/content-jobs/oster-bastel-ideen-2026-03-30/
├── job.json                 # metadata
├── research-dossier.json    # full research (from Retool)
├── selected-products.json   # approved products
├── brief.md                 # strategic brief (if persisted)
└── article.html             # final article HTML (if persisted)
```

## Workflow Integration

### Standard blog-seo-pipeline QA workflow:

1. **Fetch from Retool:**
   ```bash
   npm run create-blog-job latest
   ```

2. **QA the created job folder** (via blog-seo-pipeline skill)
   - Review research dossier
   - Audit brief structure
   - Check article coverage, SEO, brand voice
   - Generate QA report

3. **Optionally revise** (if blog-seo-pipeline identifies issues)
   - Update article HTML
   - Refine product links
   - Improve brand voice consistency

4. **Publish to repo** or export for publishing

## Scripts Included

### `create-blog-job-from-retool.js`

Main tool to fetch Retool artifacts and create a job folder.

**Usage:**
```bash
node .agents/scripts/create-blog-job-from-retool.js latest
node .agents/scripts/create-blog-job-from-retool.js <dossier-id>
```

**Options:**
- `--brief` - warn if brief is expected but not found in DB
- `--article` - warn if article is expected but not found in DB

**Output:** JSON metadata about the created job

### `fetch-retool-artifacts.js`

Lower-level tool that just fetches artifacts from Retool DB without creating files.

**Usage:**
```bash
node .agents/scripts/fetch-retool-artifacts.js latest
node .agents/scripts/fetch-retool-artifacts.js <dossier-id>
```

**Output:** Full artifact bundle as JSON (printed to stdout)

## Database Connection

Both scripts connect to the Retool PostgreSQL database using credentials stored in the script:

```
host: ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com
user: retool
password: npg_nGJpXRcD2Mh5
database: retool
```

**Note:** Credentials are currently inline. Future improvements could move these to `.env` or `process.env`.

## Database Schema

Scripts query these Retool DB tables:

- `research_dossiers` - research runs with `result_json` field
- `product_keyword_approvals` - approved products for keywords
- `content_briefs` - persisted strategic briefs (optional)
- `staged_articles` - persisted article HTML (optional)

## Limitations

- **Brief/Article persistence:** Not all Retool runs save briefs and articles to DB yet. Scripts warn if expected but not found.
- **Product matching:** Only fetches products explicitly approved in `product_keyword_approvals` with status `Use Product Link`.
- **No write access:** Scripts are read-only. They create files locally but don't modify Retool DB.

## Next Steps

- [ ] Add `.env` support for database credentials
- [ ] Add `--output` flag to customize job folder location
- [ ] Integrate with blog-seo-pipeline skill for one-command workflow
- [ ] Add option to auto-trigger blog-seo-pipeline after fetch
- [ ] Cache recent dossier queries for faster subsequent runs
- [ ] Add filtering by topic/keyword for "latest" queries

## Troubleshooting

**Connection timeout:**
- Verify network access to `ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com:5432`
- Check if Retool DB is running

**Dossier not found:**
- Verify the dossier ID exists in Retool
- Check `research_dossiers` table in Retool DB directly

**No products found:**
- Ensure products are approved in Retool with status `Use Product Link`
- Check that keyword matches the dossier topic

**Brief/Article not saved:**
- This is expected. Retool may not persist these yet.
- Manually add `brief.md` and `article.html` to the job folder if needed
