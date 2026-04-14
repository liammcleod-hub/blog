# Bastelschachtel Live SEO Audit
#seo

*Date: 2026-03-27*
*Domain audited: `https://www.bastelschachtel.at/`*
*Method: live browser inspection of homepage, blog, core collection pages, landing page, `robots.txt`, and `sitemap.xml`*

## Executive Summary

Bastelschachtel has a stronger SEO base than the earlier `.docx` suggested in one key respect: the blog is no longer empty. There is now a meaningful archive of 2025 posts, and the site has visible trust assets, strong category depth, and a clear Austria-specialist position.

The main SEO problem is now less "no content exists" and more "your strongest positioning is not consistently expressed in high-value search surfaces." The homepage underuses core search terms, several key templates have weak or missing H1s, some collection metadata is truncated or generic, and at least one important category URL returns a live 404.

The highest-leverage move is straightforward:
- make the homepage rankable for `Bastelbedarf Österreich` and `Kreativshop Österreich`
- turn core category pages into true search landing pages
- fix template-level heading/meta issues
- expand the strongest category and tutorial clusters around Pentart, Reispapier/Decoupage, Korbflechten, and casting molds

## What I Checked

- Homepage: `https://www.bastelschachtel.at/`
- Blog index: `https://www.bastelschachtel.at/blogs/uebersicht`
- Strong landing page: `https://www.bastelschachtel.at/pages/bastelbedarf`
- Key collections:
  - `https://www.bastelschachtel.at/collections/reispapier`
  - `https://www.bastelschachtel.at/collections/ihr-pentart-lieferant`
  - `https://www.bastelschachtel.at/collections/bastelsets`
- Crawl basics:
  - `https://www.bastelschachtel.at/robots.txt`
  - `https://www.bastelschachtel.at/sitemap.xml`

## Top Findings

### 1. Homepage search positioning is still too weak

Live findings:
- Title: `Bastelschachtel - der Online Kreativshop`
- H1: `Bastelschachtel`
- Meta description exists, but it is long, broad, and not tightly optimized for the highest-value terms.

Why this matters:
- The homepage is the best candidate for `Bastelbedarf Österreich`, `Kreativshop Österreich`, and brand-plus-category queries.
- Right now it underuses Austria, specialist authority, and category leadership in the title/H1.
- The hero copy on-page is elegant, but not aligned with the strongest commercial search terms.

Priority: Critical

### 2. The blog is active, but its index page is structurally weak

Live findings on `/blogs/uebersicht`:
- Title: `Blog | Bastelideen | Bastelschachtel.at`
- Meta description present, but awkwardly written and typo-prone.
- No visible H1 detected.
- Schema detected.
- There are many 2025 posts live, including content on glass etching, concrete, rice paper, and seasonal DIY.

Why this matters:
- This is no longer a "blog absent" problem.
- It is now a "blog under-optimized as a search entry point" problem.
- The archive needs a real H1 and a cleaner intro/meta so Google can understand the section better.

Priority: High

### 3. `/pages/bastelbedarf` is your strongest SEO model page

Live findings:
- Title: `Bastelbedarf – Bastelschachtel`
- Meta description is useful and category-specific.
- Strong long-form content present.
- Schema types detected: `HowTo`, `WebPage`, `FAQPage`, `BreadcrumbList`, `Organization`
- FAQ content is present.
- Despite that, no true H1 was detected in the rendered page.

Why this matters:
- This page is doing the right kind of work: category explanation, education, FAQs, and structured data.
- It is a clear model for future pages like `Pentart Österreich`, `Korbflechten Material kaufen`, `Reispapier kaufen`, and casting-mold pages.
- The main issue is finishing the on-page structure properly rather than reinventing the format.

Priority: High

### 4. Collection templates are inconsistent and in places under-optimized

#### `Reispapier`
- Title: `Reispapier – Bastelschachtel`
- H1 present: `Reispapier`
- Meta description is too long and appears truncated / malformed at the end.
- Content exists, which is good.

#### `Pentart Shop`
- Title: `Pentart Shop – Bastelschachtel`
- No H1 detected.
- Content exists.
- Several schema objects detected.

#### `Bastelsets`
- Title: `Bastelsets – Bastelschachtel`
- No H1 detected.
- Content exists.
- Schema present, but lighter than the stronger landing page.

Why this matters:
- The content depth is no longer the bottleneck on these pages.
- Template consistency is.
- If the collection template often fails to output a visible H1, that is a sitewide issue affecting many rankings.

Priority: High

### 5. There is at least one important category gap / broken route

Live finding:
- `https://www.bastelschachtel.at/collections/peddigrohr` returns a `404`

