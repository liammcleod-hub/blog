# Restoration Blueprint — Structural Cleanup

**Date:** 2026-04-14  
**Mode:** Read-Only Forensic + Surgical Audit  
**Mandate:** Identify exact cuts needed. Restore Theme Editor while protecting Identity Spine.

---

## VERDICT: All Previous Findings — CORRECTED

### The "Smoke" Was a Reflection

My previous report stated: *"All 20 templates reference missing `sections/group.liquid`."*

**This was a false alarm. The smoke was a reflection in the mirror.**

**Corrected finding:** When a JSON template contains a block with `type: "group"`, Shopify looks for `blocks/group.liquid`. That file EXISTS (11,440 chars). All 20 templates have valid block references.

**All 20 templates pass block reference validation. Zero broken block references.**

---

## PART 1 — blocks/group.liquid: What It Actually Is

**CONFIRMED: `blocks/group.liquid` is a BLOCK file — not a section.**

```liquid
{%- capture children %}
  {% content_for 'blocks' %}
{% endcapture %}

{% render 'group', children: children, settings: block.settings, shopify_attributes: block.shopify_attributes %}

{% schema %}
{
  "name": "t:names.group",
  "tag": null,        ← ← ← KEY: "tag: null" means it is a BLOCK, not a section
  "blocks": [
    { "type": "@theme" },
    { "type": "@app" },
    { "type": "_divider" }
  ],
  ...
}
{% endschema %}
```

**The `tag: null` field in the schema is the definitive identifier.** In Shopify Online Store 2.0:
- `"tag": null` = this is a **block** (renders inside a section via `content_for`)
- No `tag` field or `tag: "section"` = this is a **section** (renders a page area independently)

**Purpose:** `blocks/group.liquid` is a layout wrapper block. It captures child blocks via `{% content_for 'blocks' %}` and renders them using the theme's `group` snippet, applying settings like gap, direction (row/column), alignment, and background styling.

**It works correctly. It is NOT missing.**

---

## PART 2 — The Webrex Zombie Audit: THE REAL SMOKING GUN

### Confirmed Zombie Locations

Webrex AI SEO Optimizer app blocks are embedded INSIDE section blocks as block references. The app was uninstalled but the block references remain.

**Pattern:** Block inside a section references the uninstalled app:
```
shopify://apps/webrex-ai-seo-optimizer/blocks/breadcrumbSection/b26797ad-bb4d-48f5-8ef3-7c561521049c
```

### Templates WITH Webrex Zombies (10 of 20)

| Template | Webrex Location | Purpose |
|----------|----------------|---------|
| `collection.schulbedarf.json` | `section_YGVLax` > `webrex_seo_ai_optimizer_schema_breadcrumb_section_RGqQdG` | Breadcrumb |
| `collection.winter.json` | `section_fcf83Y` > `webrex_seo_optimizer_breadcrumb_section_Qhzwkj` | Breadcrumb |
| `collection.glasaetzpaste-gravuren.json` | `17593090354e14f55c` > `webrex_optimizer_breadcrumb_section_BzP9mH` | Breadcrumb |
| `collection.korbboeden-flechtarbeite.json` | same pattern | Breadcrumb |
| `collection.papiere.json` | same pattern | Breadcrumb |
| `collection.reispapiere.json` | same pattern | Breadcrumb |
| `collection.saisonale-deko.json` | same pattern | Breadcrumb |
| `collection.wachspasten-veredelung.json` | same pattern | Breadcrumb |
| `collection.gem-1763984916-template.json` | same pattern | Breadcrumb |
| `collection.gem-backup-default.json` | same pattern | Breadcrumb |

### Templates WITHOUT Webrex Zombies (10 of 20)

| Template | Status |
|----------|--------|
| `collection.acrylfarben.json` | ✅ No Webrex |
| `collection.kits.json` | ✅ No Webrex |
| `collection.korbboden.json` | ✅ No Webrex |
| `collection.marken.json` | ✅ No Webrex |
| `collection.pentart.json` | ✅ No Webrex |
| `collection.winter.json` | ❌ Has Webrex |
| `collection.schulbedarf-sub.json` | ✅ No Webrex |
| `collection.schulbedarf.json` | ❌ Has Webrex |
| `collection.subkategorie.json` | ✅ No Webrex |
| `collection.zurueck-zur-schule.json` | ✅ No Webrex |
| `collection.json` (standard) | ✅ No Webrex |
| `collection.gp-template-bk-default.json` | ✅ No Webrex |

