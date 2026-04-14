---
created: 2026-04-13
modified: 2026-04-13
status: active
source: Shopify theme assets (Maerz 2026) + theme editor sidebar
---

# DIY Theme Editor Mapping (Shopify)

## What you are seeing in the theme editor

When editing a specific `diy_experience` entry (example shown in the sidebar: `Diy Experience #Y8IGVHSI`), Shopify’s theme editor shows:

- Global theme sections (Header, Footer, announcement bar, etc.)
- Template-specific sections defined by the metaobject template `templates/metaobject/diy_experience.json`

The important point: this DIY experience is rendered via a metaobject template, not a normal Page template.

## Template used

- Theme: `Maerz 2026` (main)
- Theme ID: `196991385938`
- Template: `templates/metaobject/diy_experience.json`

Current structure of `templates/metaobject/diy_experience.json`:

- Four sections in order:
- A generic Horizon “section builder” section (`type: "section"`) used as “Bild mit Text”
- A second generic builder section (`type: "section"`) currently named/typed as a custom section
- A third generic builder section (`type: "section"`) currently used for materials/products
- The original full DIY renderer (`type: "master-diy-anleitung"`)

In the JSON, they appear as:

- `section_Hca4zN`: `type: "section"`
- `section_PQQgbR`: `type: "section"`
- `section_Hi3V48`: `type: "section"`
- `main`: `type: "master-diy-anleitung"`

## Sidebar item to asset mapping

Based on the sidebar you pasted:

- `DIY Experience (Standard)`
  - Shopify template: `templates/metaobject/diy_experience.json`

- `Vorlage: Bild mit Text`
  - This is `section_Hca4zN` in the template JSON
  - Section implementation file: `sections/section.liquid`
  - It is configured via JSON blocks (image + group + text/button blocks)
  - Crucially, its block settings are wired to the current metaobject using Shopify “dynamic sources” like:
    - `{{ closest.metaobject.diy_experience.hero_image.value }}`
    - `{{ closest.metaobject.diy_experience.title.value }}`
    - `{{ closest.metaobject.diy_experience.subtitle.value }}`
    - `{{ closest.metaobject.diy_experience.intro | metafield_tag }}`

- (New) Additional builder section
  - This is `section_PQQgbR` in the template JSON
  - Section implementation file: `sections/section.liquid`
  - Template order places it between the hero “Bild mit Text” and `Master DIY Content`
  - It is also wired to `diy_experience` fields via dynamic sources; the current JSON includes a dynamic heading for:
    - `{{ closest.metaobject.diy_experience.midpage_cta_heading.value }}`

- (New) Materials/products builder section
  - This is `section_Hi3V48` in the template JSON
  - Section implementation file: `sections/section.liquid`
  - It currently contains a `custom-liquid` block that loops `metaobject.materials_products.value` and renders a centered product grid (image/title/price).

- `Master DIY Content`
  - Section type: `master-diy-anleitung`
  - Section implementation file: `sections/master-diy-anleitung.liquid`
  - This is the “full metaobject render” section you’re keeping as the baseline/fallback.

- `Glassmorphism Controls`
  - Section implementation file: `sections/glassmorphism-controls.liquid`
  - Behavior: defines CSS variables on `:root` based on section settings (blur, gradient colors, border, animation speed)

- `Custom Liquid`
  - Section implementation file: `sections/custom-liquid.liquid`
  - Behavior: prints `section.settings.custom_liquid`

- `Trennlinie`
  - Section implementation file: `sections/divider.liquid`
  - Behavior: renders a styled divider via `snippets/divider` with spacing settings

- `Header`, `Ankündigungsleiste`, `Footer`, `E-Mail-Anmeldung`, `Richtlinien und Links`
  - These are global sections (header/footer groups), not unique to the DIY template.
  - Related theme assets that exist in the live theme:
    - `sections/header-group.json`, `sections/header.liquid`, `sections/header-announcements.liquid`
    - `sections/footer-group.json`, `sections/footer.liquid`, `sections/footer-utilities.liquid`
  - The exact “E-Mail-Anmeldung” implementation depends on which section type the footer group references.

## Two different ways the metaobject data is wired today

The current template uses two distinct data-binding approaches:

1. **Dynamic sources inside template JSON**
   - Used by the `type: "section"` builder section
   - References `closest.metaobject.diy_experience.*.value` inside the JSON settings strings
   - Advantage: merchants can rewire content sources in the theme editor without editing Liquid

2. **Direct Liquid access via `metaobject`**
   - Used by `sections/master-diy-anleitung.liquid`
   - Reads values like `metaobject.title`, `metaobject.steps.value`, etc.
   - Advantage: richer logic and custom rendering (including structured data output)

This split is normal, but it matters for maintenance: if you want “one source of truth”, you should be explicit about which layer owns which parts of the experience.

## Structured data behavior (current)

- `sections/master-diy-anleitung.liquid` emits a `HowTo` JSON-LD block.
- The generic builder `sections/section.liquid` currently contains a special-case `FAQPage` JSON-LD generator, but it only runs on the homepage with a hard-coded `section.id` check.
  - This means your DIY template will not automatically get FAQ schema unless you add it explicitly.

## What changed vs the earlier baseline

Earlier, the metaobject template contained only the `master-diy-anleitung` section.

Now, it includes an additional builder section (`type: "section"`) above it, wired to `diy_experience` fields using dynamic sources.

After the latest saves, it includes three builder sections (`type: "section"`) above it, for a total of four template sections.