Why this matters:
- `Peddigrohr kaufen` is one of the clearest specialist-intent keywords for the business.
- The SEO audit `.docx` and your positioning both treat Peddigrohr / basket weaving as a core strength.
- A broken or missing obvious collection URL is a direct commercial SEO problem.

Priority: Critical

### 6. Crawl basics are fine

Live findings:
- `robots.txt` is standard Shopify and includes the sitemap reference.
- `sitemap.xml` exists and includes product, page, collection, blog, and metaobject sitemap indexes.

Why this matters:
- Crawlability is not the main current bottleneck.
- The next gains come from stronger page targeting, not infrastructure repair.

Priority: Low

### 7. Schema is unevenly deployed

Live findings:
- Homepage: only `Organization` schema detected.
- `/pages/bastelbedarf`: rich schema stack detected, including `HowTo` and `FAQPage`.
- Blog and collection pages have some schema, but not necessarily the richest or most useful variant for search presentation.

Why this matters:
- The site already proves richer schema is possible.
- The homepage and key collection pages are not getting the full benefit.

Priority: Medium

### 8. Trust assets are excellent and should be leaned on harder in search-facing copy

Live findings:
- `4.88 ★ (764)` visible on homepage
- `Mehr als 60.000 begeisterte Kunden`
- `Über 250.000 Ideen verwirklicht`
- `14 Tage Geld-zurück-Garantie`
- `Kostenloser Versand ab €70`
- direct phone / WhatsApp support

Why this matters:
- Many competitors can match assortment breadth.
- Fewer can match specialist authority plus local trust plus visible proof.
- These should be reflected more deliberately in title, meta, intro copy, and dedicated landing pages.

Priority: High

## Current SEO Strengths

- Clear category authority in Pentart, rice paper / Decoupage, Korbflechten, and related making categories
- Strong local differentiation as a small Austrian specialist
- Trust signals are visible and credible
- Blog exists and covers real category-relevant tutorials
- `/pages/bastelbedarf` already demonstrates a workable SEO content format
- Sitemap and robots setup are healthy

## Current SEO Weaknesses

- Homepage title and H1 are under-optimized
- Missing H1s on important templates
- Some collection metas are too long, truncated, or generic
- Commercial category gaps exist, including a live 404 on a relevant URL
- SEO effort is uneven: one or two strong pages, many weaker template-driven pages
- Homepage schema is thin compared with your best-performing informational page architecture

## Priority Actions

## 1. Critical: Fix homepage search positioning

Recommended homepage title direction:
`Bastelbedarf kaufen | Bastelschachtel - Kreativshop Österreich`

Recommended homepage H1 direction:
`Bastelbedarf kaufen - Österreichs Kreativshop für Pentart, Decoupage & Korbflechten`

Recommended homepage meta direction:
`Bastelbedarf aus Österreich: Pentart, Reispapier, Korbflechten, Bastelsets und kreative Spezialprodukte. 4.88★, persönliche Beratung, Versand ab 70€ frei.`

Why:
- this aligns the homepage with how people actually search
- it preserves the specialist angle
- it uses trust proof instead of generic branding language

## 2. Critical: Resolve Peddigrohr / Korbflechten URL strategy

Actions:
- decide the canonical ranking URL for Peddigrohr / basket-weaving intent
- make sure it returns 200, not 404
- align it with the keywords:
  - `Peddigrohr kaufen`
  - `Korbflechten Material kaufen`
  - `Peddigrohr Anfänger Set`
- add explanatory category copy and internal links from homepage, blog posts, and `/pages/bastelbedarf`

## 3. High: Fix H1 output on templates

Observed issue:
- blog index, Pentart collection, and Bastelsets collection did not expose a visible H1 in live rendering

Actions:
- audit the Shopify theme template for blog and collection headings
- ensure one visible H1 per template
- make the H1 keyword-specific, not just decorative

Suggested H1 examples:
- Blog: `Bastelideen, Anleitungen und DIY Tipps`
- Pentart collection: `Pentart kaufen - Farben, Pasten und Medien`
- Bastelsets: `Bastelsets für Einsteiger, Geschenke und kreative Projekte`

## 4. High: Standardize collection metadata

Observed issue:
- some collection titles are minimal
- some collection metas are too long or malformed

Actions:
- create a metadata standard for top collections
- prioritize:
  - Reispapier
  - Pentart
  - Bastelsets
  - Korbflechten / Peddigrohr
  - molds / casting

Metadata pattern:
- keyword first
- Austria / specialist trust where useful
- concise benefit statement
- no clipping or broken sentence endings

