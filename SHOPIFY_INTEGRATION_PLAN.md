# Shopify Integration Plan — Bastelschachtel Blog SEO Pipeline

**Date:** 2026-04-08
**Platform:** Shopify (not WordPress)
**Blog URL:** https://www.bastelschachtel.at/blogs/uebersicht/

---

## Key Findings

- Shopify blog posts use **HTML blocks** (not markdown), rendered via Shopify's theme system
- Content stored in **Shopify GraphQL** or REST API (not local files or PostgreSQL directly)
- Structure: `/blogs/{handle}/{article-handle}` URLs
- Theme: Horizon v3.2.1 with JSON-LD schema + Judge.me reviews
- Publishing: Via Shopify admin or API

---

## Best Starting Point: Shopify REST API Integration

### Phase 1A: Shopify API Adapter (FOUNDATION)

**Purpose:** Read/write blog articles via Shopify REST API

**What to build:**
1. **`integration/shopify-api-adapter.py`** — Read-only article fetch
   - Fetch article by handle
   - Parse HTML content
   - Extract metadata (title, description, image, tags)
   - Convert to working markdown (for Claude analysis)

2. **`integration/shopify-article-schema.md`** — Document expected fields
   - Title, body_html, author, published_at, image, tags, etc.

3. **Shopify credentials in `.env`:**
   - `SHOPIFY_STORE_URL` (e.g., bastelschachtel.myshopify.com)
   - `SHOPIFY_ACCESS_TOKEN` (REST API token)

**Why this first:**
- Unlocks ability to fetch + analyze existing articles
- Enables `/qa-article` to work with real Shopify content
- Simple foundation before building write operations

---

## Skill Building Order (Phases 2-4)

### Phase 2: `/qa-article [article-handle]`
- Fetch article from Shopify
- Compare against Bastelschachtel context (seo-guidelines, style-guide, writing-examples)
- Produce QA report (structure, SEO, tone, internal linking)
- Output: QA report (no modifications yet)

### Phase 3: `/optimize [article-handle]`
- Fetch article from Shopify
- Apply fixes: keyword placement, internal links, readability, German grammar
- Build revised article (HTML)
- Output: Revised article (requires manual approval before publishing)

### Phase 4: `/publish [article-handle]`
- Accept revised HTML
- Update Shopify article via REST API
- Update meta title, description, image alt text
- Update published_date (if new article)
- Track in PostgreSQL `published_articles` table
- Output: Shopify article URL + success confirmation

---

## Why This Order Works

✅ **Phase 1A (Adapter):** No risk. Just reads data. Enables testing.
✅ **Phase 2 (QA):** Uses adapter. Analyzes content. No writes. Safe to test heavily.
✅ **Phase 3 (Optimize):** Still read-only Shopify (revisions in memory). Easy to review before publish.
✅ **Phase 4 (Publish):** Only write when user explicitly approves revised article.

---

## Key Implementation Details

### Shopify Blog Post Structure
```html
<h1>Korbflechten mit Peddigrohr für Anfänger: Material, Stärke und erste Schritte</h1>
<p>[introduction paragraphs]</p>

<h2>Quick Answer Section</h2>
<p>[summary]</p>

<h2>What is Peddigrohr?</h2>
<p>[definition]</p>

<!-- more H2/H3 sections + lists + tables -->

<h2>FAQ</h2>
<dl>
  <dt>Q1?</dt>
  <dd>A1</dd>
</dl>
```

**Conversion strategy:**
- Parse HTML → Extract structure
- Analyze headings + content blocks
- Generate markdown representation (for Claude)
- Reverse: Revised markdown → HTML (for Shopify update)

### Shopify REST API Endpoints
```
GET /admin/api/2024-01/blogs/{blog-id}/articles/{article-id}
PUT /admin/api/2024-01/blogs/{blog-id}/articles/{article-id}
GET /admin/api/2024-01/articles.json (list all)
POST /admin/api/2024-01/articles.json (create)
```

---

## Success Criteria for Phase 1A

✅ Can fetch Bastelschachtel Peddigrohr article by handle
✅ Can parse HTML + extract title, body, metadata
✅ Can convert to markdown for analysis
✅ Can reverse-convert markdown back to HTML
✅ Shopify credentials stored securely in .env

---

*This plan avoids WordPress complexity entirely. Shopify API is simpler, and we control the blog directly via REST API.*
