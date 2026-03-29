# Blog Cluster Engine Phase Plan

Date: 2026-03-29

## Goal

Define and execute the next phase after `blog-seo-pipeline` v1:

- create a repo-owned spinoff article template library
- define the second plugin boundary clearly
- prepare the future cluster plugin to consume those templates instead of inventing them

This phase does **not** assume the second plugin should create template law.

The template law for spinoff article systems should live in repo docs and be deliberately authored by humans.

## Core Design Decision

Use this separation:

- `blog-seo-pipeline`
  - single-job truth engine
  - QA, revision, and template-law consumer on the article side

- repo docs template library
  - source of truth for spinoff article template families
  - stable, reviewable, editable by humans

- future `blog-cluster-engine`
  - scale engine
  - chooses the right template
  - assigns cluster role and sequencing
  - creates cluster outputs using repo-defined templates

## Why This Is Better

This approach is better than letting plugin 2 create its own templates because:

- Bastelschachtel's blog system is still being actively shaped
- template quality needs deliberate editorial control
- repo docs are easier to review than plugin-internal inferred rules
- the cluster plugin should scale decisions, not invent Bastelschachtel strategy
- both humans and plugins can use the same source material

## Recommended Approaches

### Approach A: Shared Repo-Docs Template Library

Create a dedicated repo-docs template library and make the future cluster plugin consume it.

Pros:
- cleanest source of truth
- easy to review and evolve
- works for both humans and plugins
- easiest to align with Bastelschachtel voice and SEO strategy

Cons:
- requires some upfront template authoring before the plugin can scale

### Approach B: Cluster Plugin-Owned Templates

Put all spinoff templates inside the second plugin and manage them there.

Pros:
- all cluster logic and template files live together

Cons:
- weaker editorial visibility
- harder for humans to use directly
- risks drift between repo strategy docs and plugin internals

### Approach C: Hybrid With Generated Plugin Templates

Author repo-doc templates first, then copy or compile them into plugin-owned runtime templates.

Pros:
- runtime-friendly
- still preserves a human-facing source

Cons:
- more moving parts
- needs version-sync discipline

## Recommendation

Use **Approach A** for this phase.

If runtime needs later demand a compilation step, add that later as a thin compatibility layer.

Do **not** start with plugin-owned template creation.

## Phase Scope

This phase should produce:

1. a stable repo-docs template library for spinoff article systems
2. a clear design spec for the second plugin
3. a selection model the future plugin can use
4. initial mapping between category / intent / cluster role and template choice

This phase should **not** yet require:

- full cluster-plugin implementation
- autonomous template generation
- write-back integration
- large-scale batch drafting

## Proposed Folder Direction

Create a repo-doc template area that is intentionally human-readable and plugin-consumable.

Recommended direction:

- `docs/reference/blog-templates/`

Suggested structure:

- `docs/reference/blog-templates/README.md`
- `docs/reference/blog-templates/base/`
- `docs/reference/blog-templates/families/`
- `docs/reference/blog-templates/subformats/`
- `docs/reference/blog-templates/modifiers/`
- `docs/reference/blog-templates/mappings/`

## Template System Shape

The second plugin should be designed to consume layered repo templates.

### Base layer

Owns:
- evidence rules
- Bastelschachtel voice rules
- SEO hygiene rules
- link-discipline rules
- product-truth rules

### Family layer

Owns high-level article family behavior such as:
- `deep-dive-guide`
- `product-comparison`
- `curation-listicle`
- future families when justified

### Subformat layer

Owns role-specific shapes such as:
- `master-article`
- `spinoff-support`
- `beginner-guide`
- `troubleshooting-guide`
- `material-vs-material`
- `starter-choice`
- `gift-curation`
- `seasonal-roundup`

### Modifier layer

Owns:
- awareness stage
- cluster role
- internal-link expectations
- CTA intensity

## What The Second Plugin Should Eventually Do

The future `blog-cluster-engine` should:

- expand a topic into a cluster
- assign article roles
- choose the right repo template
- sequence execution
- define internal-link relationships
- create structured article jobs or cluster plans
- run cluster-level QA

It should **not** be responsible for inventing the templates it uses.

## Phase Deliverables

### Deliverable 1: Template Library Spec

Define:
- folder layout
- naming rules
- what each layer owns
- how plugins reference the templates

### Deliverable 2: Initial Template Set

Author the first human-owned spinoff template documents.

Recommended initial set:
- `master-article`
- `support-spoke`
- `comparison-spoke`
- `conversion-support`
- `refresh-update`

These are roles, not final mandatory names. Naming can be adjusted during spec work.

### Deliverable 3: Template Selection Matrix

Create a mapping document that answers:
- which template fits which search intent
- which template fits which category situation
- which cluster role should support which page type

### Deliverable 4: Cluster Plugin Spec

Write the second plugin design around:
- inputs
- selection logic
- outputs
- dependency on repo template docs

### Deliverable 5: Implementation Plan

After the spec is approved, write a separate implementation plan for:
- repo template library creation
- plugin scaffold
- selection engine
- cluster output artifacts

## Suggested Execution Order

### Step 1

Write the repo-doc template library spec.

### Step 2

Define the initial template families and subformats.

### Step 3

Write the template selection matrix.

### Step 4

Write the `blog-cluster-engine` plugin design against that repo template library.

### Step 5

Write the implementation plan.

## Suggested Inputs

When authoring the templates and plugin spec, use:

- `docs/reference/skill-guides/blogs.md`
- `docs/customer reviews/`
- `docs/seo/`
- `.agents/product-marketing-context.md`
- `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-design.md`

The point is to keep the second system grounded in:
- Bastelschachtel VOC
- Bastelschachtel SEO priorities
- the boundary already established by plugin 1

## Working Rule For This Phase

If there is tension between:
- plugin convenience
- and editorial control

choose editorial control first.

The templates are the long-term leverage point.

## Success Criteria

This phase is successful when:

1. the template library exists in repo docs
2. it has a stable README-first entrypoint
3. the second plugin can be specified as a consumer of that library
4. template choice logic is explicit enough to implement later
5. no one has to guess whether plugin 2 owns template creation

## Recommended Immediate Next Move

Start by writing a design spec for:

- the repo-docs template library
- and the second plugin's dependency on it

Do not start by coding the second plugin.
