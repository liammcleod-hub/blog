# Craft Language Rules

This reference helps `blog-seo-pipeline` use more natural arts-and-crafts language for Korbflechten and Peddigrohr content.

## Core Rule

For beginner-facing craft content, use domain-correct words, but explain them at first mention.

Do not overload the reader with niche terminology too early.

## German Orthography Rule

For German content, always use real umlauts and ß where appropriate.

Do not normalize:

- `ae` instead of `ä`
- `oe` statt `ö`
- `ue` statt `ü`

unless the string is a fixed technical limitation such as a URL, handle, slug, file name, or source text that must stay unchanged.

Mojibake is a hard failure, not a style issue. Reject output containing strings like:

- `fÃ¼r`
- `StÃ¤rke`
- `groÃŸ`
- `AnfÃ¤nger`

## For Peddigrohr / Korbflechten

Prefer a progression like:

1. simple plain-language term
2. niche term in context
3. later reuse of the niche term once established

Example:

- `die senkrechten Stäbe`
- `oft auch Staken genannt`
- later: `die Staken`

## Terms Worth Introducing Carefully

- `Staken`
- `Flechtrohr`
- `Randabschluss`
- `Zuschlag`
- `Boden`
- `Spannung`

## Material-Range Rule

If a guide recommends one material size or strength as the default, it should usually mention the next relevant alternative as well.

For example:

- if `2mm` is the beginner default, briefly explain where `3mm` becomes useful
- if one material is recommended for small projects, state when a sturdier option makes more sense
- if a concrete `2mm` or `3mm` product or set is linked, make sure the wording matches what the destination actually is

The reader should leave with:

- a default recommendation
- one nearby alternative
- a simple explanation of when to choose which

## Good Beginner Pattern

Use:

- what the part is
- what it does
- what beginners usually get wrong

Example:

- `Die senkrechten Stäbe bilden das Gerüst des Korbs. Im Korbflechten nennt man sie oft Staken. Wenn sie am Anfang ungleich sitzen, wird später auch die Form unruhig.`

## Avoid

- unexplained niche jargon in the first paragraph
- vague phrases that sound generic rather than crafty
- overly abstract descriptions when a hand movement can be named clearly

## For Tutorial-Intent Pages

Prefer concrete verbs:

- einweichen
- anschneiden
- einführen
- führen
- flechten
- nachfeuchten
- ausrichten
- abschließen

Over weak verbs like:

- bearbeiten
- anwenden
- umsetzen
- vorbereiten

Use the weak verbs only when the more concrete action is not known.

## Weave-Motion Rule

If the article teaches a first project or first technique, it should name the basic movement clearly.

Do not stop at:

- `lege die erste Runde`
- `führe das Material`
- `beginne mit dem Flechten`

Prefer one concrete sentence such as:

- `Führe das Flechtrohr abwechselnd vor und hinter den Staken entlang.`
- `Lege das Rohr in einer ruhigen Vor-und-hinter-Bewegung um die Staken.`

The reader should be able to imagine the first hand movement without needing a video immediately.

## Inline Linking Rule

When the article mentions product-relevant beginner phrases, link them naturally where they become useful.

Examples:

- `2mm Peddigrohr`
- `Korbboden`
- `Mini Korb`
- `Bleistifthalter`
- `Korb mit Deckel`

Do not rely only on a link dump at the end of the article.

## Section-Pruning Rule

If a section does not clearly help the beginner start, choose, or succeed, cut it or rewrite it.

Examples of weak sections:

- comparison blocks that feel like leftover research
- side-topic material comparisons that do not improve the first project decision

## Product Image Rule

If multiple product images appear in one article:

- normalize their presentation intentionally
- avoid cropping important product content
- avoid adding visible background framing unless explicitly wanted
- if the goal is square presentation without cropping, prefer `object-fit: contain` over `cover`
