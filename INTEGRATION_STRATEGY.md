# Bastelschachtel Content Pipeline Integration Strategy

**Date:** 2026-04-08
**Scope:** Unified architecture connecting Retool (Perplexity Sonar research + content generation) with Claude Code (QA, SEO optimization, publishing)

---

## Executive Summary

The goal is a **hybrid system** where:
- **Retool** = Human-operated research + content generation interface (Perplexity Sonar → Brief → Article HTML)
- **Claude Code** = Automated QA, SEO optimization, internal linking, and publishing layer
- **Blog SEO Pipeline Plugin** = Orchestration bridge (repository of skills, templates, and QA rules)
- **PostgreSQL (RetoolDB)** = Central artifact store (research dossiers, briefs, articles, approvals, published content)

The pipeline flows:
```
Retool Research Lab (Perplexity Sonar)
         ↓
  Research Dossier (JSON → PostgreSQL)
         ↓
Retool Content Factory (DeepSeek brief + Claude Sonnet article)
         ↓
  Article HTML + Brief (live Retool state → can be persisted to PostgreSQL)
         ↓
Claude Code Skills (QA, Optimize, Publish)
         ↓
PostgreSQL (final article + publish status)
         ↓
WordPress REST API (live blog)
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
4. Brief generation (DeepSeek) → saved to Retool state (+ optionally PostgreSQL)
5. Article generation (Claude 3.5 Sonnet) → returned as HTML (currently ephemeral)

**Artifacts Produced:**
- Research dossier (JSON) → `research_dossiers` table
- Strategic brief (markdown) → Retool state + optional DB
- Article HTML → Retool textarea (not yet persisted)
- Selected products list (JSON) → Retool state

**Integration Point:** All artifacts are accessible via Retool API (or can be exported/saved to PostgreSQL)

---

### Layer 2: Claude Code Skills (Codex-side QA & Optimization)
**New Skills to Build:** (in `plugins/blog-seo-pipeline/skills/`)

#### Skill 1: `/research-deep [topic]`
**Purpose:** Alternative to Retool Research Lab (for power users)
**Input:** Bastelschachtel topic keyword + optional Perplexity API key
**Output:** Research dossier (JSON) + save to PostgreSQL
**Integration:** Can skip Retool if user wants direct Codex workflow

#### Skill 2: `/qa-article [dossier_id] [article_file]`
**Purpose:** QA a generated article against research + brief
**Input:** PostgreSQL dossier ID + article file path
**Output:** QA report + revision plan
**Uses:** blog-seo-pipeline QA engine + context files (seo-guidelines, style-guide, writing-examples)
**Modes:** Deep mode (detailed) or quick mode (priority issues only)

#### Skill 3: `/optimize [article_file]`
**Purpose:** Apply SEO + internal linking + style fixes
**Input:** Article markdown/HTML file
**Output:** Optimized article + change summary
**Uses:** target-keywords.md, internal-links-map.md, style-guide.md, writing-examples.md
**Focus:**
- Keyword placement (H1, first 100 words, conclusion)
- Internal linking strategy (4-6 contextual links)
- Meta elements (title 50-60 chars, description 150-160 chars)
- Readability (sentence length, paragraph structure, active voice)
- German grammar validation

#### Skill 4: `/publish [article_file] [status]`
**Purpose:** Publish to WordPress + track in PostgreSQL
**Input:** Article file + optional publication status (draft, published, scheduled)
**Output:** WordPress post URL + status in PostgreSQL
**Uses:** WordPress REST API + Yoast SEO integration
**Hooks:** Update `published_articles` table with post_id, publication_date, content_hash

#### Skill 5: `/audit-brief [dossier_id] [brief_file]`
**Purpose:** Validate brief before article generation
**Input:** Research dossier + brief markdown
**Output:** Brief audit report + improvement suggestions
**Prerequisite:** Run before sending to Retool Content Factory for article generation

---

### Layer 3: Blog SEO Pipeline Plugin (Orchestration & Rules)
**Location:** `plugins/blog-seo-pipeline/`
**Responsibility:** Central repository for:
- Skills definitions (with MCP integration)
- QA templates + rules
- SEO inference rules (from seo-guidelines.md)
- Content family templates (deep-dive, listicle, etc.)
- Retool integration contract + API adapters

**Key Files to Create/Update:**
- `skills/` → All 5 skills (as .md files with frontmatter + prompts)
- `hooks.json` → PostPublish hooks (update PostgreSQL on WordPress publish)
- `.mcp.json` → Perplexity + Retool API connections (for direct research calls)
- `integration/retool-api-adapter.py` → Read-only bridge to Retool PostgreSQL
- `integration/wordpress-api-adapter.py` → Publish + Yoast metadata

---

### Layer 4: PostgreSQL / RetoolDB (Central Artifact Store)
**Current Tables:**
- `research_dossiers` (topic, research_type, result_json, status)
- Optionally: `content_briefs` (brief_text, primary_keyword, awareness_stage)
- Optionally: `articles` (article_markdown, status, wordpress_post_id)
- `published_articles` (NEW) → Track final published content + metrics

**Extended Schema (Proposed):**
```sql
-- Final content tracking
CREATE TABLE published_articles (
  id INTEGER PRIMARY KEY,
  keyword TEXT,
  wordpress_post_id INTEGER,
  article_markdown TEXT,
  published_date TIMESTAMP,
  content_hash VARCHAR(64),  -- for duplicate detection
  seo_score INTEGER,
  traffic_30d INTEGER,
  status ENUM('draft', 'published', 'archived')
);

