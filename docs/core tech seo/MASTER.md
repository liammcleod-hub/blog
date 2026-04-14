# Bastelschachtel SEO & AEO/GEO — Master Index

**Date:** 2026-04-14  
**Status:** Active  
**Folders covered:** `docs/seo/`, `docs/core tech seo/`, `docs/diy/`  
**Total documents:** 23

---

## Purpose

This is the single entry point for the Bastelschachtel SEO, technical crawl forensics, and AEO/GEO schema documentation. Use it to navigate from high-level strategy down to forensic evidence — and back again.

**Start here.** Then follow wikilinks into the specific docs you need.

---

## Quick Status

| Area | Status | Best doc |
|------|--------|---------|
| SEO strategy & copy | ✅ Active (2026-03) | [[seo-copy-deck-2026-03-27]] |
| Technical crawl audit | ✅ Active (2026-04) | [[2026-04-14-operation-deep-crawl-vulnerability-report]] |
| Schema / AEO / GEO | ✅ FORTRESS LIVE (2026-04) | [[2026-04-13-schema-master-status]] |
| Internal validator | ✅ 5/5 proof points PASSED | [[2026-04-13-internal-validator-raw-evidence-report]] |

---

## docs/seo/ — Strategy & Execution

### [[docs/seo/README|README]]

Folder entry point. Start here. Covers purpose, recommended reading order, and how to use this folder.

### [[docs/seo/live-seo-audit-2026-03-27|Live SEO Audit — 2026-03-27]]

Live browser audit of bastelschachtel.at. Covers homepage, blog index, `/pages/bastelbedarf`, Pentart/Reispapier/Bastelsets collections, robots.txt, and sitemap.xml. 8 key findings with priority ratings.

Key findings: Homepage under-optimized for `Bastelbedarf Österreich`, missing H1s on collection templates, `/collections/peddigrohr` returns 404, blog index structurally weak, schema unevenly deployed, but trust assets are strong.

### [[docs/seo/master-article-plan-2026-03-29|Master Article Plan — 2026-03-29]]

Plan for 5 hub-style master articles to support core commercial categories. Includes recommended title direction, search intent targets, internal-link model, article format template, and recommended build order.

Priority: 1. Korbflechten/Peddigrohr → 2. Glasätzung → 3. Reispapier/Decoupage → 4. Gießen mit Gips & Beton → 5. Pentart.

### [[docs/seo/priority-category-intros-2026-03-29|Priority Category Intros — 2026-03-29]]

Ready-to-use intro copy for 6 priority categories: Pentart, Reispapier/Decoupage, Glasätzung, Silikonformen für Gips & Beton, Korbflechten/Peddigrohr, Bastelsets. Both short and longer variants for collection pages vs. landing pages.

### [[docs/seo/seo-copy-deck-2026-03-27|SEO Copy Deck — 2026-03-27]]

Full SEO copy package: title, meta description, H1, intro copy, body sections, FAQ prompts, and internal-link targets for 8 pages. Covers homepage, blog index, `/pages/bastelbedarf`, Pentart Shop, Reispapier, Bastelsets, Korbflechten/Peddigrohr, and Silikonformen für Gips & Beton.

### [[docs/seo/seo-execution-checklist-2026-03-27|SEO Execution Checklist — 2026-03-27]]

Phase-by-phase sprint checklist for implementing all audit findings. 10 phases from critical homepage fixes through schema expansion. Includes sprint structure, copy drafting queue, and success markers.

---

## docs/core tech seo/ — Technical Crawl Forensics

### [[docs/core tech seo/2026-04-14-operation-deep-crawl-vulnerability-report|Operation Deep Crawl — Forensic Vulnerability Report]]

Read-only forensic audit of the entire crawl architecture: sitemap XML, pagination meta trap, canonical leaks, noindex sweep, and robots.txt full disallow audit. Covers 267 liquid theme files.

6 confirmed vulnerabilities: sitemap product count breach (~1,700 products missing), pagination meta description trap (no `current_page` check), paginated canonical self-leak, faceted navigation canonical (PASS), zero noindex directives, search page noindex gap.

### [[docs/core tech seo/OPERATION-IRONCLAD-SCIENTIFIC-METHODOLOGY|Operation Ironclad — Scientific Methodology (LAW)]]

The governing LAW for all implementation. 7‑phase scientific method: KNOW → HYPOTHESIZE → STRESS TEST → ADVERSARIAL REVIEW → PROVE → IMPLEMENT → VERIFY. Mandates empirical proof before deployment, adversarial stress‑testing, and atomic reversibility.

**All Phase 3+ work must comply.**

### [[docs/core tech seo/2026-04-14-operation-ironclad-strategic-overview|Operation Ironclad — Strategic Overview]]

End‑to‑end campaign narrative showing how each phase builds toward DACH domination. Connects Technical SEO Core fixes to AEO/GEO layer implementation. References the Scientific Methodology LAW.

