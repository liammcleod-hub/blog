# Shopify Theme Operations — Bastelschachtel

_Last updated: April 16, 2026_

---

## Store Details
- **Store**: bastelschachtel.myshopify.com
- **Live Theme**: #196991385938 "Maerz 2026"
- **Backup Theme**: #199264305490 "Kopie von Maerz 2026"
- **API Version**: 2026-01
- **Access Token**: In `shopify_api_work/.env`
- **CSS served from**: `/cdn/shop/t/27/assets/` (increments to t/28 etc. after changes)

---

## Theme Architecture

### File Structure (Critical Paths)
```
sections/header.liquid              → Main header section (loads header-group.json)
sections/header-group.json          → Configures header blocks
blocks/_header-menu.liquid          → Menu block config
snippets/header-drawer.liquid       → Mobile hamburger menu (HTML + {% stylesheet %} + script reference)
assets/base.aio.min.css            → **THE COMPILED CSS ACTUALLY SERVED** (not base.css!)
assets/base.css                    → Source CSS — Shopify compiles this into base.aio.min.css
assets/header-drawer.aio.min.js    → **THE COMPILED JS ACTUALLY SERVED** (not header-drawer.js!)
assets/header-drawer.js            → Source JS — NOT loaded, compiled into .aio.min.js
```

### Mobile Menu HTML Structure
```html
<header-drawer class="header-drawer ...">
  <details id="Details-menu-drawer-container" class="menu-drawer-container" ref="details">
    <summary aria-label="Menü">...</summary>
    <div class="menu-drawer motion-reduce color-scheme-1">
      <nav class="menu-drawer__navigation">
        <ul class="menu-drawer__menu">
          <li>...~50+ items with nested accordions...</li>
        </ul>
      </nav>
    </div>
  </details>
</header-drawer>
```

### Key CSS Classes and Rules
```css
.menu-drawer {
  position: fixed;
  height: var(--drawer-height);    /* --drawer-height: 100dvh = full viewport */
  overflow: auto;                   /* Intended scroll, but... */
}
.menu-drawer:has(details[open]) {
  overflow: initial;               /* OVERRIDES scroll when accordion open! */
}
.header__drawer--desktop .menu-drawer {
  height: 100vh;                   /* Desktop override */
}
```
- `menu-open` class is on `<details#Details-menu-drawer-container>`, NOT on `.menu-drawer` div
- `color-scheme-1` class on `.menu-drawer` provides the background gradient/color

### JS Architecture
- `header-drawer.aio.min.js` defines `<header-drawer>` as a Custom Element (Web Component)
- Uses `import { Component } from "@theme/component"`
- Handles open/close with `menu-open` class toggle, focus trapping, accordion animations
- Loaded as `<script type="module">` with `fetchpriority="low"`

---

## CRITICAL: Shopify Compiled Assets

### The #1 Lesson
**Shopify serves `.aio.min.css` and `.aio.min.js`, NOT the source `.css`/`.js` files.**

| Source File (you edit) | Compiled File (Shopify serves) |
|------------------------|-------------------------------|
| `base.css`             | `base.aio.min.css`            |
| `header-drawer.js`     | `header-drawer.aio.min.js`    |

- Edits to `base.css` do NOT appear on live site unless Shopify recompiles
- **Always edit `base.aio.min.css` directly** for immediate effect
- Same for JS — edit `header-drawer.aio.min.js` directly
- Shopify may recompile on theme push, but the `.aio.min.` version takes precedence

### The Unclosed Rule Bug
The original `base.aio.min.css` ends with:
```css
.section-content-wrapper .blog-post-content.rte {
  max-width: none !important;
  padding-inline: 0 !important;
/* } */
```
The closing brace `}` is **commented out** (`/* } */`). This means:
- Any CSS appended gets NESTED inside `.section-content-wrapper .blog-post-content.rte`
- Must replace `/* } */` with `}` before appending new rules
- **Always check the last rule is properly closed before appending**

### {% stylesheet %} Blocks
- `{% stylesheet %}...{% endstylesheet %}` in Liquid snippets does NOT compile into served CSS
- These blocks are ignored by Shopify's build system
- Do NOT put fixes here — they won't appear on the live site

---

## Mobile Menu Scroll Fix (April 2026)

### Problem
Menu cut off at "Saisonale Deko" — items below (Blog, Katalog) inaccessible. No scrollbar on mobile.

### Root Cause
- `--drawer-height: 100dvh` = drawer fills entire viewport (812px on iPhone)
- Content is 997px tall — overflows but no scroll because height = viewport exactly
- `.menu-drawer:has(details[open])` sets `overflow: initial`, killing scroll when accordions open

### Fix Applied
Appended to `base.aio.min.css` (after fixing the unclosed `/* } */`):
```css
/* MOBILE MENU SCROLL FIX */
@media screen and (max-width: 749px) {
  .menu-drawer {
    overflow-y: auto !important;
  }
}
```

