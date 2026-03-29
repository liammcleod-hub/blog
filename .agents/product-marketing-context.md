# Product Marketing Context

*Last updated: 2026-03-29*

## Product Overview
**One-liner:** Bastelschachtel is a small, family-run Austrian specialist craft shop for Pentart, rice paper/Decoupage, basket weaving, silicone molds for gypsum and concrete casting, and selected craft materials, built around human trust, hand-packed service, and meaningful making.

**What it does:** Bastelschachtel sells about 5,000 craft SKUs through a physical shop, Shopify store, and Amazon presence. Today the business is best understood as a specialist creative-supplies shop, especially for Pentart products, rice paper and Decoupage materials, basket weaving, silicone molds for casting with gypsum and concrete, and related craft categories. The "Schachteln" bundle concept is a real merchandising opportunity tied to the brand name, but it is not yet the perfected hero offer.

**Product category:** Specialist craft supplies / creative shop, with strengths in Pentart, rice paper/Decoupage, basket weaving, silicone molds for gypsum and concrete casting, natural craft materials, and gift-making materials.

**How customers search for it:** Bastelbedarf Oesterreich, Kreativshop Oesterreich, Pentart Oesterreich, Pentart kaufen, Decoupage Reispapier kaufen, Peddigrohr kaufen, Korbflechten Material kaufen, Glasaetzpaste kaufen.

**Product type:** Hybrid retail + e-commerce business.

**Business model:** Product sales via Amazon, Shopify, and in-store retail. Current economics are still Amazon-heavy, with Shopify/email intended to become the higher-value owned channel. Bundle experiments and gift-tier mechanics exist, but the core business today is still product-led specialist retail rather than a mature bundle-led model.

## SEO & Discoverability
**Core search positioning:** Bastelschachtel should be understood by search engines and customers as an Austrian specialist creative shop, not just a generic online craft store.

**Implementation context:** The storefront is managed in the native Shopify theme editor, not a page builder. For homepage SEO work, assume the visible hero copy and the technical H1 may be controlled in different places.

**Verified homepage state (2026-03-27):**
- Technical homepage H1 is set in `sections/header.liquid` as a visually hidden heading, not as the visible hero headline.
- Current hidden homepage H1: `Bastelbedarf kaufen - Österreichs Kreativshop für Pentart, Reispapier & Korbflechten`
- Current visible hero headline: `Dein Kreativshop aus Österreich für Reispapier, Pentart, Korbflechten und mehr.`
- Current visible hero subheading: `Kleine Bastelwelt, großes Spezialsortiment: ausgewählte Materialien, persönliche Hilfe und besondere Produkte für Projekte, die Freude machen und gelingen sollen.`
- Current hero CTA: `Jetzt entdecken`
- Screenshot reference: `output/playwright/homepage-2026-03-27.png`

**Homepage updates completed on 2026-03-27:**
- Homepage SEO title updated to `Bastelbedarf kaufen | Bastelschachtel - Kreativshop Österreich`
- Homepage hidden H1 updated in `sections/header.liquid`
- Visible homepage hero copy updated to specialist Austrian positioning
- Intro section added below the hero:
  - `Kein anonymer Großshop. Eine echte Bastelwelt aus Österreich.`
  - supporting body copy about Reispapier, Pentart, Korbflechten, Silikonformen fuer Gips und Beton, and Tirol small-shop positioning
- Footer claim changed from `Mit Liebe in Österreich hergestellt` to `Mit Liebe in Österreich ausgewählt`
- Homepage now includes a blog section below `Alles für das Bastelherz`
- Current issue on homepage blog section: it shows too many posts and should be reduced to a 3-post teaser with a single `Zum Blog` button