### [[docs/core tech seo/2026-04-14-operation-ironclad-verification-findings-sorted|Operation Ironclad — Verification Findings (Sorted)]]

Prioritized action plan with AEO/GEO alignment for each fix. Critical leaks identified: Bastelbedarf broken schema, HowTo not rendering, missing H1s, AVADA 404 scripts, missing DACH trust signals.

### [[docs/core tech seo/2026-04-14-operation-ironclad-lateral-extension-report|Operation Ironclad — Lateral Extension Report]]

"Going Wide" scan of 4 vectors: content bloat, asset rot, merchant identity, parameter explosion. Found: 9 orphaned AVADA snippets, 2 AVADA 404 scripts, missing DACH schema nodes.

### [[docs/core tech seo/2026-04-14-operation-clean-sweep-handoff|Operation Clean Sweep — Handoff Document]]

Step‑by‑step implementation instructions for Phase 3. Single‑source‑of‑truth for executing the full Clean Sweep without re‑auditing. Includes Webrex zombie nuke instructions, Pagination Trap fix, meta‑tags.liquid update.

---

## docs/diy/ — AEO/GEO Schema & DIY Pages

### [[docs/diy/2026-04-13-aeo-geo-framework|AEO/GEO Framework — 2026-04-13]]

Living reference for AI Engine Optimization (AEO) and Generative Engine Optimization (GEO). Covers identity graph architecture, schema.org types for Bastelschachtel (ArtSupplyStore, LocalBusiness, HowTo, FAQPage), NAP consistency, E-E-A-T signals, GDPR compliance, and implementation checklist.

Best doc for understanding the AEO/GEO strategy underpinning the entire FORTRESS schema deployment.

### [[docs/diy/2026-04-13-schema-master-status|Schema Master Status — FORTRESS LIVE]]

**The main status document.** FORTRESS v1 — 14/14 architectural checks passed, 5/5 Internal Validator proof points confirmed. Full identity graph architecture, sameAs trust circle, transactional bridge, AVADA ghost permanently nuked, GSC priority data, credentials, and growth-phase next steps.

Start here for the definitive state of the schema program.

### [[docs/diy/2026-04-13-schema-session-context|Schema Session Context — 2026-04-13]]

Quick reference card for new sessions. One-page summary of identity graph, theme renders, sameAs, transactional bridge, AVADA status, internal validator results, GSC priority data, and credentials. Designed to orient any new agent or session immediately.

### [[docs/diy/2026-04-13-schema-session-success|Session Success Summary — 2026-04-13]]

Session wrap-up document. Zero dangling threads confirmed. Lists every component built (3 schema snippets deployed), adversarial findings fixed, GSC data cleaned, credentials, and remaining growth-phase tasks.

### [[docs/diy/2026-04-13-schema-live-architecture|Schema Live Architecture Reference]]

Live, deployed FORTRESS architecture — not a plan. Theme render locations, entity ID spine, transactional bridge proof, sameAs circle, logo resolution, AVADA removal confirmation, and theme file locations. Independently validated 2026-04-13.

### [[docs/diy/2026-04-13-schema-live-gap-analysis|Live Gap Analysis — 2026-04-13]]

Current gap state at time of writing: FAQ page = GOLDEN, homepage = ⏳ blocked by AVADA cache. Root cause analysis of AVADA app embed injection system, what was done to fix it, and next steps.

### [[docs/diy/2026-04-13-store-wide-schema-audit|Store-Wide Schema Audit — 2026-04-13]]

Full store schema audit covering Organization, WebSite, LocalBusiness, FAQPage, HowTo, Product FAQ, and AVADA SEO Suite dashboard. AVADA scores 55/100, 378 broken links, 8.6s load time. All pages score 18–44 SEO. Critical actions identified.

### [[docs/diy/2026-04-13-internal-validator-raw-evidence-report|Internal Validator — Raw Evidence Report]]

Raw evidence from the Internal Validator Protocol. Verdict: FORTRESS IS LIVE — 5/5 proof points passed. Full JSON-LD raw extracts, Ghost Audit (zero AVADA Organization), ID Integrity check (character-for-character @id match), Transactional Bridge proof (exact acceptedAnswer.text with `<a href>`), canonical tag confirmation.

### [[docs/diy/2026-04-13-metadata-forgery-audit-bing-duplicate-descriptions|Metadata Forensic Audit — Bing 899 Duplicates]]

Investigation of Bing Webmaster Tools "899 Duplicate Meta Descriptions" alert. CSV deep-dive reveals 164-row subset, 45 unique description strings, multi-vector duplication pattern. Root cause confirmed: pagination trap (no `current_page` check) + product template content rot. Live DOM vs. CSV comparison shows partial resolution since crawl.

### [[docs/diy/2026-04-13-diy-faq-implementation-notes|DIY FAQ Implementation Notes — 2026-04-13]]

