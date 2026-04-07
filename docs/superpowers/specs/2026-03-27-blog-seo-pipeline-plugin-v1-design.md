# Blog SEO Pipeline Plugin V1 Design

Date: 2026-03-27
Status: approved design draft
Scope: v1 only

## Purpose

This document narrows the broader plugin design down to the v1 system only.

The v1 plugin is a single-job content operating system for Bastelschachtel.

It exists to:

- discover content-job state from local and external artifacts
- normalize that state
- choose the correct mode
- execute QA or revision work reliably
- write structured local outputs
- establish the first canonical template system

It does not yet try to solve full topic-cluster generation.

## What V1 Is

V1 is:

- Retool-aware
- read-only against external systems
- write-capable locally
- discovery-first
- mode-aware
- family-aware
- template-governed

V1 is optimized for:

- quality
- alignment
- consistency
- template law

## What V1 Is Not

V1 is not:

- a full Retool replacement
- a cluster-generation engine
- a 3-20 article batch generator
- a write-back integration to Retool
- an unrestricted self-modifying system

## Entry Intent

The operator entrypoint should feel like:

- `blog me this latest keyword from retool`
- `blog me this dossier`
- `blog me this article folder`

The plugin must start from incomplete context and discover what exists.

## External and Local Discovery

V1 should inspect:

1. external read-only sources
2. local job folders
3. inferred Retool stage logic from canonical docs

External fetch is read-only in v1.
Local writing is allowed in v1.

## Canonical Process References

V1 should treat these as process law:

- `docs/reference/retool/README.md`
- `docs/reference/retool/process.md`
- `docs/reference/retool/research-lab-json-contract.md`
- `docs/reference/retool/content-factory-contract.md`
- `docs/reference/retool/integration-contract.md`
- `repo-skills/blog-seo-pipeline/references/run-modes.md`

V1 should also use these as seed and compatibility references for the plugin-owned output layer:

- `docs/reference/content-pipeline/README.md`
- `docs/reference/content-pipeline/v1-ingest-contract.md`
- `docs/reference/content-pipeline/retool-readonly-access-plan.md`
- `docs/reference/content-pipeline/retool-readonly-api-spec.md`
- `docs/reference/content-pipeline/run-modes.md`
- `docs/reference/content-pipeline/qa-report-template.md`
- `docs/reference/content-pipeline/revision-plan-template.md`
- `docs/reference/content-pipeline/seo-inference-rules.md`

Important:

- these files are inputs and compatibility baselines
- they are not the final canonical template law for the plugin
- the plugin should create and own its enhanced base layer after seeding from these references

## Normalized Job State

Minimum v1 normalized state:

- `topic`
- `locale`
- `primary_keyword`
- `format`
- `archetype`
- `family`
- `dossier`
- `brief`
- `selected_products`
- `article_html`
- `artifact_provenance`
- `confidence_flags`
- `mode`

### V1 metadata note

V1 should also reserve fields for:

- `subformat`
- `awareness_level`
- `cluster_role`

These do not need to drive full behavior yet, but they should exist in the model so v1 does not trap future expansion.

## V1 Modes

Supported modes:

- `qa-article`
- `revise-article`
- `audit-brief`

### V1 default rules

- if article markdown is present and the user did not ask for edits, default to `qa-article`
- if only a brief is present, default to `audit-brief`
- use `revise-article` only when the user explicitly asks for applied changes

The plugin must not infer `revise-article` from article presence alone.

## V1 Canonical Families

The initial canonical family set is:

- `deep-dive-guide`
- `product-comparison`
- `curation-listicle`

These are the first official template families for v1.

They should be auto-promoted once created and accepted as the baseline family set.

## Why These Three

They are the strongest overlapping result from the research set:

- `deep-dive-guide` for trust, process teaching, and beginner onboarding
- `product-comparison` for mixed intent and decision support
- `curation-listicle` for discovery and clickability

V1 should not promote glossary, directory, or persona-led systems into first-class template law yet.

## V1 Template Architecture

V1 should use a layered template model.

### Layers in scope

1. base layer
2. family overlay

### Layers reserved but not fully implemented

3. subformat overlay
4. awareness and cluster modifiers

### Base layer owns

- common QA structure
- common revision-plan structure
- product-truth ceiling rules
- brand voice rules
- publishability status rules
- output naming and placement rules

### Family overlay owns

- family-specific required sections
- family-specific failure modes
- family-specific SEO expectations
- family-specific commerce behavior
- family-specific revision priorities

## V1 Output Artifacts

Primary local outputs:

- `qa-report.md`
- `revision-plan.md`
- revised article markdown when the mode requires it

These must always be template-driven.

The plugin should:

1. collect structured findings
2. classify them
3. render them through template files

## Template Derivation Rule

The initial v1 templates should be derived from the latest finished content-job folders one level under:

- `output/content-jobs/`

The canonical compatibility skeleton for v1 job bundles should be:

- `output/content-jobs/_template/`

The first template-generation cycle should:

1. inspect the newest job folders
2. identify recurring useful output shape
3. compare that shape against `output/content-jobs/_template/`
4. use the existing repo templates and bundle skeleton as seed inputs
5. convert that shape into plugin-owned canonical base and family templates

After that, the plugin-owned canonical template files become the source of truth.

To avoid ambiguity with repo reference templates, plugin-owned templates should use an explicit naming marker such as:

- `*.plugin-base.tmpl`
- `*.plugin-family.tmpl`

The exact marker can be finalized in implementation, but it must clearly distinguish plugin-owned operational templates from repo reference templates.

## V1 Learning Loop

V1 should include a controlled learning loop after a successful run.

### Flow

1. finished job folder becomes candidate evidence
2. plugin classifies which family the run belonged to
3. plugin compares outputs against current base and family templates
4. plugin generates proposed template deltas

### Promotion policy

- ordinary changes remain proposed first
- only the initial 3 family templates are auto-promoted as the initial accepted baseline
- future updates should be family-scoped unless clearly base-level

### Safety rule

One finished job must not blindly rewrite template law.

## V1 Quality Gates

At minimum, v1 must enforce:

- dossier grounding
- brief alignment
- product-link integrity
- product-truth ceiling
- natural internal-link placement
- brand voice alignment
- structurally sound HTML
- publishability judgment

## V1 Success Criteria

V1 is successful if it can reliably do this:

1. accept an incomplete prompt like `blog me this latest keyword from retool`
2. discover the content-job state
3. select the correct mode
4. produce stable local outputs
5. classify the article into one of the three canonical families
6. improve future output quality through controlled template proposals

## Out of Scope for V1

Explicitly out of scope:

- cluster planning
- multi-article generation
- full pillar/spoke execution
- automatic interlink graph generation across many new pages
- write-back to Retool
- large-scale format experimentation

## Deferred Systems

These are intentionally postponed:

- subformat-specific behavior
- awareness-level-specific behavior
- cluster-role-specific behavior
- glossary family
- gift-guide family
- material-care family
- future cluster engine plugin

## Implementation Priority for V1

When planning implementation, use this order:

1. plugin boundary and command entry behavior
2. artifact discovery
3. job-state normalization
4. mode selection logic
5. base template system
6. family overlay system
7. output rendering
8. learning-loop proposal generation
9. initial template derivation from latest content-job folders

## Summary

V1 should do one thing very well:

take one Bastelschachtel content job from messy partial context to a correct, structured, high-quality local output.

Its most important durable output is the first stable base-and-family template system.

