---
name: blog-seo-pipeline
description: Use when working on the Bastelschachtel blog pipeline, especially to ingest Retool research dossiers, briefs, and article markdown; validate SEO and logic quality; check product-link integrity; and refine content into a stronger publishable draft. Also use when the user wants Codex to operate alongside the Bastelschachtel Retool workflow rather than replace it.
---

# Blog SEO Pipeline

This skill is the Codex-side operator for the Bastelschachtel content system.

It complements Retool. It does not replace the current Retool workflow.

## Use This Skill For

- ingesting Retool research dossiers
- reviewing Retool-generated briefs
- auditing Retool-generated article markdown
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
- `references/run-modes.md`

Do not start QA or revision work until `references/run-modes.md` has been read and the active mode has been selected.

Also read these when useful:

- `docs/reference/Bastelschachtel Email Brand Voice Guide.md`
- `docs/strategy/BASTELSCHACHTEL MASTER BUSINESS CONTEXT.md`
- `docs/seo/bastelschachtel_seo_audit.docx`
- `brand_assets/brand_guidelines.md`
- `brand_assets/tone_doc.md`
- `brand_assets/voice_guidelines.md`
- `brand_assets/forbidden_phrases.md`
- `repo-skills/marketing-library/skills/seo-audit/SKILL.md`
- `repo-skills/marketing-library/skills/programmatic-seo/SKILL.md`
- `repo-skills/marketing-library/skills/ai-seo/SKILL.md`

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

## Mode Selection

Before doing any substantive work, select the active run mode from `references/run-modes.md`.

Default rule:

- if article markdown is present and the user did not ask for edits, use `qa-article`
- if only a brief is present, use `audit-brief`
- use `revise-article` only when the user explicitly asks for changes to be applied

Do not infer `revise-article` from the presence of article markdown alone.

State the chosen mode in the working context before proceeding.

## V1 Intake Modes

Support these input combinations:

### Mode 1: Full manual handoff

Inputs:

- research dossier JSON
- brief text or brief JSON
- article markdown
- selected products, if available

### Mode 2: Hybrid with Retool-backed dossier

Inputs:

- dossier identifier or dossier payload
- brief text or brief JSON
- article markdown
- selected products or approved product list

In this mode, use the integration contract to determine what can be fetched and what still needs to be supplied manually.

## V1 Workflow

1. Load the Retool process and contract docs.
2. Load `references/run-modes.md` and select the active mode.
3. Identify which stage artifact(s) are present in the job folder:
   - dossier
   - brief
   - article markdown
   - selected products
4. Normalize the job context:
   - topic
   - locale
   - format
   - archetype
   - primary keyword
   - approved product set
5. Execute according to mode:
   - `qa-article`: produce findings first, then a short revision plan
   - `revise-article`: identify issues, then revise the article directly
   - `audit-brief`: inspect the brief and propose outline or brief fixes
6. Keep recommendations compatible with the current Retool process unless the user asks to redesign it.

Do not produce an improved draft unless the active mode is `revise-article` or the user explicitly asks for applied changes.

## Required Inference Layer

Do not treat the brief as the only authority for what the article should contain.

When reviewing or revising an article, infer required content structure from all three of these inputs:

1. the research dossier
2. the Bastelschachtel SEO audit and gap map
3. the mirrored SEO skill library

This means the skill should ask:

- What content gaps does the Bastelschachtel audit say the site must close?
- What search-intent patterns dominate this topic?
- What content blocks do the SEO skills imply are necessary for this type of query?

If the brief under-specifies the page, the skill should still require the missing sections when they are strongly implied by the audit and SEO skill guidance.

Examples:

- a listicle may still need a definition block, FAQ, maintenance section, or comparison block
- a commerce article may still need informational sections if the search landscape is tutorial-heavy
- a page targeting list-style queries must still provide unique per-item value and not read like thin template output

Use this inference layer to judge whether the article actually matches the real search opportunity, not just whether it mechanically follows the brief.

## Brand Voice Layer

For Bastelschachtel content, do not stop at SEO correctness.

Also validate the article against the brand assets:

- `brand_assets/brand_guidelines.md`
- `brand_assets/tone_doc.md`
- `brand_assets/voice_guidelines.md`
- `brand_assets/forbidden_phrases.md`

The article should feel:

- warm
- personal
- helpful
- unhurried
- product-present but not product-dominated
- small-shop helpful rather than system-generated

Reject wording that exposes the pipeline or sounds machine-written, for example:

- `in deinem Setup`
- `in deinem aktuellen Produktkontext`
- tool-facing or system-facing phrasing
- overly optimized or catalog-like transitions
- research-exhaust sections that read like leftover dossier comparisons rather than real customer help

When SEO and brand voice are in tension, keep the search-intent coverage but rewrite the language so it still sounds like Bastelschachtel.

## QA Checklist

At minimum, check:

- claims are grounded in dossier evidence
- article structure matches the chosen format
- product mentions match selected or approved products
- internal product links are valid and consistent
- internal links are placed naturally in the body where relevant key phrases appear, not only dumped at the end
- linked anchor text matches the destination product truthfully and does not overclaim missing variants or specs
- primary and secondary keyword coverage is coherent
- title, intro, and sections align with the brief
- HTML markup is structurally sound, including balanced anchor boundaries and no runaway links
- German output is free of mojibake such as `fÃƒÂ¼r`, `StÃƒÂ¤rke`, `groÃƒÅ¸`, or `AnfÃƒÂ¤nger`
- final publishable article output does not default to a visible `Quellen` section unless the user explicitly wants public-facing sources
- when multiple product images appear, their presentation is intentionally normalized and does not crop essential product content
- the article adds information gain beyond obvious competitor summaries

Treat `selected-products.json` as the hard ceiling for product specificity. If the exact linked destination does not support a stronger claim, soften the language instead of inventing a more precise product variant.

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
- Do not assume article markdown persistence exists unless confirmed for the current run.
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
- `references/seo-inference-rules.md`
- `references/brand-voice-rules.md`
- `references/craft-language-rules.md`
