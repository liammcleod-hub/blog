# Retool Research Lab JSON Contract
#retool #content-pipeline

This document defines the Research Lab output from the Bastelschachtel Retool content pipeline.

It exists as a stable reference because this JSON payload is an integral upstream input for the broader blog and SEO workflow. Future docs, skills, scripts, and QA checks should treat this as a source-of-truth contract unless explicitly superseded.

## Purpose

The Research Lab is the first structured research stage in the pipeline.

It allows a user to:

- enter a keyword or topic
- choose a research mode
- choose an OpenRouter model
- choose how many sources to reference
- receive structured JSON that can be reused downstream

This output is intended to inform:

- keyword selection refinement
- competitor landscape analysis
- article angle selection
- strategic brief creation
- full article generation
- SEO and logic QA

## Current Workflow Position

Current manual flow:

1. Run the Retool Research Lab for a keyword.
2. Choose research type, model, and source count.
3. Receive structured JSON.
4. Feed that JSON into later pipeline stages and into Codex-driven blog/SEO workflows.

For now, the user presses the buttons in Retool manually. Codex should be able to consume the exported JSON as a reusable artifact.

## Research Lab Inputs

The Research Lab currently operates with these user-controlled inputs:

- `topic`
- `locale`
- `research_type`
- `competitor_url` (optional)
- `max_sources`
- selected OpenRouter model in Retool

## Research Types

Known Research Lab modes include:

- `general research dossier`
- `serp landscape`
- `competitor overview`
- `product research`

These labels may be represented internally in normalized form such as `product_research`.

## Output Contract

The JSON payload currently includes the following top-level fields:

- `locale`
- `topic`
- `research_type`
- `competitor_url`
- `max_sources`
- `summary`
- `citations`
- `competitor_blueprints`
- `competitor_findings`
- `search_intents`

## Field Semantics

### `locale`

Target market or language/region context for the research.

Example:

- `de-AT`

### `topic`

The keyword, product term, or topic submitted to the Research Lab.

Example:

- `peddigrohr`

### `research_type`

The chosen research mode. This determines the expected emphasis of the returned research.

Example:

- `product_research`

### `competitor_url`

Optional URL used when the research run targets a specific competitor. May be `null`.

### `max_sources`

The requested cap on referenced sources.

### `summary`

A short synthesized overview of the topic and the competitive/search landscape discovered by the model.

### `citations`

A list of source objects used as evidence in the research output.

Each citation object may include:

- `url`
- `title`
- `publisher`
- `published_date`
- `quote`

### `competitor_blueprints`

A list of abstractions of competitor pages or source pages, capturing how they are framed and where they are weak.

Each blueprint object may include:

- `url`
- `title`
- `framework`
- `hook`
- `gap`
- `evidence`

The nested `evidence` object may include:

- `quote`
- `source_url`

### `competitor_findings`

Lightweight structured notes about notable pages found in the landscape.

Each finding object may include:

- `url`
- `notes`
- `structure`
- `word_count_estimate`
- `target_keyword_guess`

The nested `structure` object may include:

- `has_faq`
- `has_tables`
- `has_video`

### `search_intents`

Observed or inferred keyword-intent mappings based on the returned sources.

Each intent object may include:

- `intent`
- `type`
- `why`
- `evidence_url`

## Example Payload

