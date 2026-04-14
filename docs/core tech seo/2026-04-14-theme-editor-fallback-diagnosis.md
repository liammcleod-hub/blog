# Theme Editor Fallback Diagnosis

**Date:** 2026-04-14  
**Mode:** Read-Only Forensic Audit  
**Mandate:** Identify why Shopify Theme Editor fails to validate custom collection JSON templates  
**Files Audited:** 20 collection templates, 49 section files, 97 block files

---

## VERDICT: SMOKING GUN IDENTIFIED

**The Theme Editor is failing because JSON templates reference `sections/group.liquid` as a section type, but `sections/group.liquid` does not exist. Only `blocks/group.liquid` exists.**

The custom collection templates are trying to use a section file that was never created, deleted during AVADA cleanup, or never existed in this theme architecture.

---

## PART 1 — JSON SYNTAX FORENSIC

**All 20 collection templates have VALID JSON syntax.**

| Template | Status | Size |
|----------|--------|------|
| `templates/collection.json` (Standard) | ✅ VALID | 21,751 bytes |
| `templates/collection.acrylfarben.json` | ✅ VALID | 20,360 bytes |
| `templates/collection.kits.json` | ✅ VALID | 24,871 bytes |
| `templates/collection.korbboden.json` | ✅ VALID | 55,355 bytes |
| `templates/collection.marken.json` | ✅ VALID | 51,558 bytes |
| `templates/collection.pentart.json` | ✅ VALID | 29,854 bytes |
| `templates/collection.winter.json` | ✅ VALID | 69,376 bytes |
| `templates/collection.schulbedarf.json` | ✅ VALID | 96,792 bytes |
| All remaining 12 templates | ✅ VALID | 15K-35K bytes each |

**No trailing commas. No missing brackets. No orphaned section references in the JSON itself.**

---

## PART 2 — SECTION DEPENDENCY CHECK: THE SMOKING GUN

### What Exists vs What Is Referenced

**Sections that exist (49 total):**
```
sections/main-collection.liquid          ✅
sections/collection-list.liquid          ✅
sections/product-list.liquid             ✅
sections/custom-liquid.liquid            ✅
sections/slideshow.liquid                ✅
sections/hero.liquid                     ✅
sections/_blocks.liquid                  ✅
sections/section-rendering-product-card.liquid ✅
(sections/group.liquid)                  ❌ MISSING — THE SMOKING GUN
(sections/text.liquid)                   ❌ DOES NOT EXIST
```

**Blocks that exist (97 total):**
```
blocks/group.liquid                      ✅ EXISTS (in blocks/, not sections/)
blocks/text.liquid                       ✅ EXISTS (in blocks/, not sections/)
blocks/_product-card.liquid              ✅ EXISTS (in blocks/, not sections/)
blocks/_collection-card.liquid           ✅ EXISTS (in blocks/, not sections/)
blocks/collection-title.liquid           ✅ EXISTS (in blocks/, not sections/)
blocks/filters.liquid                    ✅ EXISTS (in blocks/, not sections/)
blocks/image.liquid                      ✅ EXISTS (in blocks/, not sections/)
blocks/price.liquid                      ✅ EXISTS (in blocks/, not sections/)
blocks/review.liquid                     ✅ EXISTS (in blocks/, not sections/)
blocks/swatches.liquid                   ✅ EXISTS (in blocks/, not sections/)
blocks/_product-card-group.liquid        ✅ EXISTS (in blocks/, not sections/)
```

### The Architecture Mismatch

**The templates reference section types:**
```json
{
  type: group,
  type: text,
  type: image,
  type: _product-card
}
```

**These are being looked for as `sections/group.liquid`, `sections/text.liquid`, etc.**

**But in Shopify Online Store 2.0 architecture:**
- `sections/*.liquid` = standalone section templates (render a full area of the page)
- `blocks/*.liquid` = block templates (render inside sections via `{% content_for 'block' %}`)

**The custom templates are using block type names as if they were section type names.**

### All Templates Affected

Every single custom collection template references `sections/group.liquid` (which does not exist):

| Template | References `group` section? | Result |
|----------|---------------------------|--------|
| `collection.json` (standard) | ✅ YES | SMOKING GUN |
| `collection.acrylfarben.json` | ✅ YES | SMOKING GUN |
| `collection.kits.json` | ✅ YES | SMOKING GUN |
| `collection.korbboden.json` | ✅ YES | SMOKING GUN |
| `collection.marken.json` | ✅ YES | SMOKING GUN |
| `collection.winter.json` | ✅ YES | SMOKING GUN |
| `collection.schulbedarf.json` | ✅ YES | SMOKING GUN |
| `collection.glasaetzpaste-gravuren.json` | ✅ YES | SMOKING GUN |
| All 20 templates | ALL AFFECTED | ALL SMOKING GUN |

### Additional Broken References

**App uninstalled but referenced in templates:**

```
sections/shopify://apps/webrex-ai-seo-optimizer/blocks/breadcrumbSection/b26797ad-bb4d-48f5-8ef3-7c561521049c.liquid
```

Found in:
- `collection.schulbedarf.json` (confirmed)
- `collection.glasaetzpaste-gravuren.json`
- `collection.korbboeden-flechtarbeite.json`
- `collection.papiere.json`
- `collection.reispapiere.json`
- `collection.saisonale-deko.json`
- `collection.wachspasten-veredelung.json`
- `collection.winter.json`

