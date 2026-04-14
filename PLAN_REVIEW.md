# Plan Review: Integration Strategy & Shopify Implementation

**Review Date:** 2026-04-08
**Status:** ⚠️ REQUIRES ADJUSTMENTS (critical issues found)

---

## Summary

**Strength:** Architecture is sound. Shopify integration order is correct. Context files are excellent.

**Critical Issue:** INTEGRATION_STRATEGY.md assumes WordPress + persistent Retool API that doesn't exist yet.

**Severity:** Medium (doesn't block Shopify work, but requires plan clarification)

---

## Issues Found

### 1. ❌ INTEGRATION_STRATEGY.md References "WordPress" Not Shopify

**Problem:**
- Line 30: `WordPress REST API (live blog)` — should be `Shopify REST API`
- Lines 85-90: `/publish [article_file] [status]` designed for WordPress + Yoast SEO
- Lines 113-114: References `wordpress-api-adapter.py` — doesn't exist for Shopify
- Table schema assumes `wordpress_post_id` not `shopify_article_id`

**Impact:** Strategy doc contradicts the actual platform (Shopify, not WordPress)

**Fix:** Update INTEGRATION_STRATEGY.md to Shopify-specific. Keep PostgreSQL tracking but reference Shopify article IDs.

---

### 2. ⚠️ Retool API Bridge Not Live (Per Reality Check Doc)

**Problem:**
From `2026-03-28-retool-api-reality-check.md`:
- No live HTTP API for Retool content pipeline
- Retool Database queries are server-side SQL only
- No exposed endpoints for Claude Code to call
- Artifacts currently ephemeral (kept in Retool state, not persisted)

**Current Reality:**
- Research dossiers → Persisted to `research_dossiers` table ✅
- Briefs → Live in Retool state only (not DB) ⚠️
- Articles → Live in Retool textarea only (not DB) ⚠️
- No HTTP API to fetch them from Claude Code ❌

**Integration Impact:**
- INTEGRATION_STRATEGY says `/qa-article [dossier_id] [article_file]` can fetch from PostgreSQL
- Reality: Articles are passed manually (copy/paste or export from Retool)
- Briefs are also manual

**Fix:** Accept ephemeral workflow for now. Skills work with **local files** not PostgreSQL fetches. Users export from Retool → Claude Code processes locally → User manually posts result back to Retool or publishes.

---

### 3. ✅ Shopify Plan is Correct (No Issues)

**Strengths:**
- Shopify API is real + documented
- Adapter-first approach (Phase 1A) is safe
- HTML ↔ Markdown conversion is feasible
- Read-only QA before write operations is prudent

**No changes needed here.**

---

### 4. ⚠️ Task Breakdown Needs Clarification

**Issue:** Tasks #2-4 assume Shopify fetch is automatic

**Task #2 current:** `/qa-article [article-handle]`
- Says: "Fetch article from Shopify"
- Assumes: Skill can read article by handle
- Reality: ✅ This works once Phase 1A adapter exists

**Task #4 current:** `/publish [article-handle]`
- Says: "Update Shopify article via REST API"
- Assumes: Takes **revised HTML** + **article-handle** → updates live
- Reality: ✅ This works, but should also accept **local file** as fallback

**Fix:** Task descriptions are fine, but add note: "Can also accept local file path if Shopify fetch fails"

---

## Revised Plan (Corrected)

### What to Keep ✅

1. **9 Context Files** — Perfect. No changes.
2. **Shopify Integration Plan** — Excellent. No changes.
3. **Task #1 (Shopify API Adapter)** — Correct first step.
4. **Tasks #2-4 (QA, Optimize, Publish)** — Correct order.

### What to Fix/Clarify 🔧

1. **Replace INTEGRATION_STRATEGY.md** with **SHOPIFY_INTEGRATION_STRATEGY.md**
   - Keep architecture layers
   - Replace WordPress references with Shopify
   - Accept ephemeral workflow (Retool state → files → Claude Code → back to user)
   - Remove PostgreSQL artifact assumptions for briefs/articles (keep for research dossiers + final published)

2. **Update Task #2-4 Descriptions:**
   - Add note: "Falls back to local file if Shopify API unavailable"
   - Remove assumptions about automatic artifact fetch from PostgreSQL

3. **Add Task #0: Verify Retool Credentials**
   - Confirm Shopify API token access
   - Test Shopify REST API availability before building adapter

---

## Revised Workflow (Based on Reality)

```
User in Retool:
1. Research Lab → generates dossier → saved to PostgreSQL ✅
2. Content Factory → generates brief (kept in Retool state)
3. Content Factory → generates article HTML (kept in Retool textarea)
4. User exports/copies article HTML to local file or Shopify draft

User in Claude Code:
5. `/qa-article [article-handle]` OR `/qa-article /path/to/article.html`
   → Fetches from Shopify OR reads local file
   → Produces QA report
6. `/optimize [article-handle]` OR `/optimize /path/to/article.html`
   → Applies fixes
   → Returns revised HTML (user reviews)
7. User approves revised HTML
8. `/publish [article-handle] --revised-file=/path/to/revised.html`
   → Updates Shopify article
   → Tracks in PostgreSQL published_articles table
   → Returns Shopify article URL

Result: Seamless workflow despite Retool API gaps
```

---

## What This Means for Task Execution

### No blocker for starting Task #1 ✅
- Build Shopify API Adapter as planned
- Test with actual credentials

### Tasks #2-4 remain valid ✅
- Add local file fallback to skill inputs
- Design skills to work with files OR Shopify handles

### Retool integration becomes future optimization (not blocking) ⏳
- Once Retool exposes API → can auto-fetch briefs/articles
- Until then → manual export/import between tools
- Still reduces friction vs. manual editing

---

## Recommended Action

**Option A: Update Plans Now (Recommended)**
1. Create SHOPIFY_INTEGRATION_STRATEGY.md (correct version)
2. Mark INTEGRATION_STRATEGY.md as "for reference only, Shopify variant exists"
3. Update Task #2-4 descriptions with file fallback notes
4. Add Task #0: Verify Shopify + Retool credentials
5. Proceed with implementation

**Option B: Proceed As-Is**
- Implementation won't be blocked (Shopify work is independent)
- But context will confuse future readers
- Recommend fixing docs before Task #2

---

## Verdict: Plan is Sound, Docs Need Shopify Clarity

**The actual workflow will work great.** The architecture is right. Shopify is simpler than WordPress anyway.

**Just need to update docs to match Shopify reality, not WordPress assumption.**

**Recommendation:** Spend 30 min fixing INTEGRATION_STRATEGY.md → Create SHOPIFY_INTEGRATION_STRATEGY.md variant. Then execute Task #0-4 with confidence.

---

*Review by Claude Code*
*2026-04-08*