```json
{
  "locale": "de-AT",
  "topic": "peddigrohr",
  "research_type": "product_research",
  "competitor_url": null,
  "max_sources": 10,
  "summary": "Peddigrohr ist ein flechtbares Rattan-Material fuer Bastelarbeiten, Gaerkoerbchen und Sitzflaechen. Competitor-Artikel fokussieren auf Anleitungen zum Flechten, Reinigen und Vergleichen mit Alternativen wie Holzschliff.",
  "citations": [
    {
      "url": "https://www.morex.de/blog/webenanleitungen-von-peddigrohr/",
      "title": "Webenanleitungen von Peddigrohr",
      "publisher": "MOREX",
      "published_date": null,
      "quote": "Anleitungen - Flechten aus Peddig · Engel aus Peddig · Weihnachtssterne aud Peddig · Glocke aus Peddig · Serviettenhalter."
    },
    {
      "url": "https://www.roggenwolf.de/blogs/blog/garkorbchen-reinigen",
      "title": "Gaerkorbchen reinigen - Peddigrohr, Holzschliff & Bezuege",
      "publisher": "roggenwolf",
      "published_date": null,
      "quote": "Bei der Reinigung von Peddirohr Gaerkorben gibt es ein paar Dinge zu beachten. Mit der richtigen Pflege, ist ein Peddigrohr Gaerkorb ein langlebiger Backbegleiter."
    },
    {
      "url": "https://brotliebling.com/pages/gaerkoerbchen",
      "title": "Gaerkorbchen aus Holzschliff oder Peddigrohr",
      "publisher": "Brotliebling Wissen",
      "published_date": null,
      "quote": "Peddigrohr ist sehr atmungsaktiv, was dazu beitraegt, dass der Teig gut 'atmen' kann."
    },
    {
      "url": "https://www.vbs-hobby.com/anleitung-peddigrohr-pflanzenkorb-t1423/",
      "title": "Anleitung: Peddigrohr-Pflanzenkorb",
      "publisher": "VBS Hobby",
      "published_date": null,
      "quote": "Nach dem Trocknen das Peddigrohr ca. 45 Minunten in Wasser einweichen, bis es ausreichend flexibel ist."
    }
  ],
  "competitor_blueprints": [
    {
      "url": "https://www.morex.de/blog/webenanleitungen-von-peddigrohr/",
      "title": "Webenanleitungen von Peddigrohr",
      "framework": "How-To",
      "hook": "Webenanleitungen von Peddigrohr",
      "gap": "Fehlende detaillierte Schritt-fuer-Schritt-Anleitungen",
      "evidence": {
        "quote": "Anleitungen - Flechten aus Peddig · Engel aus Peddig · Weihnachtssterne aud Peddig",
        "source_url": "https://www.morex.de/blog/webenanleitungen-von-peddigrohr/"
      }
    },
    {
      "url": "https://www.roggenwolf.de/blogs/blog/garkorbchen-reinigen",
      "title": "Gaerkorbchen reinigen - Peddigrohr, Holzschliff & Bezuege",
      "framework": "How-To",
      "hook": "In diesem Artikel erfaehrst du, wie du Holzschliff und Peddigrohr Gaerkorbe sowie die passenden Bezuege am besten reinigst",
      "gap": "Wenig Infos zu spezifischen Pflegeprodukten",
      "evidence": {
        "quote": "Anschliessend bei ca. 120° C fuer 20 Minuten im Ofen trocknen lassen",
        "source_url": "https://www.roggenwolf.de/blogs/blog/garkorbchen-reinigen"
      }
    },
    {
      "url": "https://brotliebling.com/pages/gaerkoerbchen",
      "title": "Gaerkorbchen aus Holzschliff oder Peddigrohr",
      "framework": "Comparison",
      "hook": "Peddigrohr, auch als Rattan bekannt, ist ein natuerliches Material",
      "gap": "Keine Kaufempfehlungen oder Preise",
      "evidence": {
        "quote": "Unterschied zwischen Peddigrohr und Holzschliff: Peddigrohr hat eine geflochtene Struktur, die es sehr atmungsaktiv macht",
        "source_url": "https://brotliebling.com/pages/gaerkoerbchen"
      }
    },
    {
      "url": "https://www.vbs-hobby.com/anleitung-peddigrohr-pflanzenkorb-t1423/",
      "title": "Anleitung: Peddigrohr-Pflanzenkorb",
      "framework": "How-To",
      "hook": "Anleitung Nr. 1326",
      "gap": "Begrenzte Varianten jenseits von Pflanzenkorb",
      "evidence": {
        "quote": "Nun die 3 mm-Staken mit einem Seitenschneider auf die gewuenschte Laenge zuschneiden",
        "source_url": "https://www.vbs-hobby.com/anleitung-peddigrohr-pflanzenkorb-t1423/"
      }
    }
  ],
  "competitor_findings": [
    {
      "url": "https://www.morex.de/blog/webenanleitungen-von-peddigrohr/",
      "notes": "Uebersicht ueber Flechtanleitungen mit Peddigrohr",
      "structure": {
        "has_faq": false,
        "has_tables": false,
        "has_video": false
      },
      "word_count_estimate": 150,
      "target_keyword_guess": "peddigrohr anleitungen"
    },
    {
      "url": "https://www.roggenwolf.de/blogs/blog/garkorbchen-reinigen",
      "notes": "Pflegetipps fuer Peddigrohr-Gaerkorbchen",
      "structure": {
        "has_faq": false,
        "has_tables": false,
        "has_video": false
      },
      "word_count_estimate": 400,
      "target_keyword_guess": "peddigrohr reinigen"
    },
    {
      "url": "https://brotliebling.com/pages/gaerkoerbchen",
      "notes": "Vergleich Peddigrohr vs. Holzschliff fuer Gaerkorbchen",
      "structure": {
        "has_faq": false,
        "has_tables": false,
        "has_video": false
      },
      "word_count_estimate": 500,
      "target_keyword_guess": "peddigrohr gaerkorbchen"
    },
    {
      "url": "https://www.vbs-hobby.com/anleitung-peddigrohr-pflanzenkorb-t1423/",
      "notes": "Schritt-fuer-Schritt-Anleitung fuer Pflanzenkorb",
      "structure": {
        "has_faq": false,
        "has_tables": false,
        "has_video": false
      },
      "word_count_estimate": 300,
      "target_keyword_guess": "peddigrohr flechten anleitung"
    }
  ],
  "search_intents": [
    {
      "intent": "peddigrohr flechten anleitung",
      "type": "informational",
      "why": "Mehrere How-To-Guides zu Flechttechniken",
      "evidence_url": "https://www.morex.de/blog/webenanleitungen-von-peddigrohr/"
    },
    {
      "intent": "peddigrohr gaerkorbchen reinigen",
      "type": "informational",
      "why": "Detaillierte Reinigungsanleitung fuer Gaerkorbchen",
      "evidence_url": "https://www.roggenwolf.de/blogs/blog/garkorbchen-reinigen"
    },
    {
      "intent": "peddigrohr vs holzschliff",
      "type": "commercial",
      "why": "Vergleich der Materialien fuer Backzubehoer",
      "evidence_url": "https://brotliebling.com/pages/gaerkoerbchen"
    }
  ]
}
```

## Downstream Use in the Blog SEO Pipeline

This JSON should be considered valid upstream context for:

- choosing whether a topic is worth pursuing
- deciding the best article angle
- identifying likely competing pages
- identifying missing content structures in the SERP
- extracting likely subtopics and intent patterns
- informing strategic brief generation
- grounding article generation in cited evidence

## Current Practical Rule

When a Retool Research Lab run exists for a topic, later pipeline stages should prefer using that JSON instead of reconstructing the research from scratch.

## Notes for Future Expansion

Likely future additions to this contract or its surrounding workflow:

- model metadata used for the run
- timestamp of execution
- normalized keyword cluster data
- content opportunity score
- recommendation on whether to proceed or skip
- suggested article type and title candidates
- schema recommendations
- internal linking recommendations
- QA flags for weak evidence or thin competitor coverage

## Status

This is the initial reference version created on `2026-03-27` based on the current Bastelschachtel Retool pipeline behavior and an example `peddigrohr` research payload.
