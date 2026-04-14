---
created: 2026-04-13
modified: 2026-04-13
status: active
source: Shopify Admin API (theme assets)
theme:
  name: "Maerz 2026"
  id: 196991385938
  role: main
---

# DIY Template Snapshot (Metaobject)

## Template

- `templates/metaobject/diy_experience.json`

## Current section order (as of 2026-04-13)

The template currently renders three sections in this order:

1. `section_Hca4zN` (`type: section`)
2. `section_PQQgbR` (`type: section`)
3. `section_Hi3V48` (`type: section`)
4. `main` (`type: master-diy-anleitung`)

## High-signal notes

- `type: section` resolves to the Liquid implementation in `sections/section.liquid`.
- These builder sections use theme-editor “dynamic sources” strings such as `closest.metaobject.diy_experience.*` to bind metaobject fields into block settings.
- The baseline “full DIY metaobject render” remains `sections/master-diy-anleitung.liquid`, which also emits `HowTo` JSON-LD.
- `section_Hi3V48` is currently being used for a materials/products grid injected via a `custom-liquid` block.

## Theme update timestamp

The main theme reported:

- `updated_at`: `2026-04-13T11:40:43+02:00`
