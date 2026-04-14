# Shopify Integration Strategy — Bastelschachtel Content Pipeline

**Date:** 2026-04-08
**Platform:** Shopify (not WordPress)
**Scope:** Unified architecture connecting Retool (Perplexity Sonar research + content generation) with Claude Code (QA, SEO optimization, publishing)

---

## Executive Summary

The goal is a **hybrid system** where:
- **Retool** = Human-operated research + content generation interface (Perplexity Sonar → Brief → Article HTML)
- **Claude Code** = Automated QA, SEO optimization, internal linking, and publishing layer
- **Blog SEO Pipeline Plugin** = Orchestration bridge (repository of skills, templates, and QA rules)
- **PostgreSQL (RetoolDB)** = Central store for research dossiers + final published articles
- **Shopify REST API** = Live blog publishing + article management

The pipeline flows:
```
Retool Research Lab (Perplexity Sonar)
         ↓
  Research Dossier (JSON → PostgreSQL)
         ↓
Retool Content Factory (DeepSeek brief + Claude Sonnet article)
         ↓
  Brief + Article HTML (live Retool state, user exports to file)
         ↓
Claude Code Skills (local files: QA, Optimize, Publish)
         ↓
Shopify REST API (publish to live blog)
         ↓
PostgreSQL published_articles table (tracking only)
```

---

## Architecture Layers

### Layer 1: Retool (Operator Interface)
**Current State:** Manual, human-operated pipeline
**Tools:** Perplexity Sonar, DeepSeek, Claude 3.5 Sonnet
**Workflow:**
1. Research Lab: User inputs keyword, locale, research type → Perplexity Sonar generates research dossier (JSON)
2. Save dossier to PostgreSQL `research_dossiers` table
3. Content Factory: User selects dossier + format (deep-dive, listicle, etc.) + products
4. Brief generation (DeepSeek) → saved to Retool state (ephemeral, user can export)
5. Article generation (Claude 3.5 Sonnet) → returned as HTML in Retool textarea (ephemeral, user exports to file)

**Artifacts Produced:**
- Research dossier (JSON) → `research_dossiers` table (persisted)
- Strategic brief (markdown) → Retool state (user copy-pastes if needed)
- Article HTML → Retool textarea (user exports to file)
- Selected products list (JSON) → Retool state

**Integration Point:** Research dossiers are fetched via PostgreSQL. Briefs/articles are exported by user as files to Claude Code.

---

### Layer 2: Claude Code Skills (Codex-side QA & Optimization)
**New Skills to Build:** (in `plugins/blog-seo-pipeline/skills/`)

#### Skill 1: `/qa-article [shopify-handle] OR [file-path]`
**Purpose:** QA a generated article against Bastelschachtel context
**Input:** Either:
  - Shopify article handle (fetches from live API)
  - Local file path (reads markdown/HTML from disk)
**Output:** QA report + revision plan
**Uses:** blog-seo-pipeline QA engine + context files (seo-guidelines, style-guide, writing-examples)
**Modes:** Deep mode (detailed) or quick mode (priority issues only)

#### Skill 2: `/optimize [shopify-handle] OR [file-path]`
**Purpose:** Apply SEO + internal linking + style fixes
**Input:** Either:
  - Shopify article handle (fetches + processes)
  - Local file path (reads + processes)
**Output:** Optimized article HTML/markdown + change summary
**Uses:** target-keywords.md, internal-links-map.md, style-guide.md, writing-examples.md
**Focus:**
- Keyword placement (H1, first 100 words, conclusion)
- Internal linking strategy (4-6 contextual links)
- Meta elements (title 50-60 chars, description 150-160 chars)
- Readability (sentence length, paragraph structure, active voice)
- German grammar validation

#### Skill 3: `/publish [shopify-handle] --revised-file=[path]`
**Purpose:** Publish revised article to Shopify + track in PostgreSQL
**Input:**
  - Shopify article handle (or create new article)
  - Path to revised HTML/markdown file
  - Optional: publish status (draft, published, scheduled)
**Output:** Shopify article URL + status in PostgreSQL `published_articles` table
**Uses:** Shopify REST API + PostgreSQL adapter
**Behavior:**
  - Updates existing Shopify article OR creates new
  - Sets SEO meta title (50-60 chars)
  - Sets SEO meta description (150-160 chars)
  - Updates article content (HTML)
  - Tracks in `published_articles` table with shopify_article_id, published_date, content_hash
  - Returns live Shopify article URL for verification

#### Skill 4: `/research-deep [topic]` (Optional, Power Users)
**Purpose:** Alternative to Retool Research Lab (skip Retool if desired)
**Input:** Bastelschachtel topic keyword + optional Perplexity API key
**Output:** Research dossier (JSON) + save to PostgreSQL
**Integration:** Can skip Retool if user wants direct Codex workflow

#### Skill 5: `/audit-brief [file-path]`
**Purpose:** Validate brief before article generation
**Input:** Brief markdown file
**Output:** Brief audit report + improvement suggestions
**Prerequisite:** Run before article generation (optional quality gate)