**Blog work completed on 2026-03-27:**
- New post published: `Korbflechten mit Peddigrohr für Anfänger: Material, Stärke und erste Schritte`
- Live URL: `/blogs/uebersicht/uebersicht-korbflechten-mit-peddigrohr-fuer-anfaenger`
- The post is the recommended next SEO-support article for the Korbflechten / Peddigrohr cluster
- Required cleanup identified after live review:
  - fix malformed internal-link HTML
  - prefer inline internal links in the body over a link dump at the end
  - keep the FAQ block

**Primary search themes:**
- Bastelbedarf Oesterreich
- Kreativshop Oesterreich
- Pentart kaufen / Pentart Oesterreich
- Decoupage Reispapier kaufen
- Peddigrohr kaufen
- Korbflechten Material kaufen
- Glaetzpaste / Glasaetzpaste kaufen
- Bastelsets Oesterreich
- Silikonformen fuer Gips und Beton

**Current search strengths:**
- Strong Austria-specific niche and specialist authority
- Live trust signals on the storefront
- Active blog with tutorial and seasonal DIY content
- One strong long-form landing-page model at `/pages/bastelbedarf`
- Existing schema usage on some pages, including FAQ/HowTo on the strongest landing page

**Current search weaknesses:**
- Homepage title and H1 underuse the highest-value commercial search terms
- Some collection and blog templates appear to miss visible H1s
- Collection metadata quality is inconsistent
- At least one important basket-weaving / Peddigrohr route is broken or unresolved
- Search-facing positioning is stronger on individual pages than on the homepage

**Strategic implication:** Other marketing and SEO work should treat specialist search authority as a core growth lever. When writing landing pages, blog posts, metadata, category intros, or internal links, prioritize Bastelschachtel's role as a trusted Austrian specialist in Pentart, Decoupage rice paper, Korbflechten, and related craft categories.

**Category priority map updated on 2026-03-29:**
- Use the real shop/category structure as the backbone, not just the review set.
- Priority commercial categories are:
  - Pentart
  - Reispapier / Decoupage
  - Glasätzung
  - Silikonformen für Gips & Beton
  - Korbflechten / Peddigrohr
  - Bastelsets
- `Korbflechten / Peddigrohr` and `Bastelsets` remain strategic priorities even though the review-derived VOC is thinner there.
- `Metallic & Patina / finishing` should likely be treated first as a Pentart-led sub-family rather than a standalone top-priority page.

**Master-article strategy updated on 2026-03-29:**
- The next SEO layer after category intros is hub-style master articles that support the commercial pages.
- Recommended master-article sequence:
  1. Glasätzung
  2. Korbflechten / Peddigrohr
  3. Reispapier / Decoupage
  4. Gießen mit Gips & Beton / Silikonformen
  5. Pentart
- These articles should function as informational hubs that link into the matching category pages, products, and supporting tutorials.

## Target Audience
**Target customers:** Primarily women aged 30-60 in Austria, Germany, and Switzerland who already want to make something meaningful, but need an easier path to start or finish.

**Decision-makers:** The buyer is usually the user. Core buyers include self-directed hobby crafters, women making for family and friends, and gift-givers who want a more meaningful alternative to generic store-bought gifts.

**Primary use case:** Helping customers create thoughtful gifts or personal creative projects without the overwhelm of sourcing, deciding, and assembling everything alone.

**Jobs to be done:**
- Help me make a meaningful gift that feels personal, not generic.
- Help me start a creative project without having to figure out every material myself.
- Help me reclaim creative time for myself without guilt or friction.

**Use cases:**
- Seasonal handmade gifts, especially for Christmas.
- DIY gifts for birthdays, family occasions, and personal milestones.
- Home decoration and beautification projects.
- Basket weaving, glass etching, finishing, and decorative craft projects.
- Decoupage and rice-paper based decorative projects.
- Gypsum and concrete casting projects using silicone molds.
- Family crafting and kid-friendly creative time.
- "Something for me" projects where the buyer is making for herself, not only others.

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| The woman who used to make things | Reclaiming creativity, rest, self-expression | Adult life crowded out creative time; guilt about doing something for herself | Permission plus an easy starting point |
| The one who makes for others | Giving meaning, care, and effort through gifts | Always making for others, rarely for herself; overwhelmed by planning | A simple system for thoughtful handmade gifting |
| The gift-giver tired of Amazon | Authenticity, originality, human feeling | Generic gifts feel empty and transactional | A more personal, flexible, handmade alternative |