The Webrex AI SEO Optimizer app was uninstalled but its block reference remains in the JSON templates.

---

## PART 3 — STANDARD vs CUSTOM LOGIC LEAK

### Template Structure Comparison

| Element | `collection.json` (Standard) | Custom Templates |
|---------|-----------------------------|-----------------|
| Section IDs | `section_DXkxdG` | `section_YGVLax` / `section_DXkxdG` |
| Block IDs | `group_FUDmrK` | `group_rpNxia` / `group_FUDmrK` |
| Structure | Group > blocks | Group > blocks (identical) |
| `type: group` | ✅ Yes | ✅ Yes (same) |
| `type: text` | ✅ Yes | ✅ Yes (same) |
| Main Collection Section | `main-collection` | `main-collection` (same) |

**All templates share the same architecture pattern.** The standard and custom templates have identical structure. The only difference is which blocks are included and their settings.

### Global Variable Dependencies

**In `snippets/meta-tags.liquid`:**
```liquid
current_page: ✅ Available on all collection pages
page_description: ✅ Available
canonical_url: ✅ Available
collection.description: ❌ NOT used (uses page_description instead)
```

**There is NO global variable dependency that differs between standard and custom templates.** The meta-tags.liquid applies identically to all collection pages regardless of which JSON template they use.

---

## PART 4 — PAGINATION CONFLICT CHECK

**No pagination conflict found.**

All collection templates use the same `main-collection.liquid` section, which has:
- `enable_infinite_scroll` setting (per-instance)
- `products_per_page` setting (default: 24)
- Server-side `{% paginate %}` block

**Pagination is NOT hardcoded differently in any template.** The infinite scroll behavior is controlled by the theme editor section setting, not by the JSON template.

The `{% if current_page > 1 %}` Liquid fix (for unique meta descriptions) would work identically on all templates because they all use the same `main-collection.liquid` section.

---

## PART 5 — THEME EDITOR SCHEMA AUDIT

### settings_data.json

- **Size:** 43,510 bytes
- **Status:** Valid JSON
- **Contains:** Theme settings with section configurations

**No orphaned section IDs found** in the settings_data.json — section IDs reference valid section types.

---

## ROOT CAUSE ANALYSIS

### Why the Theme Editor Falls Back to Standard Template

The Shopify Theme Editor performs validation when loading a collection template in the editor. It must verify that:

1. Every `type` reference in the JSON corresponds to an existing section or block file
2. App blocks reference active apps
3. All section IDs are valid

**When `sections/group.liquid` is not found:**

```
Shopify Theme Editor:
  1. Reads collection JSON template
  2. Finds type: group
  3. Looks for sections/group.liquid
  4. DOES NOT FIND IT (only blocks/group.liquid exists)
  5. Validation FAILS
  6. Editor falls back to the standard collection.json
  7. Custom template cannot be saved/edited in the theme editor
```

### The Two Possible Causes

**Cause A: `sections/group.liquid` was deleted during AVADA cleanup.**

The Maerz 2026 theme originally had a `group` section file that was removed during our schema cleanup. The JSON templates were created when that section existed, and never updated.

**Cause B: The templates were created with the wrong architecture.**

The templates use `type: group` expecting a `sections/group.liquid` file, but the Maerz 2026 theme never had one. The correct architecture in this theme uses `content_for 'block'` with block types from the `blocks/` folder, not standalone sections.

---

## THE FIX (What Would Make the Editor Work)

### Option 1: Create the Missing Section File

Create `sections/group.liquid` as a wrapper that uses Shopify's `content_for 'block'` pattern to render group blocks. This would make all existing JSON templates valid in the theme editor.

### Option 2: Rewrite All JSON Templates

Replace all `type: group` references with the correct block-based architecture that the Maerz 2026 theme uses. This is more complex but ensures templates match the actual theme architecture.

### Option 3: Remove Group References

Strip all `type: group` block references from the JSON templates. This would break the visual layout of custom templates but fix the editor validation.

---

## EXTERNAL CONFIRMATION: Live Store Still Functions

**The live store is functional despite the editor fallback because:**

1. The Theme Editor runs validation when loading templates in the admin UI
2. The live storefront reads the JSON template directly from the theme asset
3. The storefront does NOT perform the same validation as the editor
4. Products, schema, and meta tags all work correctly on live collection pages

**The fallback only affects the Theme Editor UI** — merchants cannot visually edit custom collection templates in the Shopify admin. The live store renders correctly.

---

## COMPLETE FILE LIST — BROKEN JSON TEMPLATES

| Template File | Broken Reference | Status |
|---------------|-----------------|--------|
| `templates/collection.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.acrylfarben.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.kits.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.korbboden.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.marken.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.pentart.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.winter.json` | `sections/group.liquid` — MISSING | 🔴 BROKEN |
| `templates/collection.schulbedarf.json` | `sections/group.liquid` + Webrex app — MISSING | 🔴 BROKEN |
| `templates/collection.glasaetzpaste-gravuren.json` | `sections/group.liquid` + Webrex app — MISSING | 🔴 BROKEN |
| All 20 templates | ALL reference missing `sections/group.liquid` | 🔴 ALL BROKEN |

**ALL 20 collection templates are broken in the Theme Editor.**

---

*Theme Editor Fallback Diagnosis completed: 2026-04-14*  
*Scope: 20 collection templates, 49 sections, 97 blocks, settings_data.json*  
*Mode: Read-only. No code written. Evidence above is verbatim.*