# Blog SEO Pipeline Run Modes

This document defines the first operational run modes for the `blog-seo-pipeline` skill.

## Modes

- `qa-article`
- `revise-article`
- `audit-brief`

## `qa-article`

Purpose:

- inspect a generated article against the dossier and brief
- surface factual, structural, SEO, and commerce issues

Expected inputs:

- research dossier
- brief
- article HTML

Expected outputs:

- prioritized findings
- concise revision plan

## `revise-article`

Purpose:

- apply fixes directly to the generated article

Expected inputs:

- research dossier
- brief
- article HTML

Expected outputs:

- improved article
- short edit summary

## `audit-brief`

Purpose:

- inspect a generated brief before article generation

Expected inputs:

- research dossier
- brief
- optional selected products

Expected outputs:

- brief findings
- improved outline or correction plan