## Problems & Pain Points
**Core problem:** Customers already want to make or give something meaningful, but they feel blocked by complexity, time pressure, too many options, or the sense that handmade projects are harder than they should be.

**Why alternatives fall short:**
- Amazon is fast, but it is impersonal and relationship-free.
- Generic craft retailers sell products, not a clear path to the finished outcome.
- Fixed kits can feel restrictive or generic.
- Pinterest and inspiration content create desire, but not execution.
- Mass-produced gifts solve convenience, but not meaning.

**What it costs them:** Wasted time, abandoned project ideas, generic gifting, lower confidence, higher decision fatigue, and missed chances to make something more memorable.

**Emotional tension:** Guilt about taking time for themselves, sadness about not making things anymore, frustration with impersonal gifting, intimidation about starting, and fear of getting it wrong.

## Competitive Landscape
**Direct:** Amazon, generic craft supply retailers, large European craft chains like Boesner, VBS Hobby, BABSI, and broad online Bastelshops. They win on scale, price perception, and convenience, but they often lose on warmth, specialist depth, flexibility, and direct human connection.

**Secondary:** Etsy sellers, fixed DIY kits, Pinterest-driven inspiration journeys, and general gift shops. They solve parts of the problem, but usually not the whole path from idea to execution.

**Indirect:** Buying a generic gift, doing nothing, or postponing the project again. The real competitor is often inertia plus convenience, not just another store.

**Category-level competitive read:**
- **Pentart:** Customers are not just looking for "craft paint." They are looking for a specialist source that helps them find the right Pentart effect, medium, or finish for a specific project. Generic shops lose here when their assortment is broad but not legible.
- **Reispapier / Decoupage:** Customers want motif quality, decorative inspiration, and a sense of discovery. Generic paper listings and broad marketplaces lose when the assortment feels random or aesthetically weak.
- **Glasätzung:** The real competitor is often uncertainty. Customers want to know the product will work, especially on the first try. A specialist shop can win by reducing beginner anxiety better than a commodity seller.
- **Korbflechten / Peddigrohr:** Search intent is highly specific and strongly commercial. The main competitive weakness to exploit is confusion: many alternatives do not provide a clear, trustworthy path from "I want to try this" to "these are the right materials."
- **Silikonformen für Gips & Beton:** Buyers care about detail fidelity and usable project outcomes, not just "a mold." Broad marketplaces tend to underserve the project system around the form, material, and finishing steps.

## Differentiation
**Key differentiators:**
- Bastelschachtel is a real small business and family-run operation in Wattens, Tirol.
- Every order is hand-packed by a real 4-person team in Wattens, Tirol.
- Customers can contact the team directly when something goes wrong.
- The brand voice is warm, personal, and permission-based instead of pushy.
- The bundle philosophy gives structure without removing customer choice.
- The assortment is broad enough to support real creative variety, not just a narrow kit catalog.
- The business has a defendable Austria-specific niche as one of the last true specialists in this category space, especially for Pentart, Decoupage rice paper, and Peddigrohr basket-weaving kits.
- Bastelschachtel competes on meaning, authenticity, and ease, not on "cheapest" positioning.

**How we do it differently:** Bastelschachtel does not try to convince people to become creative. It assumes they already want to create and removes the barriers that stop them. The business sells a system and a feeling of support, not just materials.

**Why that's better:** Customers get the emotional value of handmade gifting or making, without as much friction, confusion, or impersonality. They keep control over what they buy while still getting guidance and curation.

