# Retool Content Factory Contract

This document captures the current Content Factory workflow and artifact structure in the Bastelschachtel Retool app.

It is a core part of the pipeline and should be preserved as a reusable reference for future Codex integration.

## Purpose

Content Factory takes an existing research dossier and turns it into:

- a structured strategic brief
- a full article draft in HTML

## Inputs

The current Content Factory stage depends on:

- a selected research dossier from Research Lab
- a selected brief model
- a selected article model
- an output format
- a content style archetype
- mapped Bastelschachtel catalog products
- operator selection of which mapped products to include

## Current Model Setup

Known current example:

- brief model: DeepSeek
- article model: Claude 3.5 Sonnet

The use of different models for different stages is intentional and should be treated as part of the contract.

## Output Format Options

Current options:

- `deep dive guide`
- `listicle`
- `product comparison`
- `expert hacks`

Working interpretation:

- `deep dive guide`: instructional
- `listicle`: top-n list
- `product comparison`: buy-review focus
- `expert hacks`: information-gain focus

## Content Style Archetype Options

Current options:

- `listicle`
- `deep dive`
- `product comparison`
- `expert hacks`
- `advertorial`
- `gift guide`

## Research Dossier Dependency

The selected research dossier is the upstream input from Research Lab.

The Content Factory should use it to inform:

- topic framing
- competitor gaps
- angle selection
- hook selection
- SEO keywords
- FAQs
- supporting evidence

## Product Mapping

After dossier selection, the chosen keyword is mapped to the Bastelschachtel product CSV list stored in the Retool database.

Current behavior:

- simple keyword-to-product-title matching

The system returns product candidates from the catalog. The operator then explicitly selects which products should be included in the brief and final article.

## Brief Contract

The generated brief currently contains these sections:

- `Topic`
- `Format`
- `Working title`
- `Angle`
- `Hook options`
- `Key takeaways`
- `Outline (format-specific)`
- `Internal linking plan (locked products only)`
- `SEO block`
- `FAQ`
- `Visual Plan (Image Prompts)`

## Example Brief