### Why This Works
- `overflow-y: auto !important` overrides both `overflow: auto` (redundant) and `overflow: initial` from `:has()` rule
- Height stays at `100dvh` = full screen (no gap at bottom)
- `scrollHeight (997) > clientHeight (812)` = scrollbar appears when needed
- Color preserved: `color-scheme-1` background intact, no inline style overrides

### Verified Results (Browser Testing)
```json
{
  "height": "812px",
  "overflowY": "auto",
  "bg": "rgb(255, 255, 255)",
  "scrollHeight": 997,
  "clientHeight": 812
}
```

---

## Failed Approaches (Do NOT Repeat)

### Editing base.css directly
Shopify compiles to `base.aio.min.css`. Source file changes don't appear on live.

### Editing header-drawer.js directly
Shopify compiles to `header-drawer.aio.min.js`. Source file changes don't appear on live.

### {% stylesheet %} blocks in Liquid
Ignored by Shopify's build system. CSS never makes it to the compiled output.

### Adding <style> tags in Liquid snippets
Can break rendering or get stripped. Caused color loss (transparent background).

### Inline style="height: 85dvh;" on .menu-drawer div
Shopify may strip inline styles or the component JS overrides them. Also broke color-scheme-1.

### MutationObserver on .menu-drawer for menu-open class
`menu-open` class is on PARENT `<details>`, not on `.menu-drawer` div. Observer never fires.

### height: 85dvh !important on .menu-drawer
Reduces height (812 to 690px) which enables scroll BUT leaves gap at bottom + breaks color.

### Overwriting files instead of appending
Previous model destroyed `base.css` (99KB to 221 bytes) and `header-drawer.js` (5KB to 530 bytes). **ALWAYS APPEND.**

### Appending CSS without closing the last rule
The unclosed `/* } */` causes appended rules to nest inside `.blog-post-content.rte`.

---

## Working Procedures

### Deploying CSS Changes
1. Pull live theme: `shopify theme pull --store bastelschachtel.myshopify.com --theme 196991385938 --path work_theme`
2. Download current CDN CSS: `curl -s "https://www.bastelschachtel.at/cdn/shop/t/27/assets/base.aio.min.css" -o base_original.css`
3. Fix unclosed rule: replace trailing `/* } */` with `}`
4. Append new CSS rules
5. Replace both `base.aio.min.css` AND `base.css` in work_theme with the fixed version
6. Push: `shopify theme push --store bastelschachtel.myshopify.com --theme 196991385938 --path work_theme --allow-live --ignore "config/settings_data.json"`
7. Wait 10-15s for CDN cache update
8. Verify with browser tools

### Rollback Procedure
```bash
# Interactive terminal required! (shopify theme publish needs confirmation)
shopify theme publish --store bastelschachtel.myshopify.com --theme 199264305490
# Press Y when prompted
```
**Cannot be run non-interactively** — must use a real terminal.

### Browser Testing
```bash
# Using gstack browse
B=~/.claude/skills/gstack/browse/dist/browse.exe
$B goto https://www.bastelschachtel.at/
$B wait --load
$B click "[aria-label='Menü']"
$B js '(function(){var d=document.querySelector(".menu-drawer");var s=getComputedStyle(d);return JSON.stringify({height:s.height,overflowY:s.overflowY,bg:s.backgroundColor})})()'
$B screenshot /tmp/result.png
```

### Verifying Served CSS
```bash
# Check which CSS version is being served
curl -s "https://www.bastelschachtel.at/cdn/shop/t/28/assets/base.aio.min.css" | grep "YOUR_FIX_STRING"
```

---

## AEO/GEO in CSS?
**No.** CSS is for visual styling only. AEO/GEO optimization belongs in:
- HTML/Liquid templates (schema markup, JSON-LD, meta tags)
- Section/block files (structured data, FAQ content)
- `<head>` in `theme.liquid` (meta tags, link tags)

If AEO/GEO stuff ends up in a CSS file, something went wrong.

---

## Other Theme IDs (for reference)
| ID | Name | Notes |
|----|------|-------|
| #196991385938 | Maerz 2026 | **LIVE** |
| #199264305490 | Kopie von Maerz 2026 | Backup/rollback |
| #152202281298 | AVADA Assets - DO NOT REMOVE | Asset management |
| #184450842962 | Horizon | Previous theme |
| #188668477778 | Horizon before Shopify Support Bug Cleanup (V1) | Pre-cleanup |
| #188997534034 | Horizon Post Cleanup (V2) | Post-cleanup |

---

## Local Working Directories
| Path | Purpose |
|------|---------|
| `temp_theme/` | Original pull (WARNING: files were corrupted by previous models) |
| `/c/Users/Hp/shopify_fix/work_theme/` | Clean working copy (last used for successful push) |
| `/c/Users/Hp/shopify_fix/backup_theme/` | Backup theme pull (contaminated with test fix) |
| `/c/Users/Hp/shopify_fix/original_base_aio.css` | Clean CDN-served CSS (t/27) |
| `/c/Users/Hp/shopify_fix/fix_base_aio_v2.css` | CSS with scroll fix applied |
| `shopify_api_work/` | API integration scripts and docs |