**Why customers choose us:** Because they want the gift or project to feel like them, not like Amazon. They want warmth, flexibility, specialist depth, and a human brand they can trust.

## Objections
| Objection | Response |
|-----------|----------|
| "I am not creative enough for this." | You already know what a meaningful gift looks like. Bastelschachtel makes it easier to start with the right materials and categories. |
| "This looks complicated." | The role of the bundle system is to remove sourcing friction and make the path clearer, not to add more decisions. |
| "I do not have time." | The promise is not elaborate artistry. It is a more meaningful result with a simpler path than doing everything from scratch. |
| "Amazon is easier/faster." | Amazon is easier for transactions. Bastelschachtel is better when the outcome needs to feel personal, handmade, and cared for. |
| "Shipping is expensive for small orders." | This is a real friction point and should be handled honestly with better bundling, thresholds, and value framing rather than hype. |

**Anti-persona:** Someone optimizing only for lowest price, instant commodity delivery, or fully done-for-you gifting. Also not ideal for people who want zero involvement in the making process.

## Switching Dynamics
**Push:** Generic gifts feel empty. Amazon is convenient but impersonal. Sourcing craft materials across many products or stores feels tiring. Many customers miss a more meaningful, creative way of giving.

**Pull:** Bastelschachtel offers a simpler way to make something personal, with hand-packed care, direct support, flexible bundles, and a brand that feels human.

**Habit:** Defaulting to Amazon, buying something pre-made, postponing the project, or assuming creative work is "for later."

**Anxiety:** "What if I buy the wrong things?" "What if I do not finish?" "What if it is harder than it looks?" "What if shipping or timing makes this not worth it?"

## Customer Language
**How they describe the problem:**
- "I want to make something meaningful, but I do not know where to start."
- "I have been thinking about this gift for a while and still have not begun."
- "I want it to feel personal, not like something I grabbed at the last minute."
- "I used to make things more often."
- Review-derived friction themes:
  - "Trotz Reklamation keine Antwort oder Reaktion erhalten"
  - "4 Farben Pink bestellt und nur 1 Produkt erhalten"
  - "Von dem unterirdischen Versand mit GLS will ich garnicht erst anfangen!"
  - "Leider wird das A3-Format geknickt und nicht gerollt verschickt"

**How they describe us:**
- "Everything I need to make the gift I have been thinking about."
- "Not complicated. Not generic. Not from a big store."
- "A real Austrian specialist shop, not a faceless marketplace."
- "A place where I can actually find the specialist materials, not just generic craft products."
- Review-derived direct VOC:
  - "Glasätzpaste funktioniert wunderbar"
  - "Riesige Auswahl"
  - "Schneller Versand und tolle Verpackung"
  - "Das Reispapier kam sicher verpackt und schnell bei mir an"
  - "Ich benutze nur noch Produkte von Pentart"
  - "sehr detailreiche Siliconform"
  - "unkomplizierte sehr kundennahe Lösung"

**Words to use:** hand-packed, meaningful, personal, inspiration, for you, for your projects, make it yourself, warm, easy to start, thoughtful, handmade, permission, creativity, support, specialist, family-run, leicht zu verarbeiten, gute Deckkraft, toller Effekt, detailreich, funktioniert wunderbar, große Auswahl.

**Words to avoid:** Q4, sales push, VIP-only language, fake exclusivity, "last chance" language, aggressive CTA language, corporate phrasing, over-optimized marketing jargon, generic "premium quality" filler without project-specific proof.

**Glossary:**
| Term | Meaning |
|------|---------|
| Schachteln | Bastelschachtel's bundle concept and naming opportunity, not yet the fully developed hero offer |
| For Christmas | Holiday and gift-making category |
| For Yourself | Self-directed projects with a permission angle |
| For Gifting | Gift-making category for meaningful presents |
| For the Home | Home decoration and beautification projects |
| With Children | Family-friendly and child-inclusive crafting |

