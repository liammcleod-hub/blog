# Blog SEO Pipeline Canonical Rehaul Plan

Date: 2026-03-31
Owner: Codex + Bastelschachtel
Status: Proposed baseline

## Decision

`blog-seo-pipeline` becomes the canonical article engine for Bastelschachtel blog content.

That means:

- Retool is no longer the final logic owner for article structure or product logic.
- Retool may still provide dossier, brief seeds, article seeds, and selected products.
- The pipeline owns final coherence: article assembly, section logic, product roles, complementary product expansion, internal linking, excerpt, SEO title, meta description, handle, and publish-ready HTML.
- The pipeline may use both:
  - exact approved products from job artifacts or upstream snapshots
  - governed complementary search-result URLs such as `https://www.bastelschachtel.at/search?q=acryl+glas`

## Why This Rehaul Is Needed

The current system still behaves like a patchwork:

- Retool and Codex both try to shape article logic.
- Briefs and articles can arrive partial, malformed, or structurally weak.
- Product logic is too binary: either exact selected products exist or the article becomes thin.
- The article can read like a list of products rather than a credible craft guide.
- The pipeline can QA and rewrite, but it is not yet operating as the authoritative assembly engine.

The Filz sections in the Oster article exposed the core weakness clearly:

- the article stated time estimates
- but did not clearly say what the user is actually doing
- so the draft sounded plausible without being fully logical

That is exactly the kind of failure a canonical pipeline should prevent.

## New Baseline

The new default model is:

1. Inputs are gathered.
2. The pipeline infers the article intent and required structure.
3. The pipeline assigns product roles.
4. The pipeline decides where exact products are needed and where complementary search links are better.
5. The pipeline assembles the article from a governed content model.
6. The pipeline emits all publish artifacts.
7. QA validates against the same logic model that generated the article.

The system should stop behaving like:

- "Retool generated something, now Codex fixes it"

It should behave like:

- "Retool supplied ingredients, and the pipeline assembled the final article correctly"

## Canonical Responsibilities

`blog-seo-pipeline` should own:

- job intake and normalization
- schema-aware artifact discovery
- brief normalization
- article assembly
- article revision
- link policy
- complementary-product logic
- source and provenance handling
- SEO metadata generation
- excerpt generation
- handle generation
- image-usage logic
- QA and publish-readiness assessment

Retool should be treated as:

- a source of research and editorial inputs
- an optional preferred source of curated product choices
- not the final judge of article structure

## Content Logic Model

Every article section should answer four things clearly:

1. What is being made?
2. What does the user actually do?
3. Why would this idea suit this situation?
4. Which product link type belongs here?

This becomes the minimum logic unit for all item sections.

For example, a craft item section should not merely say:

- this felt bunny is nice
- it takes 15 to 20 minutes

It should instead specify the action model:

- assemble, decorate, fill, wrap, paint, hang, place, weave, or combine

If the exact project action is unknown from the product itself, the article must soften and reframe:

- from "make this in 15 minutes"
- to "use this as the base for a quick Osterfigur"

## Product Role System

Every linked product must be assigned one role before being placed into the article.

Allowed roles:

- core material
- project base
- optional enhancer
- finish/detail
- display/staging
- adjacent inspiration

Examples:

- Peddigrohr-Körbchen = project base
- Bastelfilz-Figur = project base or core material, depending on exact product
- Bastelwatte = optional enhancer
- Satinband = finish/detail
- Search link for `acryl glas` = adjacent inspiration or optional enhancer, never the core material unless the section is truly about acrylic projects

This role system solves the current problem where every product is treated as if it were equally central.

## Complementary Product Logic

The pipeline should support two product paths:

### Path A: Exact product linking

Use exact product URLs when:

- the item is central to the project
- the product is clearly the intended material or object
- the claim can be supported by the product title and context

### Path B: Complementary search-link expansion

Use search-result URLs when:

- the article needs a broader material family, not a single exact SKU
- the complementary product is relevant but not central enough to force a single product
- the category is better represented as a browse path
- the exact matching product set is too thin

Pattern:

- `https://www.bastelschachtel.at/search?q=<url-encoded-query>`

Example:

- `https://www.bastelschachtel.at/search?q=acryl+glas`

### Rules for search-link usage

Search links are allowed only when all of the following are true:

- they make the article more helpful, not more salesy
- they are introduced as optional complements, not mandatory hidden requirements
- they do not pretend to represent a single exact product
- the query is concrete and shopper-meaningful
- the section still stands if the reader ignores the complementary links

### Search-link query quality rules

Good:

- `acryl glas`
- `holz eier`
- `federn`
- `deko moos`

Bad:

- `bestes bastelmaterial ostern`
- `günstige kreative oster ideen`
- vague marketing phrases

## Article Assembly Model

The pipeline should assemble articles from governed blocks, not freeform drift.

Canonical output blocks:

1. `h1`
2. opener
3. quick-orientation block
4. decision helper or mini chooser
5. optional comparison table when useful
6. main sections
7. short recommendation close
8. FAQ
9. invisible provenance metadata in job artifacts, not public `Quellen` by default

### Main section contract

Each item section should contain:

- clear item title
- image
- practical framing
- explicit action model
- realistic time framing
- optional difficulty framing
- 1 to 3 product links max in the main body
- optional complementary search link only if it adds real help

### Main section anti-patterns

Do not allow:

- pure product admiration without a craft action
- exact time claims with no visible process
- sections that are only decorative filler
- five adjacent sections with the same sentence rhythm
- commerce blocks disguised as craft advice

## Article Truth Rules

The pipeline should distinguish between three claim levels:

### Strong claims

Allowed only if grounded by product reality or dossier evidence.

Examples:

- suitable as a table decoration
- can be combined with Bastelwatte
- quick to decorate

### Soft claims

Use when likely true but not fully evidenced.

Examples:

- works especially well if you want something quick
- can be a gentle project with children
- makes a nice small Easter greeting

### Forbidden claims

Do not allow:

- false specificity
- exact process claims without support
- made-up material behavior
- unverifiable difficulty precision

## Artifact Contract Rehaul

The job folder should evolve from "whatever Retool exported" into a canonical bundle consumed and emitted by the pipeline.

### Required inputs

- `job.json`
- `research-dossier.json`

### Preferred inputs

- `brief.md`
- `article.html`
- `selected-products.json`

### New normalized artifacts to add

- `normalized-brief.json`
- `article-plan.json`
- `link-map.json`
- `provenance.json`
- `seo-metadata.json`
- `publish-summary.md`

### Artifact purposes

- `normalized-brief.json`
  - machine-readable editorial structure after parsing markdown, fenced JSON, or partial inputs
- `article-plan.json`
  - canonical content outline with section intent, product roles, and required logic
- `link-map.json`
  - every outgoing link with role, confidence level, and reason
- `provenance.json`
  - evidence backing and notes for internal validation
- `seo-metadata.json`
  - title, meta description, excerpt, handle, optional social text
- `publish-summary.md`
  - short human summary of what is safe, what was softened, and where fallback logic was used

## Intake and Normalization Rules

The pipeline should gracefully handle these input realities:

- raw JSON brief
- markdown-wrapped JSON brief
- partial brief
- article seed HTML
- no article seed at all
- exact selected products present
- selected products missing but article-level SKU snapshot present
- no products at all, requiring search-link fallback

### Normalization priority

1. exact selected products from canonical job bundle
2. upstream article-level approved SKU snapshot
3. inferred product families from article plan
4. governed search-link complements

This avoids the current brittle behavior where local emptiness makes the pipeline act as if no product truth exists at all.

## QA Rehaul

QA should stop being a generic article critique and become a contract validator.

### QA must validate

- section logic completeness
- action-model clarity
- claim realism
- role-appropriate linking
- complementary search-link justification
- article rhythm and repetition
- image-shape risk
- metadata completeness
- provenance presence
- public-facing absence of `Quellen` unless explicitly requested

### New hard failures

- item section says how long it takes but not what the user does
- search-result link is used as if it were an exact product
- optional complement becomes an unstated requirement
- article includes product specificity beyond available evidence
- article section exists only to place a link

## Skill and Docs Changes

### `blog-seo-pipeline` skill

Update the skill to explicitly define:

- canonical-engine role
- assembly-first workflow
- product role system
- complementary search-link policy
- normalized artifact outputs
- public sources policy
- claim-strength ladder

### References to add or rework

- `references/article-assembly-model.md`
- `references/product-role-system.md`
- `references/complementary-linking-rules.md`
- `references/claim-strength-rules.md`
- `references/normalized-artifact-contract.md`

### Templates to rework

- QA report template
- revision plan template
- article skeleton template
- SEO metadata template
- publish summary template

## Prompt and Template Rehaul

The templates should stop prompting for "Top N listicle with products" in a shallow way.

They should instead force:

- what is the reader trying to make
- what is the smallest believable action
- which products are truly central
- which additions are optional
- what should be exact product URLs versus search links
- where the article should sound helpful rather than commercial

### New article template fields

- reader intent
- making mode
- section action verb
- section outcome
- core link
- optional complement links
- soft-claim boundaries

## Migration Strategy

### Phase 1: Canonical contracts

- define the new artifact contract
- define product roles
- define claim rules
- define complementary search-link rules

### Phase 2: Skill and template rewrite

- update `SKILL.md`
- add new reference docs
- replace or extend templates
- align README and integration docs

### Phase 3: Intake and fetch normalization

- parse multiple brief formats
- ingest upstream approved SKU snapshots
- emit normalized artifacts

### Phase 4: Assembly and QA convergence

- generate `article-plan.json`
- generate final article from plan
- run QA against the same plan

### Phase 5: Live article rehaul

- rework existing article drafts such as the Oster article against the new canonical logic

## Acceptance Criteria

The rehaul is successful when:

- the pipeline can create a publish-ready article from dossier plus thin inputs
- exact selected products are used when available
- complementary search links are used only where governed and helpful
- every section states a credible action model
- product links feel supportive, not forced
- the article, excerpt, meta title, and meta description all come from one coherent logic layer
- QA findings are mostly about real editorial quality, not broken contracts

## Immediate Next Work

1. Rewrite the skill and references around canonical ownership.
2. Define and document the normalized artifact contract.
3. Add complementary search-link rules and product-role taxonomy.
4. Update templates so article generation is action-led, not product-led.
5. Patch intake so `selected-products.json` can be enriched from upstream snapshots and governed search links.
6. Rebuild the Oster article under the new model.

## Recommendation

Do not treat this as a small prompt tweak.

This is a system-boundary change:

- from downstream QA helper
- to canonical article engine

That means the docs, templates, references, and artifact contract all need to change together. If only the prompt changes, the same incoherence will reappear in a different form.