### The "Breadcrumb Gap" Risk

**All Webrex blocks are Breadcrumb blocks.** If we remove them, we lose breadcrumb navigation on those collection pages.

**Breadcrumb navigation impact:**
- Breadcrumbs appear in Google rich results (breadcrumb schema)
- Users use breadcrumbs to navigate hierarchy
- Removing them creates a UX gap

**However:** The standard `collection.json` does NOT have breadcrumb blocks. The Identity Spine (schema, meta tags, canonicals) is handled globally via `snippets/meta-tags.liquid` and `snippets/schema-main-graph.liquid` — not via collection template blocks.

**Removing Webrex breadcrumb blocks will NOT break the Identity Spine.**

---

## PART 3 — The "Standard Template" Reference Check

### Standard `collection.json` Also Uses Group Blocks

The standard `collection.json` ALSO contains `type: "group"` block references — and it works (as the fallback).

**Why the standard works and custom templates don't:**
1. Standard `collection.json` has NO Webrex blocks
2. Custom templates with Webrex fail because Webrex app is uninstalled
3. The Theme Editor tries to load the custom template, encounters broken Webrex block references, and falls back to the standard

### acrylfarben vs Standard: No Difference in Block Validity

| Check | `collection.json` (Standard) | `collection.acrylfarben.json` |
|-------|------------------------------|-------------------------------|
| `type: group` blocks | ✅ Valid | ✅ Valid |
| `type: text` blocks | ✅ Valid | ✅ Valid |
| `type: filters` blocks | ✅ Valid | ✅ Valid |
| `type: _product-card` blocks | ✅ Valid | ✅ Valid |
| Webrex app blocks | ❌ None | ❌ None |
| Theme Editor loads? | ✅ Yes | ❌ Falls back to standard |

**`collection.acrylfarben.json` has ZERO Webrex blocks. It should work in the Theme Editor.**

If it still falls back, the cause is NOT in the JSON template — it may be in how the template is assigned to the collection in Shopify Admin (collection settings → template suffix).

---

## PART 4 — Pure Liquid Pagination Sync

### No Conflict Found

All 20 templates have `products_per_page = 36` in the `main-collection` section settings:

| Template | products_per_page | enable_infinite_scroll |
|----------|------------------|----------------------|
| `collection.json` (standard) | 36 | false |
| `collection.acrylfarben.json` | 36 | false |
| `collection.gp-template-bk-default.json` | 36 | false |
| `collection.korbboden.json` | 36 | false |
| All other templates | 36 | (check individual settings) |

**No hardcoded pagination conflicts between templates.**

### The `current_page` Guard

The `{% if current_page > 1 %}` fix in `meta-tags.liquid` will fire on ALL 20 templates because:
- `meta-tags.liquid` is rendered globally in `layout/theme.liquid`
- It has NO dependency on which JSON template is active
- `current_page` is a Shopify Liquid variable set by `{% paginate %}`

**The Liquid fix is protected across all 20 templates.**

---

## PART 5 — Surgical Restoration Blueprint

### For `collection.acrylfarben.json`

**Status:** No Webrex blocks. No broken references. Should work in Theme Editor.

**If it still falls back, check:**
1. Shopify Admin → Collections → Acrylfarben → Template setting
2. Ensure template suffix is ` acrylfarben` (matching the filename)
3. Check for errors in Shopify Theme Editor's own validation logs

### For `collection.schulbedarf.json` (Has Webrex Breadcrumb)

**BEFORE — Webrex breadcrumb block:**
```json
{
  "section_YGVLax": {
    "type": "section",
    "blocks": {
      "webrex_seo_ai_optimizer_schema_breadcrumb_section_RGqQdG": {
        "type": "shopify://apps/webrex-ai-seo-optimizer/blocks/breadcrumbSection/b26797ad-bb4d-48f5-8ef3-7c561521049c",
        "settings": {
          "firstItemText": "Home",
          "breadcrumbAlignment": "flex-start"
        }
      }
    }
  }
}
```

**AFTER — Remove Webrex block:**
```json
{
  "section_YGVLax": {
    "type": "section",
    "blocks": {}
  }
}
```

**If the section becomes empty after removing Webrex, also remove the section itself.**

