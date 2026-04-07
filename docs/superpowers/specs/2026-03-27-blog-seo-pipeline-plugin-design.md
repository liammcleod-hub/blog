# Blog SEO Pipeline Plugin Design

Date: 2026-03-27
Status: approved design draft
Scope: v1 plugin design for Bastelschachtel content-job orchestration, QA, revision, and template governance

## Purpose

This document defines the v1 design for a Bastelschachtel `blog-seo-pipeline` plugin.

The plugin is not a generic article helper.
It is a Retool-aware content operating system for single content jobs.

Its job is to:

- discover content-job state from local and external artifacts
- normalize that state into one working model
- decide the next appropriate action
- execute QA or revision work in a controlled way
- write canonical local outputs
- maintain the base template system that later content automation can build on

This plugin complements Retool.
It does not replace the current Retool workflow.

## Why This Exists

The current workflow has these properties:

- research generation happens in Retool
- brief generation happens in Retool
- article generation happens in Retool
- product selection happens in Retool
- Codex is used for QA and refinement

That hybrid model works, but it is still too instruction-driven.
The operator has to rely on the model to remember:

- which artifacts to look for
- which mode should apply
- what counts as publishable
- how outputs should be structured
- how template improvements should be retained

The plugin exists to make that process stable, repeatable, and learnable across runs.

## Core Design Decision

The v1 plugin focuses on quality and alignment for one content job at a time.

It does not yet try to be the cluster-scale system that generates and interlinks large topic sets.

That cluster-scale layer should exist later as a separate system that consumes the canonical template law created by this plugin.

This separation is deliberate:

- `blog-seo-pipeline` plugin = truth engine
- future cluster engine = scale engine

## Inputs and Discovery Model

The plugin must support context-discovery-first execution.

The primary operator entrypoint is intended to feel like:

- `blog me this latest keyword from retool`
- `blog me this dossier`
- `blog me this article folder`

The plugin should not require the operator to already know whether a dossier, brief, article, or selected-product set exists.

Instead, it should discover state first.

### Supported starting hints

The request can begin from:

- latest keyword from Retool
- dossier id
- topic keyword
- job slug
- local job folder
- local article markdown path
- partial artifact bundle

### External data policy

v1 should be read-only against external systems.

That means:

- it may fetch from Retool-backed sources
- it may infer missing state from Retool process docs
- it writes only locally
- it does not persist changes back to Retool in v1

### Artifact priority

The plugin should inspect artifacts in this order:

1. external read-only sources
2. local job folder artifacts
3. inferred stage state from documented Retool logic

The plugin must treat `docs/reference/retool/` as canonical process law.

## Normalized Job State

All execution should run through a normalized job-state object.

Minimum fields:

- `topic`
- `locale`
- `primary_keyword`
- `format`
- `archetype`
- `family`
- `subformat`
- `awareness_level`
- `cluster_role`
- `dossier`
- `brief`
- `selected_products`
- `article_html`
- `artifact_provenance`
- `confidence_flags`
- `mode`

### Notes

- `family`, `subformat`, `awareness_level`, and `cluster_role` are first-class metadata
- they may be inferred when not explicitly present
- they should only be asked of the user if they cannot be reliably inferred from artifacts or process state

## Mode Model

The plugin must be discovery-first, then mode-aware.

Mode is not selected just from the presence of article markdown.

The plugin should:

1. discover the current content-job state
2. normalize the state
3. determine what stage the job is in
4. decide the next action based on user intent and job state

### Supported modes

- `qa-article`
- `revise-article`
- `audit-brief`

### Default mode rules

- if article markdown is present and the user did not ask for edits, default to `qa-article`
- if only a brief is present, default to `audit-brief`
- use `revise-article` only when the user explicitly asks for changes to be applied

The plugin must never infer `revise-article` from article presence alone.

## Family Model

The plugin should treat article families as intent families, not visual skins.

Initial canonical v1 families:

- `deep-dive-guide`
- `product-comparison`
- `curation-listicle`

### Family roles

#### `deep-dive-guide`

Best for:

- beginner onboarding
- tutorial intent
- technical trust
- process teaching

#### `product-comparison`

Best for:

- mixed informational-commercial queries
- decision support
- material or product choice

#### `curation-listicle`

Best for:

- discovery
- thematic product exploration
- clickability
- seasonal or topical roundups

## Subformat, Awareness, and Cluster Role

The family system must be extensible.

The plugin should be designed now for more granular template logic later.

### Subformat

Examples:

- `master-guide`
- `beginner-guide`
- `intermediate-guide`
- `troubleshooting-guide`
- `material-vs-material`
- `starter-choice`
- `seasonal-roundup`
- `gift-curation`

v1 does not need to fully implement every subformat.
But the metadata model must allow them now.

### Awareness level

Useful values:

- `discovery`
- `problem-aware`
- `solution-aware`
- `product-aware`
- `purchase-ready`

### Cluster role

Useful values:

- `pillar`
- `spoke`
- `support`
- `comparison`
- `conversion-support`
- `refresh`

These fields exist now so the future cluster engine can use them without changing the base plugin architecture.

## Template Architecture

The plugin should use a layered template system.

It should not rely on one freeform output style.

### Layers

1. base layer
2. family overlay
3. subformat overlay
4. awareness and cluster modifiers

### Base layer owns

- common QA structure
- common revision-plan structure
- product-truth ceiling rules
- brand voice rules
- evidence formatting rules
- publishability status rules
- output naming and placement rules

### Family overlay owns

