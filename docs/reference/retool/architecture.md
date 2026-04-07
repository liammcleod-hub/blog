# Retool Pipeline Architecture
#retool #content-pipeline

This document captures the current Bastelschachtel Retool content workflow at a systems level.

## Goal

The Retool app acts as a content and research pipeline for Bastelschachtel.

It currently supports:

- keyword/topic research
- SERP and competitor analysis
- strategic brief generation
- full article generation
- model selection per stage
- product selection from the Bastelschachtel catalog

## Operating Model

Current workflow is human-operated:

1. The user runs stages manually in Retool.
2. Retool produces structured artifacts for each stage.
3. Those artifacts can later be consumed by Codex for validation, refinement, SEO QA, and integration into a broader `blog-seo-pipeline`.

## Stage Overview

### 1. Research Lab

Purpose:

- research a keyword or topic
- gather cited source material
- derive competitor patterns
- infer search intents

Primary output:

- structured JSON dossier

Reference:

- [[docs/reference/retool/research-lab-json-contract]]

### 2. Content Factory

Purpose:

- take a saved research dossier
- choose content format and style
- map the keyword to relevant products in the Bastelschachtel catalog
- generate a strategic brief
- generate a full HTML article

Primary outputs:

- structured strategic brief
- HTML article draft

Reference:

- [[docs/reference/retool/content-factory-contract]]

## Related Docs

- [[docs/reference/retool/README]]
- [[docs/reference/retool/process]]
- [[docs/reference/retool/integration-contract]]

## Model Strategy

The app supports different model choices at different stages.

Known examples from the current workflow:

- Research Lab: Perplexity Sonar
- Brief generation: DeepSeek
- Full article generation: Claude 3.5 Sonnet

This is important because the pipeline is not using one model for everything. The stage-specific model choice is part of the workflow design.

## Integration Direction

The intended future direction is not to replace Retool, but to make Retool and Codex work as one coordinated system.

Recommended split of responsibilities:

- Retool handles operator controls, stage execution, model selection, and first-pass artifact generation.
- Codex handles orchestration, repo-aware context loading, content QA, SEO/AI-SEO review, logic checks, and final refinement.

## Artifact Chain

Current chain:

1. Research Lab JSON
2. Content Factory brief
3. Content Factory HTML article

Future Codex-driven chain may extend this with:

4. article QA report
5. SEO audit report
6. internal link validation
7. publish-ready final version
