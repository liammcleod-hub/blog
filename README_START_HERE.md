# Bastelschachtel SEO Content Pipeline — START HERE

**Date:** 2026-04-08
**Status:** ✅ READY TO EXECUTE

---

## What You Have

✅ **9 Context Files** (`seo/context/`)
- brand-voice.md, competitor-analysis.md, seo-guidelines.md, features.md, internal-links-map.md, style-guide.md, target-keywords.md, writing-examples.md, master-reference.md

✅ **Shopify Integration Strategy** (SHOPIFY_INTEGRATION_STRATEGY.md)
- Architecture: Retool (research) + Claude Code (QA/optimize) + Shopify (publish) + PostgreSQL (track)
- 5 skills to build in `plugins/blog-seo-pipeline/skills/`

✅ **5 Executable Tasks** (Ready to run)
- Task #1: Shopify API Adapter (foundation)
- Task #2: /qa-article skill
- Task #3: /optimize skill
- Task #4: /publish skill
- Task #5: End-to-end testing

---

## How It Works (Simple Version)

```
User in Retool:
1. Research keyword → saves dossier to PostgreSQL
2. Generate brief + article HTML
3. Export article to file

User in Claude Code:
4. Run /qa-article [file] → get QA report
5. Run /optimize [file] → get improved version
6. Run /publish [shopify-handle] --revised-file=[file] → live on Shopify

Done. Article published + tracked.
```

---

## Start Here (Next 30 Minutes)

### Step 1: Verify Prerequisites
```bash
# Check Shopify token exists
echo $SHOPIFY_STORE_URL
echo $SHOPIFY_ACCESS_TOKEN

# Test Shopify API
curl -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "https://$SHOPIFY_STORE_URL/admin/api/2024-01/blogs.json"

# Check PostgreSQL
psql $DATABASE_URL -c "SELECT COUNT(*) FROM research_dossiers;"
```

### Step 2: Claim Task #1
```bash
# Build Shopify API Adapter
# Location: plugins/blog-seo-pipeline/integration/shopify-api-adapter.py
# Needs: HTTP requests, HTML parsing, Markdown conversion
# Test with: Peddigrohr article handle
```

### Step 3: Success Criteria for Task #1
- ✅ Fetch Peddigrohr article by handle
- ✅ Parse HTML + extract title, body, metadata
- ✅ Convert to markdown
- ✅ Reverse-convert back to HTML (lossless)
- ✅ Store Shopify credentials securely in .env

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `SHOPIFY_INTEGRATION_STRATEGY.md` | Master strategy (read this first) |
| `seo/context/` (9 files) | Brand guidelines, keywords, style rules |
| `plugins/blog-seo-pipeline/` | Where skills will live |
| `PLAN_REVIEW.md` | Why we chose this approach |
| `docs/reference/retool/` | Retool architecture docs |

---

## Critical Constraints

1. **Retool artifacts are ephemeral** (kept in Retool state, not auto-persisted)
   - User exports brief/article manually to file
   - Claude Code processes files locally
   - This is by design (simpler than building Retool API)

2. **Shopify is source of truth** (not PostgreSQL)
   - PostgreSQL only tracks published articles (metadata)
   - Live content lives on Shopify
   - This is cleaner than WordPress

3. **All skills accept file paths OR Shopify handles**
   - `/qa-article [file]` OR `/qa-article [handle]`
   - Gives flexibility for testing + production

---

## Success Looks Like

**After Task #1:** Can fetch + parse Shopify articles programmatically
**After Task #2:** Can analyze articles against Bastelschachtel standards
**After Task #3:** Can automatically improve SEO + style
**After Task #4:** Can publish to live Shopify + track in database
**After Task #5:** Full workflow runs in <40 minutes with user control

---

## Questions?

- **Architecture:** See SHOPIFY_INTEGRATION_STRATEGY.md
- **Why this approach:** See PLAN_REVIEW.md
- **Context/guidelines:** See seo/context/ folder
- **Retool details:** See docs/reference/retool/

---

## Next Action

→ **Start Task #1: Build Shopify API Adapter**

Good luck! 🚀