## Brand Voice
**Tone:** Warm, personal, supportive, honest, and quietly invitational.

**Style:** Customer-facing copy is written in German using informal "du" language and a collective team voice ("wir"). The tone should feel personal and literary in email, customer-centered in framing, and implicit rather than overtly sales-driven.

**Personality:** Warm, authentic, unhurried, supportive, creative, grounded.

## Proof Points
**Metrics:**
- About 5,000 SKUs across the assortment
- 300+ orders/day fulfillment capacity without quality degradation
- Q4 2024 revenue: EUR106k
- Current channel mix: roughly 90% Amazon / 10% owned channels
- 8,000 total Klaviyo subscribers, around 3,200 active online-shop subscribers
- Baseline email open rate around 30%
- Top product line: glass etching paste at EUR11,737.01 YTD 2025
- 4.88-star average across 764 reviews, according to the March 26, 2026 SEO audit
- Homepage trust claim: more than 60,000 happy customers
- Homepage brand claim: more than 250,000 ideas realized
- Free shipping over EUR70 in Austria and Germany
- 14-day money-back guarantee
- Live homepage title at audit time: `Bastelschachtel - der Online Kreativshop`
- Live homepage H1 at audit time: `Bastelschachtel`

**Customers:** Primary customer base is women 30-60 across the DACH region. No named customer logos or marquee partner proof points are documented in this workspace.

**Testimonials:**
> "Glasätzpaste funktioniert wunderbar" — owned-channel review

> "Das Reispapier kam sicher verpackt und schnell bei mir an." — Amazon review

> "Ich benutze nur noch Produkte von Pentart." — owned-channel review

> "sehr detailreiche Siliconform" — owned-channel review

> "unkomplizierte sehr kundennahe Lösung" — Amazon review

> "Schneller Versand. Ware wie beschrieben. Gerne wieder." — Amazon review

**Value themes:**
| Theme | Proof |
|-------|-------|
| Human care | Orders are hand-packed daily by a 4-person team in Wattens |
| Better than generic gifting | Core positioning centers on handmade meaning vs impersonal convenience |
| Easier path to making | Bundle model and curated categories reduce sourcing friction |
| Authentic small-business trust | Direct contact, honest imperfection, and warm communication are recurring brand assets |
| Austrian specialist authority | SEO audit positions Bastelschachtel as the only/last Austrian specialist in key categories such as Pentart, Decoupage rice paper, and basket-weaving kits |
| Live-store trust signals | Homepage shows 4.88 stars from 764 reviews, 60,000+ happy customers, 250,000+ ideas realized, free shipping over EUR70, and direct phone/WhatsApp support |
| Search upside from better positioning | The live audit found that the site's category authority is stronger than its current homepage/title/H1 execution, creating a clear SEO growth opportunity |
| Product performance trust | Reviews repeatedly use language like `funktioniert wunderbar`, `leicht zu verarbeiten`, `gute Deckkraft`, and `toller Effekt` |
| Specialist assortment depth | Reviews mention `Riesige Auswahl` and category-specific discovery value, especially in Reispapier and Pentart |
| Shipping as a trust amplifier or destroyer | Reviews split strongly between `Schneller Versand und tolle Verpackung` and harsh delivery / GLS complaints, showing operations shape brand perception directly |

## Goals
**Business goal:** Reduce dependency on Amazon and grow owned channels, especially Shopify + email, toward 30-40% of total revenue while preserving small-team authenticity.

**Conversion action:** Get customers into the owned ecosystem, primarily through email sign-up, Shopify browsing/building, and direct-store purchases rather than Amazon-only behavior.

**Current metrics:** Owned channels are still underweight versus Amazon. Email engagement is healthy relative to list quality, but attribution, repeat purchase behavior, and owned-channel conversion need stronger measurement and systemization.