- required section expectations
- family-specific failure modes
- family-specific SEO expectations
- family-specific commerce behavior
- family-specific revision priorities

### Subformat overlay owns

- role-specific structure
- role-specific section order
- role-specific title and promise pattern

### Awareness and cluster modifiers own

- audience framing
- CTA softness or directness
- internal-link expectation
- information depth

## Output Artifacts

The plugin should always write structured local artifacts.

Primary outputs:

- `qa-report.md`
- `revision-plan.md`
- revised article markdown when appropriate
- updated job metadata when needed

### Template-driven requirement

The plugin must not freehand these outputs.

It should:

1. collect structured findings
2. classify them
3. render them through repo-controlled templates

Initial template files should include at minimum:

- `templates/base/qa-report.md.tmpl`
- `templates/base/revision-plan.md.tmpl`
- family overlays for the three v1 families

## Template Source of Truth

The first generation of templates should be derived from the latest finished article-job folders.

That means:

1. inspect the newest directories under `output/content-jobs/`
2. extract stable and useful output structure
3. convert that structure into canonical templates
4. use those canonical templates for all future runs

The latest folders are the calibration set.
The canonical template files become the durable source of truth afterward.

## Learning Loop

The plugin should include a post-run learning loop.

After a successful run:

1. treat the finished job folder as candidate evidence
2. classify which family and subformat the run belonged to
3. compare outputs against the current base and family overlays
4. generate proposed template deltas
5. promote changes according to template promotion policy

### Important safety rule

The plugin must not blindly rewrite template law from one finished job.

It should generate structured deltas such as:

- promote this required section into `deep-dive-guide`
- tighten this wording rule in base
- do not promote because this is job-specific

## Promotion Policy

Template evolution should be controlled.

### Base rule

- normal template changes remain proposed first

### Accepted exception

If the first three canonical template families are being created and accepted as the initial baseline, they should be auto-promoted once approved.

That means the initial v1 family set:

- `deep-dive-guide`
- `product-comparison`
- `curation-listicle`

can be promoted automatically as the first official template family set after creation and acceptance.

### Family-scoped promotion

Future promotions should only affect:

- the relevant family overlay
- or the base layer if the change is clearly global

The plugin must avoid cross-family contamination.

## Internal Linking and Cluster Readiness

The user wants a future system where family items link to each other strongly.

That is correct, but the v1 plugin should not take on full cluster generation yet.

Instead, v1 should be cluster-ready.

It should support metadata that future systems need:

- `family`
- `subformat`
- `awareness_level`
- `cluster_role`
- related article references
- internal-link opportunities

The plugin should already be able to:

- suggest internal-link targets
- identify missing support links
- preserve link relevance rules

But it should not yet own 3-20 article cluster execution in v1.

## Future Separate System: Cluster Engine

The future multi-article topic-cluster system should be a separate plugin.

Recommended name:

- `blog-cluster-engine`

Purpose:

- topic expansion
- awareness-stage coverage
- pillar and spoke planning
- internal-link graph design
- batch generation sequencing
- cluster-level QA

Dependency:

It should consume the canonical templates and rules maintained by the `blog-seo-pipeline` plugin.

This preserves a clean boundary:

- article plugin creates template law
- cluster engine scales output using that law

## Retool Compatibility

The plugin must stay compatible with the current Retool operating model.

Rules:

- do not assume brief persistence exists unless confirmed
- do not assume article markdown persistence exists unless confirmed
- treat `research_dossiers` as the most reliable persisted artifact
- treat approved products and selected products as different concepts
- prefer canonical docs under `docs/reference/retool/`

## Quality Standard

The v1 plugin should optimize for:

- correctness
- brand fit
- product-truth discipline
- mode stability
- template law

It should not optimize for raw article volume.

The standard is:

- one content job handled correctly
- consistently
- with reusable output structure

That foundation is more important than prematurely scaling to large article clusters.

## Research Synthesis That Informs This Design

The following external research files informed the family and template decisions:

- `SERP Pattern Research.md`
- `Competitor Format Mapping.md`
- `CTR  Clickability Research.md`
- `Bastelschachtel Fit Assessment.md`
- `Template Family Design Research.md`
- `Future Playbook Expansion Research.md`

Key synthesis:

- the three strongest initial families remain `deep-dive-guide`, `product-comparison`, and `curation-listicle`
- directory-style content is not a strong initial bet for Bastelschachtel
- glossary or material-lexicon pages matter, but should remain future additions rather than initial template law
- Bastelschachtel wins through precision plus warmth, not generic ecommerce scale

## Implementation Guidance for the Next Planning Step

When implementation planning begins, prioritize this order:

1. plugin boundary and entrypoint behavior
2. job-state normalization
3. external and local artifact discovery
4. mode selection logic
5. template loading and rendering
6. family overlay system
7. learning-loop proposal generation
8. initial template derivation from latest content-job folders

Do not start with cluster generation.

## Open Questions Carried Forward

These are intentionally deferred, not unresolved:

- exact Retool fetch transport and credential model
- exact plugin manifest and local plugin folder location
- exact family overlay file naming
- exact structured finding schema
- whether revised article markdown should also be strictly template-rendered or partly rule-driven

They should be resolved in the implementation plan, not by changing the core design direction.

## Summary

The v1 `blog-seo-pipeline` plugin should be built as a discovery-first, Retool-aware, template-governed, single-job quality engine.

Its most important long-term output is not just better articles.
It is better template law.

That template law is what enables the future cluster system to scale content without losing quality, alignment, or brand voice.