## 5. High: Turn your best categories into true search landing pages

Model to replicate:
- `/pages/bastelbedarf`

Pages to build or strengthen:
- `Pentart Österreich`
- `Reispapier / Decoupage Reispapier kaufen`
- `Korbflechten Material kaufen`
- `Silikonformen für Gips und Beton`
- `Bastelsets Österreich`

Template structure:
- clear H1
- short commercial intro
- category explainer
- buying guide
- FAQs
- internal links into products / collections
- schema where appropriate

## 6. High: Build tighter blog-topic clusters

You already have blog momentum. Now it needs structure.

Priority content clusters:
- Pentart tutorials
- glass etching tutorials
- Decoupage / rice paper tutorials
- basket weaving / Peddigrohr guides
- gypsum / concrete casting projects

Best format mix:
- beginner guides
- problem-solving posts
- seasonal project posts
- project roundups linking back into collections

Examples:
- `How to use glass etching paste without streaks`
- `How to choose the right Pentart product for wood, glass, and mixed media`
- `Rice paper Decoupage for beginners`
- `What you need to start basket weaving with Peddigrohr`
- `Casting with gypsum or concrete: best silicone molds and beginner mistakes`

## 7. Medium: Expand schema beyond the current high-performing page

Observed:
- homepage only exposes `Organization`
- `/pages/bastelbedarf` has materially better schema coverage

Actions:
- keep Organization schema
- add or improve:
  - `FAQPage` where visible FAQs exist
  - `BreadcrumbList` consistently
  - `CollectionPage` / `WebPage` level structure where appropriate
- test top collection pages in a rich results workflow after implementation

## 8. Medium: Use trust more aggressively in search copy

Current opportunity:
- visible proof is strong, but not consistently used in SEO-critical copy

Use more often in:
- homepage intro
- key category metas
- landing-page intros
- comparison / why-buy-here sections

Most useful trust themes:
- Austrian specialist
- family-run small business
- 4.88-star review base
- direct expert help
- fast shipping and guarantee

## Suggested Page-Level Next Moves

### Homepage
- rewrite title
- rewrite H1
- tighten meta description
- align hero with specialist search terms while keeping the brand tone

### `/pages/bastelbedarf`
- add or restore a real H1
- keep this page as the reference template for future SEO pages
- strengthen internal links to Pentart, Reispapier, Korbflechten, and molds

### `/blogs/uebersicht`
- add a real H1
- rewrite meta description in cleaner German
- add a short intro paragraph explaining what the blog covers

### `Reispapier`
- rewrite title to include purchase intent
- shorten and clean the meta description
- keep or expand the explanatory intro

Suggested direction:
- Title: `Reispapier kaufen | Decoupage Reispapier - Bastelschachtel`

### `Pentart Shop`
- ensure visible H1 exists
- rewrite title toward `Pentart kaufen` / `Pentart Österreich`
- add stronger specialist framing in intro copy

Suggested direction:
- Title: `Pentart kaufen | Pentart Österreich - Bastelschachtel`

### `Bastelsets`
- ensure visible H1 exists
- clarify whether this page is for beginner kits, giftable kits, or broad bundles
- align metadata with actual search demand, not just internal naming

## Suggested 30-Day SEO Sprint

### Week 1
- Fix homepage title, H1, and meta
- Fix blog index H1 and meta
- Confirm canonical Peddigrohr / Korbflechten landing URL

### Week 2
- Fix collection template H1 behavior
- Rewrite metadata for Pentart, Reispapier, Bastelsets, and Korbflechten pages

### Week 3
- Build or strengthen one landing page:
  - `Pentart Österreich`
  - or `Korbflechten Material kaufen`

### Week 4
- Publish 2-3 tightly targeted tutorial posts that internally link to the improved category pages

## Bottom Line

This is no longer a site with "no SEO foundation." It is a site with:
- genuine specialist authority
- real trust signals
- enough content to compete
- but inconsistent execution on search-critical templates

The gap is now operational, not conceptual.

If you fix homepage targeting, collection H1/meta consistency, and the broken Korbflechten/Peddigrohr search path, Bastelschachtel should be materially better positioned for its most realistic commercial keywords.

## Related Docs

- [[docs/seo/README]]
- [[docs/seo/seo-execution-checklist-2026-03-27|seo-execution-checklist-2026-03-27]]
- [[docs/seo/master-article-plan-2026-03-29|master-article-plan-2026-03-29]]
- [[docs/customer reviews/category-voc-priority-map|category-voc-priority-map]]

<!-- audit-date: 2026-04-14 -->

---
← [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO — Master Index]]