---

### Layer 3: Blog SEO Pipeline Plugin (Orchestration & Rules)
**Location:** `plugins/blog-seo-pipeline/`
**Responsibility:** Central repository for:
- Skills definitions (with MCP integration)
- QA templates + rules
- SEO inference rules (from seo-guidelines.md)
- Content family templates (deep-dive, listicle, etc.)
- Shopify API adapter

**Key Files to Create/Update:**
- `skills/` → All 5 skills (as .md files with frontmatter + prompts)
- `integration/shopify-api-adapter.py` → Read/write articles via Shopify REST API
- `integration/shopify-article-schema.md` → Document Shopify API fields
- `.env` → `SHOPIFY_STORE_URL`, `SHOPIFY_ACCESS_TOKEN`
- `hooks.json` → PostPublish hooks (optional: update PostgreSQL on publish)

---

### Layer 4: PostgreSQL / RetoolDB (Minimal Artifact Store)
**Current Tables:**
- `research_dossiers` (topic, research_type, result_json, status) — used actively

**New Table (for tracking):**
```sql
CREATE TABLE published_articles (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  keyword TEXT,
  shopify_article_id INTEGER,
  shopify_article_handle VARCHAR(255),
  article_title TEXT,
  shopify_url VARCHAR(500),
  published_date TIMESTAMP,
  content_hash VARCHAR(64),  -- for duplicate detection
  seo_score INTEGER,
  status ENUM('draft', 'published', 'archived'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Why minimal:** Shopify is the source of truth for live content. PostgreSQL tracks metadata + publish history only.

---

## End-to-End Workflows

### Workflow A: Retool-First (Current Production + Claude Code Enhancement)
1. **Retool Research Lab:** User researches keyword → saves dossier to PostgreSQL
2. **Retool Content Factory:** User generates brief + article HTML
3. **User exports:** Copies article HTML from Retool textarea → saves to local file (or direct to Shopify draft)
4. **Claude Code `/qa-article [file-path]`:** User runs skill on article → gets QA report
5. **Claude Code `/optimize [file-path]`:** User runs skill → receives optimized article
6. **User reviews:** Checks optimized version, approves or requests changes
7. **Claude Code `/publish [shopify-handle] --revised-file=[path]`:** User publishes to Shopify + PostgreSQL updated
8. **Verification:** User checks live blog for correctness

**Advantage:** User controls all approvals. Retool rigor + Claude optimization.
**Duration:** ~30-40 minutes (research → publication with review)

### Workflow B: Pure Codex (Power Users)
1. **Claude Code `/research-deep [topic]`:** Direct research with Perplexity (optional)
2. **Retool Content Factory** OR **Claude generation:** Generate brief + article
3. **Claude Code `/qa-article [file]`** → **`/optimize [file]`** → **`/publish [handle]`** (chained)

**Advantage:** No context switching between tools
**Duration:** ~15-20 minutes (fully automated)

### Workflow C: Hybrid (Recommended)
1. **Retool Research Lab** → research dossier saved to PostgreSQL
2. **Retool Content Factory** → generate brief + article HTML
3. **User exports article** to local file
4. **Claude Code `/qa-article [file]`** (auto-generate QA report)
5. **User reviews QA report** (iterate if needed)
6. **Claude Code `/optimize [file]`** (auto-apply fixes)
7. **User reviews revised article** (approve or request changes)
8. **Claude Code `/publish [shopify-handle] --revised-file=[path]`** (publish with approval)
9. **PostgreSQL updated** with published_articles entry

**Advantage:** Best of both worlds (Retool research rigor + Codex automation + user control)

---

## Integration Points

### Retool ↔ Claude Code
**Artifact Transfer:**
- Research dossier: Retool saves → PostgreSQL → Claude Code can read (optional)
- Briefs: User exports from Retool textarea → saves as file → passes to Claude Code
- Articles: User exports from Retool → saves as file → passes to Claude Code
- Result: User publishes back to Retool or directly to Shopify

**Why this works:**
- No API required (Retool state is ephemeral)
- User has full control + visibility
- Easy to iterate (edit file → re-run skill)

### Claude Code ↔ Shopify
**Read:**
- Fetch article by handle: `GET /admin/api/2024-01/blogs/{blog-id}/articles/{article-id}`
- Returns: title, body_html, author, published_at, image, tags, metafields

**Write:**
- Update article: `PUT /admin/api/2024-01/blogs/{blog-id}/articles/{article-id}`
- Create article: `POST /admin/api/2024-01/blogs/{blog-id}/articles`
- Sets: title, body_html, metafields (for SEO title/description)

**Authentication:**
- Header: `X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}`
- Store: Environment variable in `.env`

### Claude Code ↔ PostgreSQL
**Connection:** DATABASE_URL (already configured)
**Operations:**
- SELECT research_dossiers (read for context)
- INSERT published_articles (track published content)
- UPDATE published_articles (track revisions)

---

## Context Files Integration

**All 9 context files created become:**
- **Part of Claude Code skill prompts** (baked into `/qa-article`, `/optimize`, `/publish`)
- **Reference for Retool operations** (user checks style-guide.md when writing prompts)

**Specific mappings:**
- `target-keywords.md` → `/optimize` uses for keyword placement validation
- `seo-guidelines.md` → `/qa-article` + `/optimize` check content structure
- `style-guide.md` → `/optimize` validates tone, sentence length, German grammar
- `internal-links-map.md` → `/optimize` auto-generates internal linking plan
- `writing-examples.md` → `/qa-article` compares against Bastelschachtel voice patterns
- `master-reference.md` → `/publish` confirms strategic context before publishing

---

## Phased Implementation

### Phase 0: Pre-Flight Check
- [ ] Verify Shopify API token exists in account
- [ ] Test Shopify REST API availability (ping /admin/api/2024-01/blogs.json)
- [ ] Confirm PostgreSQL `research_dossiers` table is accessible
- [ ] Store credentials in `.env` (SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN, DATABASE_URL)

### Phase 1A: Shopify API Adapter Foundation
- [ ] Create `integration/shopify-api-adapter.py`
- [ ] Implement: fetch article by handle, parse HTML, convert to markdown
- [ ] Implement: reverse-convert markdown to HTML
- [ ] Document: Shopify API schema in `integration/shopify-article-schema.md`
- [ ] Test: Fetch Peddigrohr article, convert, verify structure

### Phase 2: `/qa-article` Skill
- [ ] Create skill with file + Shopify handle input options
- [ ] Integrate: context files (seo-guidelines, style-guide, writing-examples)
- [ ] Output: QA report with findings + priority
- [ ] Test: Run against Peddigrohr article, verify QA catches real issues

### Phase 3: `/optimize` Skill
- [ ] Create skill with file + Shopify handle input options
- [ ] Integrate: keyword placement, internal linking, readability checks
- [ ] Output: Revised article + change summary
- [ ] Test: Run `/qa-article` → `/optimize` chain, verify improvements

### Phase 4: `/publish` Skill
- [ ] Create skill with article-handle + revised-file inputs
- [ ] Integrate: Shopify REST API write operations
- [ ] Integrate: PostgreSQL published_articles tracking
- [ ] Output: Shopify article URL + confirmation
- [ ] Test: Publish test article to Shopify, verify live + DB update

### Phase 5: End-to-End Testing
- [ ] Test Workflow A (Retool → export → Claude → publish)
- [ ] Test Workflow B (Retool + Claude chained)
- [ ] Test Workflow C (Retool + QA iteration)
- [ ] Verify Shopify article is live + PostgreSQL tracked

---

## Success Metrics

**Phase 0 (Pre-Flight):**
- ✅ Shopify API token works
- ✅ PostgreSQL accessible
- ✅ Credentials stored securely

**Phase 1A (Adapter):**
- ✅ Can fetch Peddigrohr article by handle
- ✅ Can parse HTML + extract title, body, metadata
- ✅ Can convert to markdown + reverse to HTML
- ✅ Conversion is lossless (structure preserved)

**Phase 2-4 (Skills):**
- ✅ `/qa-article` catches 90%+ of real issues vs manual review
- ✅ `/optimize` improves readability + SEO scores measurably
- ✅ `/publish` creates live Shopify article + tracks in PostgreSQL

**Phase 5 (Integration):**
- ✅ Full workflow completes in <40 minutes (research → publish)
- ✅ Monthly article volume: 10-15 pieces
- ✅ Owned-channel traffic increases measurably within 8-12 weeks

---

## Why This Architecture

1. **Preserve Retool as research + generation interface:** Keeps research flexible, human-controlled
2. **Claude Code for QA + optimization:** Specializes in detailed analysis + refinement
3. **Shopify as source of truth:** Live blog managed directly via REST API
4. **PostgreSQL for tracking:** Minimal but sufficient (research dossiers + published articles)
5. **File-based workflow initially:** No Retool API complexity, just export/import
6. **Context files drive behavior:** All guidelines live in repo, not scattered
7. **Easy to extend:** Add email variant, social excerpt skill, etc. without touching core

---

## Key Differences from WordPress Plan

| Aspect | WordPress Plan | Shopify Plan |
|--------|---|---|
| **Blog Platform** | WordPress REST API | Shopify REST API |
| **SEO Plugin** | Yoast fields | Shopify metafields |
| **Content Format** | Markdown + Gutenberg blocks | HTML from Shopify theme |
| **Artifact Storage** | WordPress posts table | Shopify articles + PostgreSQL tracking |
| **API Complexity** | Higher (Yoast integration) | Simpler (direct fields) |
| **File Workflow** | Designed around WordPress | Designed around Shopify native |

---

*Shopify Integration Strategy for Bastelschachtel SEO content pipeline*
*Architecture: Retool (research + generation) + Claude Code (QA + optimization) + Shopify REST API (publishing) + PostgreSQL (tracking)*