-- Job state tracking
CREATE TABLE content_jobs (
  id INTEGER PRIMARY KEY,
  topic TEXT,
  research_dossier_id INTEGER,
  brief_id INTEGER,
  article_id INTEGER,
  qa_status ENUM('pending', 'passed', 'revisions_needed'),
  qa_report LONGTEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

---

## End-to-End Workflows

### Workflow A: Retool-First (Current Production)
1. **Retool Research Lab:** User researches keyword → saves dossier to PostgreSQL
2. **Retool Content Factory:** User generates brief + article HTML
3. **Claude Code `/qa-article`:** User runs skill on article → gets QA report
4. **Claude Code `/optimize`:** User runs skill → receives optimized article
5. **Claude Code `/publish`:** User publishes to WordPress + PostgreSQL updated

**Advantage:** User controls pacing + model selection
**Duration:** ~30 minutes (research → publication)

### Workflow B: Pure Codex (Power Users)
1. **Claude Code `/research-deep [topic]`:** Direct research with Perplexity
2. **Retool Content Factory:** Generate brief + article (or skip to Codex generation)
3. **Claude Code `/qa-article`** → **`/optimize`** → **`/publish`** (chained)

**Advantage:** No context switching between tools
**Duration:** ~15 minutes (fully automated)

### Workflow C: Hybrid (Recommended)
1. **Retool Research Lab** → research dossier saved to PostgreSQL
2. **Retool Content Factory** → generate brief + article
3. **Claude Code `/audit-brief`** (optional: validate brief quality before article generation)
4. **Retool Content Factory** → generate article
5. **Claude Code `/qa-article`** (auto-triggered or manual)
6. **Claude Code `/optimize`** (auto-triggered or manual)
7. **Claude Code `/publish`** (manual approval before publishing)

**Advantage:** Best of both worlds (Retool research rigor + Codex automation)

---

## Integration Points

### Retool ↔ Claude Code
**Read-only bridge (MCP):**
- Fetch research dossier from PostgreSQL
- Fetch saved briefs (if persisted)
- Query published articles + metrics
- Validate keyword against PostgreSQL dossier history

**Write bridge (for publishing):**
- Save optimized article to PostgreSQL
- Update published_articles table
- Log QA results to content_jobs table

### Claude Code ↔ PostgreSQL
**Connection:** DATABASE_URL environment variable (already configured in .env)
**Operations:**
- SELECT research dossiers (read-only)
- SELECT published articles (read for deduplication checks)
- INSERT/UPDATE published_articles (after successful publish)
- INSERT/UPDATE content_jobs (track workflow state)

### Claude Code ↔ WordPress
**Connection:** WordPress REST API + Yoast SEO plugin
**Operations:**
- POST /wp-json/wp/v2/posts (create/publish article)
- POST /wp-json/wp-seo/v1/posts/{id}/meta (Yoast fields: focus keyword, SEO title, meta description)
- GET /wp-json/wp/v2/posts (check for duplicates)

### Retool ↔ Perplexity Sonar
**Connection:** Existing (in Retool Research Lab)
**Alternative:** Claude Code can call Perplexity API directly if `/research-deep` skill is used

---

## Context Files Integration

**All 9 context files created earlier become:**
- **Part of Claude Code skill prompts** (baked into `/qa-article`, `/optimize`, `/publish`)
- **Reference for Retool operations** (user can check style-guide.md before writing prompt in Content Factory)
- **QA templates** (master-reference.md, seo-guidelines.md drive what passes QA)

**Specific mappings:**
- `target-keywords.md` → `/optimize` uses for keyword placement validation
- `seo-guidelines.md` → `/qa-article` + `/optimize` check content structure
- `style-guide.md` → `/optimize` validates tone, sentence length, German grammar
- `internal-links-map.md` → `/optimize` auto-generates internal linking plan
- `writing-examples.md` → `/qa-article` compares against Bastelschachtel voice patterns
- `master-reference.md` → `/publish` confirms strategic context before publishing

---

## Phased Implementation

### Phase 1: Foundation (Week 1)
- [ ] Create PostgreSQL schema for published_articles + content_jobs tables
- [ ] Build integration/retool-api-adapter.py (read-only Retool DB access)
- [ ] Build integration/wordpress-api-adapter.py (REST + Yoast)
- [ ] Document PostgreSQL + API credentials in .env

### Phase 2: Core Skills (Week 2)
- [ ] Create `/qa-article` skill (QA engine + templates)
- [ ] Create `/optimize` skill (SEO + internal linking)
- [ ] Create `/publish` skill (WordPress + PostgreSQL write)
- [ ] Add MCP connections to `.mcp.json`

### Phase 3: Retool Integration (Week 3)
- [ ] Create Retool API adapter for fetching dossiers
- [ ] Test workflow A (Retool → Claude Code → publish)
- [ ] Create workflow documentation
- [ ] Add hooks.json for post-publish automation

### Phase 4: Extended Skills (Week 4)
- [ ] Create `/research-deep` skill (optional Perplexity integration)
- [ ] Create `/audit-brief` skill (brief validation pre-article)
- [ ] Chain skills for Workflow B + C
- [ ] Performance testing + optimization

---

## Why This Architecture

1. **Preserve Retool as operator interface:** Keeps research + brief generation flexible, human-controlled
2. **Automate QA + optimization:** Claude Code specializes in detailed analysis + refinement (where it excels)
3. **Central PostgreSQL store:** Single source of truth for all artifacts + publish state
4. **MCP/API bridges:** Retool and Claude Code work independently but stay in sync
5. **Context files drive behavior:** All guidelines/patterns live in repo, not scattered in prompts
6. **Scaling path:** Easy to add more skills (e.g., email marketing variant, social media summarizer) without touching core

---

## Success Metrics

**Phase 1-2 (Foundation):**
- ✅ Can run `/qa-article` on Retool-generated article
- ✅ Can run `/optimize` and receive improved version
- ✅ Can run `/publish` and verify WordPress post + PostgreSQL update

**Phase 3 (Integration):**
- ✅ Workflow A complete (Retool → Claude → publish in <30 min)
- ✅ QA catch rate: 95%+ of real issues (tested against manual review)
- ✅ Optimize success rate: 90%+ of articles improve on readability + SEO metrics

**Phase 4 (Extended):**
- ✅ Workflow B + C fully functional
- ✅ Monthly article volume: 10-15 pieces
- ✅ Owned-channel traffic increase: measurable within 8-12 weeks

---

## Next Immediate Steps

1. **Read integration/retool-api-reality-check.md** to understand current API limitations
2. **Check if Retool PostgreSQL is live** (or need to set up export/API layer)
3. **Decide:** Start with Skill creation (Phase 2) or DB schema first (Phase 1)?
4. **Select initial skill to build:** `/qa-article` is highest-value, lowest risk

---

*Integration strategy document for Bastelschachtel SEO content pipeline*
*Architecture: Retool (research + generation) + Claude Code (QA + optimization) + PostgreSQL (artifacts)*