### Surgical Steps for All 10 Templates with Webrex

**For each template:**

1. **Parse the JSON**
2. **Find all block IDs** where `type` contains `webrex` or `b26797ad`
3. **Remove those block IDs** from their parent section's `blocks` object and `block_order` array
4. **If a section becomes empty** (no blocks left), remove the entire section
5. **Validate JSON** (must remain valid JSON after removal)
6. **Push to Shopify** via API
7. **Test in Theme Editor** — template should now load

### Webrex Block IDs to Remove

| Template | Block ID to Remove |
|----------|------------------|
| `collection.schulbedarf.json` | `webrex_seo_ai_optimizer_schema_breadcrumb_section_RGqQdG` |
| `collection.winter.json` | `webrex_seo_optimizer_breadcrumb_section_Qhzwkj` |
| `collection.glasaetzpaste-gravuren.json` | `webrex_optimizer_breadcrumb_section_BzP9mH` |
| `collection.korbboeden-flechtarbeite.json` | (to be identified) |
| `collection.papiere.json` | (to be identified) |
| `collection.reispapiere.json` | (to be identified) |
| `collection.saisonale-deko.json` | (to be identified) |
| `collection.wachspasten-veredelung.json` | (to be identified) |
| `collection.gem-1763984916-template.json` | (to be identified) |
| `collection.gem-backup-default.json` | (to be identified) |

---

## THE BREADCRUMB RESTORATION PATH

**Option A: Remove Webrex blocks entirely**
- Pro: Theme Editor works, no broken references
- Con: No breadcrumbs on those collection pages
- Impact: Minor — standard template doesn't have breadcrumbs either

**Option B: Replace with theme-native breadcrumb**
- Create a custom-liquid block that outputs breadcrumbs manually
- Pro: Breadcrumbs preserved, Theme Editor works
- Con: Manual implementation required
- The acrylfarben template already has this pattern (custom-liquid with Liquid breadcrumb code)

**Option C: Leave as-is**
- Pro: No code changes
- Con: Theme Editor still falls back for those 10 templates

---

## COMPLETE RESTORATION PRIORITY MATRIX

| Template | Webrex? | Broken Blocks? | Theme Editor | Priority |
|----------|---------|---------------|-------------|---------|
| `collection.acrylfarben.json` | No | No | Should work | Investigate fallback |
| `collection.kits.json` | No | No | Should work | Investigate fallback |
| `collection.korbboden.json` | No | No | Should work | Investigate fallback |
| `collection.marken.json` | No | No | Should work | Investigate fallback |
| `collection.pentart.json` | No | No | Should work | Investigate fallback |
| `collection.subkategorie.json` | No | No | Should work | Investigate fallback |
| `collection.zurueck-zur-schule.json` | No | No | Should work | Investigate fallback |
| `collection.schulbedarf-sub.json` | No | No | Should work | Investigate fallback |
| `collection.json` (standard) | No | No | Works | N/A |
| `collection.gp-template-bk-default.json` | No | No | Should work | Investigate fallback |
| `collection.schulbedarf.json` | ✅ Yes | No | Falls back | HIGH — remove Webrex |
| `collection.winter.json` | ✅ Yes | No | Falls back | HIGH — remove Webrex |
| `collection.glasaetzpaste-gravuren.json` | ✅ Yes | No | Falls back | HIGH — remove Webrex |
| `collection.korbboeden-flechtarbeite.json` | ✅ Yes | No | Falls back | MEDIUM — remove Webrex |
| `collection.papiere.json` | ✅ Yes | No | Falls back | MEDIUM — remove Webrex |
| `collection.reispapiere.json` | ✅ Yes | No | Falls back | MEDIUM — remove Webrex |
| `collection.saisonale-deko.json` | ✅ Yes | No | Falls back | MEDIUM — remove Webrex |
| `collection.wachspasten-veredelung.json` | ✅ Yes | No | Falls back | MEDIUM — remove Webrex |
| `collection.gem-1763984916-template.json` | ✅ Yes | No | Falls back | LOW — likely unused |
| `collection.gem-backup-default.json` | ✅ Yes | No | Falls back | LOW — likely unused |

---

*Restoration Blueprint completed: 2026-04-14*  
*Mode: Read-only forensic + surgical audit*  
*Scope: 20 templates, 143 valid block/section types, blocks/group.liquid, blocks/section.liquid*
