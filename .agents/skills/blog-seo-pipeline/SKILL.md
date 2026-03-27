---
name: blog-seo-pipeline
description: Use when working on the Bastelschachtel blog pipeline, especially to ingest Retool research dossiers, briefs, and article HTML; validate SEO and logic quality; check product-link integrity; and refine content into a stronger publishable draft. Also use when the user wants Codex to operate alongside the Bastelschachtel Retool workflow rather than replace it.
---

# Blog SEO Pipeline

This skill is the Codex-side operator for the Bastelschachtel content system.

It complements Retool. It does not replace the current Retool workflow.

## Use This Skill For

- ingesting Retool research dossiers
- reviewing Retool-generated briefs
- auditing Retool-generated article HTML
- validating SEO coverage, logic, and source grounding
- checking product-link integrity against approved or selected products
- improving article quality before publishing
- planning future read-only Retool integration

## First Read

Read these repo references before doing pipeline work:

- `docs/reference/retool/README.md`
- `docs/reference/retool/process.md`
- `docs/reference/retool/research-lab-json-contract.md`
- `docs/reference/retool/content-factory-contract.md`
- `docs/reference/retool/integration-contract.md`

Also read these when useful:

- `docs/reference/Bastelschachtel Email Brand Voice Guide.txt`
- `docs/strategy/BASTELSCHACHTEL MASTER BUSINESS CONTEXT.txt`

## Current Operating Model

Retool currently handles:

- research generation
- brief generation
- article generation
- product selection

Codex currently handles:

- repo-aware context loading
- process understanding
- QA and refinement
- future orchestration design

Assume a hybrid workflow unless the user explicitly says otherwise.

## V1 Intake Modes

Support these input combinations:

### Mode 1: Full manual handoff

Inputs:

- research dossier JSON
- brief text or brief JSON
- article HTML
- selected products, if available

### Mode 2: Hybrid with Retool-backed dossier

Inputs:

- dossier identifier or dossier payload
- brief text or brief JSON
- article HTML
- selected products or approved product list

In this mode, use the integration contract to determine what can be fetched and what still needs to be supplied manually.

## V1 Workflow

1. Load the Retool process and contract docs.
2. Identify which stage artifact(s) were provided:
   - dossier
   - brief
   - article HTML
   - selected products
3. Normalize the job context:
   - topic
   - locale
   - format
   - archetype
   - primary keyword
   - approved product set
4. Validate the article against the dossier and brief.
5. Produce one of:
   - QA report
   - revision plan
   - improved draft
6. Keep recommendations compatible with the current Retool process unless the user asks to redesign it.

## QA Checklist

At minimum, check:

- claims are grounded in dossier evidence
- article structure matches the chosen format
- product mentions match selected or approved products
- internal product links are valid and consistent
- primary and secondary keyword coverage is coherent
- title, intro, and sections align with the brief
- source section exists and is consistent with citations used
- the article adds information gain beyond obvious competitor summaries

## Review Priorities

Prioritize issues in this order:

1. factual unsupported claims
2. invalid or mismatched product links
3. format/archetype mismatch
4. SEO coverage gaps
5. weak information gain
6. awkward structure or style

## Retool Compatibility Rules

- Do not assume brief persistence exists unless confirmed for the current run.
- Do not assume article HTML persistence exists unless confirmed for the current run.
- Treat `research_dossiers` as the most reliable current persisted artifact.
- Treat approved products and locked products as different concepts.
- Prefer using the canonical docs under `docs/reference/retool/` rather than restating the process from memory.

## References

For v1 workflow details:

- `references/v1-ingest-and-qa.md`

For read-only integration planning:

- `references/retool-readonly-plan.md`

For operational execution:

- `references/run-modes.md`
- `references/qa-report-template.md`
- `references/revision-plan-template.md`
