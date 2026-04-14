---
created: 2026-04-13
modified: 2026-04-13
status: active
---

# DIY Shopify Context

## Scope

This is a side project with overlap to the Bastelschachtel content and Shopify ecosystem.

The implementation is currently Shopify-native rather than stored in a local theme codebase. Theme, template, metaobject, and page-structure work currently lives in Shopify.

## Domains

- Primary storefront: `www.bastelschachtel.at`
- Shopify domain: `bastelschachtel.myshopify.com`
- Additional connected domains:
- `bastelschachtel.at`
- `bastelschachtel.com`
- Customer account primary domain: `account.bastelschachtel.at`

## Active Theme

- Theme name: `maerz 2026`

## Main Metaobject

- Name: `DIY Experience`
- Type: `diy_experience`

Purpose:
- This is the main reusable DIY instruction-set metaobject.
- It is associated with a page.
- It is intended to support multiple future DIY instruction sets.

## Nested / Supporting Metaobject

- Name: `DIY Individual Step`
- Type: `diy_individual_step`

Purpose:
- Used as the step-level content structure within a `diy_experience`.

## Current Working Goal

The current goal is to:

1. Restructure the page template associated with the DIY Experience content.
2. Improve the visual presentation so the page looks substantially better.
3. Ensure the setup works reliably.
4. Improve the structure from an SEO / GEO / schema perspective.
5. Make the customer-visible content and search-engine-visible structured data derive from the same underlying source of truth.
6. Link metaobjects, metafield definitions, theme code, and theme-editor dynamic sections so that when content changes, visible content and schema stay synchronized.

## Content Source Files

Current working source content is stored locally at:

`C:\Users\Hp\Documents\anothervault\01-Projects\bastelschachtel\Code\docs\templates`

Current files observed there:

- `diy-tutorial-template.md`
- `diy-kleiderbuegel-ausfuellung.md`
- `DIY Handykette selbst gestalten  Handyarmband mit Perlen.md`

These appear to be reference or drafting assets for Shopify-native DIY content.

## Current Constraint

There is no local theme codebase currently available in this repo for the DIY page template. Inspection and implementation work for the actual page template, sections, and schema output must therefore happen against Shopify-hosted theme assets and admin-managed content.

## Next Inputs Needed

To audit and improve the live implementation, the next useful inputs are:

- The exact page URL or handle using `diy_experience`
- The page template name assigned in Shopify
- The field list for `diy_experience`
- The field list for `diy_individual_step`
- Any page metafields that connect the page to the metaobject
- Whether FAQ schema, HowTo schema, or custom JSON-LD is already present
- Screenshots or exported theme/template structure from Shopify if direct theme code access is unavailable