```md
### Topic: peddigrohr

**Format:** listicle

### Working title
- Top 10 Peddigrohr Bastelsets: Beste Projekte fuer Anfaenger bis Profis

### Angle
- Ranked by Einfachheit, Vielseitigkeit & Brotback-Nutzen - mit Kit-Empfehlungen & Flecht-Tipps gegen Competitor-Gaps wie fehlende Varianten und Materialvergleiche

### Hook options
- Entdecke die besten Peddigrohr-Projekte: Von Mini-Koerbchen bis Brotkoerben - inklusive Flecht-Hacks, die Competitor fehlen!
- Peddigrohr vs. Holzschliff: Warum unsere Sets atmungsaktiver backen & leichter flechten - Top 10 bewertet
- Schnell flechten lernen: 10 Peddigrohr-Kits mit Schritt-fuer-Schritt-Tipps & Reinigungs-Guides

### Key takeaways
- Peddigrohr ist atmungsaktiver als Holzschliff - ideal fuer Gaerkoerbchen mit besserer Kruste
- Unsere Sets schliessen Competitor-Gaps: Vollstaendige Materialien + Korbboeden fuer sofortiges Flechten
- Top-Ranking nach Schwierigkeit: Mini-Projekte fuer Kids, grosse Koerbe fuer Brotback-Pros
- Pflege-Tipp: Trocken buersten & 120C Ofen - Sets mit passenden Boeden fuer langlebige Ergebnisse

### Outline (format-specific)
```json
{
  "criteria": [
    "Einfachheit der Flechttechnik (Anfaenger-freundlich?)",
    "Vielseitigkeit (Dekoration, Brotback, Geschenke?)",
    "Kit-Qualitaet (inkl. Korbboeden, Perlen, Anleitung?)",
    "Preis-Leistung & Groesse",
    "Competitor-Beats (z.B. mehr Varianten als VBS/MoreX)"
  ],
  "items": [
    {
      "rank": 1,
      "name": "Bastelset aus Peddigrohr - Brotkorb",
      "why_it_wins": [
        "Perfekt atmungsaktiv fuer Brotback - schlaegt Holzschliff in Krustenbildung",
        "Grosse Groesse fuer 1kg-Teig, inkl. Korbboden-kompatibel"
      ],
      "best_for": "Brotliebhaber & Gaerkorbchen-Upgrader",
      "watch_out_for": "Etwas mehr Material fuer Anfaenger",
      "internal_link_target": {
        "name": "Bastelset aus Peddigrohr - Brotkorb",
        "handle": "brotkorb-293"
      },
      "image_hint": "Fertig geflochtener Brotkorb mit Brotlaib darin, natuerliches Licht, rustikaler Tisch"
    }
  ]
}
```

### Internal linking plan (locked products only)
**Primary products:**
- Bastelset aus Peddigrohr - Brotkorb (/products/brotkorb-293)
- Bastelset aus Peddigrohr - Korb mit Deckel (/products/korb-mit-deckel-304)
- Bastelset aus Peddigrohr - Bleistifthalter (/products/bleistiftbehlter-292)

**Secondary products:**
- Korbboden rund, O 9cm fuer Peddigrohr 2mm (/products/korbboden-rund-9cm-358)
- Peddigrohr 2mm, 500g (/products/schilf-2mm-50dkg-512)
- Korbboden Set gemischt, klein fuer Peddigrohr 2mm und 3mm (/products/korbboden-set-gemischt-klein-2mm-und-3mm)

### SEO block
```json
{
  "meta_title": "Top 10 Peddigrohr Bastelsets: Anleitungen, Tipps & Gaerkorbchen-Vergleich",
  "meta_description": "Beste Peddigrohr-Projekte zum Flechten: Brotkoerbe, Halter & mehr - mit Sets, Reinigungs-Tipps vs. Holzschliff. Einfache Anleitungen fuer Anfaenger!",
  "primary_keyword": "peddigrohr",
  "secondary_keywords": [
    "peddigrohr flechten anleitung",
    "peddigrohr gaerkorbchen",
    "peddigrohr vs holzschliff",
    "peddigrohr bastelset",
    "peddigrohr korb"
  ]
}
```

### FAQ
- **Wie flechte ich Peddigrohr als Anfaenger?**: Starte mit Mini-Korb: Rohr 5-10 Min. einweichen, Dreiergeflecht um Korbboden - detaillierte Tipps in unseren Sets.
- **Peddigrohr vs. Holzschliff fuer Gaerkorbchen?**: Peddigrohr atmungsaktiver fuer bessere Kruste, leichter zu flechten - unsere Brotkorb gewinnt.
- **Wie reinige ich Peddigrohr-Koerbchen?**: Trocken buersten, Mehlschicht auftragen, 120C Ofen 20 Min. - vermeidet Feuchtigkeitsschaeden.
- **Welches Peddigrohr-Dicke fuer Anfaenger?**: 2mm flexibel & einfach - in allen unseren Sets enthalten.
- **Brauche ich extra Korbboeden?**: Viele Sets inklusive, sonst kompatibel mit unseren runden/eckigen Boeden ab 1,14 EUR.

### Visual Plan (Image Prompts)
**Hero image:** Collage von 5 fertigen Peddigrohr-Projekten auf rustikalem Holztisch, natuerliches Sonnenlicht, detaillierte Flechtmuster, Bastelschachtel-Logo dezent, warmer, einladender Ton, fotorealistisch

**In-body image #1:** Schritt-fuer-Schritt Flecht-Prozess eines Brotkorbs aus Peddigrohr: Korbboden mit Staken, Dreiergeflecht in Aktion, Werkzeuge sichtbar, helle Kueche, Makro-Details der 2mm-Rohre, instructional Stil
**In-body image #2:** Vergleich Peddigrohr vs. Holzschliff Gaerkorbchen: Zwei Koerbchen nebeneinander mit Brotteig, Peddigrohr geflochten atmungsaktiv, Holzschliff glatt, Brotkrusten-Closeup, Infografik-Overlay, neutraler Hintergrund
```