HowTo schema status (✅ DONE — `/handykette` and `/batik-tshirt` live), Product FAQ growth plan, DIY page FAQ expansion recommendation, and GSC-informed expansion targets. Transactional Bridge pattern confirmed (5 HTML links in FAQ acceptedAnswer.text).

### [[docs/diy/2026-04-13-diy-faq-setup-step-by-step|DIY FAQ Setup — Step by Step]]

Shopify admin step-by-step for wiring `product_faq` metaobjects into DIY experience pages. What was changed in the theme (already done), what the admin user needs to do (add `faq_items` field to `diy_experience` metaobject), and expected result once populated.

---

## Architecture Overview

```
docs/
├── seo/                              ← SEO STRATEGY & COPY
│   ├── README.md                      ← Folder entry point
│   ├── live-seo-audit-2026-03-27    ← Live audit (8 findings)
│   ├── master-article-plan-2026-03-29 ← 5 hub articles
│   ├── priority-category-intros-2026-03-29 ← 6 category intros
│   ├── seo-copy-deck-2026-03-27     ← Full copy for 8 pages
│   └── seo-execution-checklist-2026-03-27 ← 10-phase sprint
│
├── core tech seo/                     ← TECHNICAL CRAWL FORENSICS
│   ├── MASTER.md                     ← ← YOU ARE HERE
│   ├── 2026-04-14-operation-deep-crawl-vulnerability-report ← 6 vulnerabilities
│   └── OPERATION-IRONCLAD-SCIENTIFIC-METHODOLOGY           ← Implementation LAW
│
└── diy/                              ← AEO/GEO SCHEMA & DIY PAGES
    ├── 2026-04-13-aeo-geo-framework  ← AEO/GEO reference
    ├── 2026-04-13-schema-master-status ← FORTRESS status (start here)
    ├── 2026-04-13-schema-session-context ← Quick reference
    ├── 2026-04-13-schema-session-success ← Session wrap-up
    ├── 2026-04-13-schema-live-architecture ← Live architecture
    ├── 2026-04-13-schema-live-gap-analysis ← Gap analysis
    ├── 2026-04-13-store-wide-schema-audit ← Full store audit
    ├── 2026-04-13-internal-validator-raw-evidence-report ← Validator evidence
    ├── 2026-04-13-metadata-forgery-audit-bing-duplicate-descriptions ← Bing duplicate audit
    ├── 2026-04-13-diy-faq-implementation-notes ← HowTo + FAQ notes
    └── 2026-04-13-diy-faq-setup-step-by-step ← Admin setup steps
```

---

## Reading Order

### For SEO Strategy
1. [[docs/seo/README]] — folder entry
2. [[docs/seo/live-seo-audit-2026-03-27]] — audit findings
3. [[docs/seo/seo-copy-deck-2026-03-27]] — copy to implement
4. [[docs/seo/seo-execution-checklist-2026-03-27]] — execution tracker

### For Technical SEO / Crawl Issues
1. [[docs/core tech seo/2026-04-14-operation-deep-crawl-vulnerability-report]] — vulnerabilities
2. [[docs/diy/2026-04-13-metadata-forgery-audit-bing-duplicate-descriptions]] — Bing duplicate root cause

### For Technical Implementation (Operation Ironclad)
1. [[docs/core tech seo/OPERATION-IRONCLAD-SCIENTIFIC-METHODOLOGY]] — Implementation LAW (start here)
2. [[docs/core tech seo/2026-04-14-operation-ironclad-strategic-overview]] — Campaign narrative
3. [[docs/core tech seo/2026-04-14-operation-ironclad-verification-findings-sorted]] — Prioritized action plan
4. [[docs/core tech seo/2026-04-14-operation-clean-sweep-handoff]] — Step-by-step instructions

### For AEO/GEO / Schema
1. [[docs/diy/2026-04-13-aeo-geo-framework]] — strategy framework
2. [[docs/diy/2026-04-13-schema-master-status]] — definitive status (start here)
3. [[docs/diy/2026-04-13-internal-validator-raw-evidence-report]] — evidence
4. [[docs/diy/2026-04-13-schema-live-architecture]] — architecture reference

### For New Sessions
1. [[docs/diy/2026-04-13-schema-session-context]] — quick orient

---

## Key Stats

| Metric | Value |
|--------|-------|
| Total docs | 28 |
| SEO sprint phases | 10 |
| FORTRESS score | 14/14 ✅ |
| Internal Validator proof points | 5/5 ✅ |
| Confirmed crawl vulnerabilities | 6 |
| Schema snippets deployed | 3 |
| sameAs URLs verified | 8 |
| HowTo DIY pages live | 2 |
| FAQ HTML links in JSON-LD | 5 |

---

*Last updated: 2026-04-14 (Operation Ironclad methodology added)*