## Article Output Contract

Based on the brief, the full article is generated.

Current output format:

- HTML only

The article may include:

- `h1`, `h2`, `h3`
- paragraphs
- internal product links
- external source references
- product images
- unordered lists
- source section

## Example Article Shape

```html
<h1>Top 10 Peddigrohr Bastelsets: Beste Projekte fuer Anfaenger bis Profis</h1>

<p>Entdecke die besten Peddigrohr-Projekte: Von Mini-Koerbchen bis Brotkoerben - inklusive Flecht-Hacks, die Competitor fehlen! Wir haben alle Sets nach Einfachheit, Vielseitigkeit und praktischem Nutzen bewertet.</p>

<h2>Kurzantwort: Unser Fazit in 30 Sekunden</h2>

<p>Testsieger ist der <a href="https://www.bastelschachtel.at/products/brotkorb-293">Bastelset aus Peddigrohr - Brotkorb</a> - perfekt atmungsaktiv fuer Brotteige und ideal fuer Einsteiger ins Flechten. Fuer absolute Anfaenger empfehlen wir den <a href="https://www.bastelschachtel.at/products/bleistiftbehlter-292">Peddigrohr Bleistifthalter</a> als ersten Schritt <a href="#source-1">[1]</a>.</p>

<h2>1. Bastelset aus Peddigrohr - Brotkorb (Testsieger)</h2>

<h3><a href="https://www.bastelschachtel.at/products/brotkorb-293">Bastelset aus Peddigrohr - Brotkorb</a></h3>
<img src="https://cdn.shopify.com/s/files/1/0422/5397/5709/products/bastelset-aus-peddigrohr-brotkorb-bastelschachtel-44828.jpg?v=1767907077" alt="Brotkorb aus Peddigrohr">

<p>Warum Testsieger:</p>
<ul>
    <li>Perfekt atmungsaktiv fuer Brotteige - deutlich besser als Holzschliff <a href="#source-2">[2]</a></li>
    <li>Grosse Groesse fuer 1kg-Teig</li>
    <li>Inkl. stabilem Korbboden</li>
</ul>

<h2>Pflege-Tipps fuer Peddigrohr</h2>

<p>Fuer langlebige Ergebnisse empfehlen Experten <a href="#source-3">[3]</a>:</p>
<ul>
    <li>Trocken buersten statt waschen</li>
    <li>Bei Gaerkorbchen: Mehlschicht auftragen</li>
    <li>Gelegentlich 20 Min. bei 120C im Ofen trocknen</li>
</ul>

<section class="quellen"><h2>Quellen</h2><ul>
<li id="source-1"><a href="https://www.morex.de/blog/webenanleitungen-von-peddigrohr/" target="_blank" rel="nofollow">Webenanleitungen von Peddigrohr</a></li>
<li id="source-2"><a href="https://www.roggenwolf.de/blogs/blog/garkorbchen-reinigen" target="_blank" rel="nofollow">Gaerkorbchen reinigen - Peddigrohr, Holzschliff & Bezuege</a></li>
<li id="source-3"><a href="https://brotliebling.com/pages/gaerkoerbchen" target="_blank" rel="nofollow">Gaerkorbchen aus Holzschliff oder Peddigrohr</a></li>
</ul></section>
```

## Why This Matters for Codex Integration

Any future `blog-seo-pipeline` skill or plugin should understand that Content Factory currently produces two core artifacts:

1. a structured brief
2. an HTML article draft

Codex should be able to ingest these artifacts and then:

- validate factual support against the research dossier
- check product-link integrity
- evaluate SEO coverage
- improve structure and information gain
- prepare a more publishable final version

## Current Limitations to Remember

- product matching is currently simple keyword-to-title matching
- article generation is HTML only
- brief and article models are stage-specific and may differ
- the operator explicitly chooses product inclusion

## Status

Initial reference version created on `2026-03-27` from the current Bastelschachtel Content Factory workflow and the provided `peddigrohr` example brief and article output.
