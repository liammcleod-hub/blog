# Run Modes

These are the first operational run modes for `blog-seo-pipeline`.

## 1. `qa-article`

Use when the user provides:

- research dossier
- brief
- article HTML

Goal:

- assess the article against the dossier and brief
- produce a prioritized QA report
- do not rewrite the full article unless asked

Default output:

- findings first
- then a short revision plan

## 2. `revise-article`

Use when the user provides:

- research dossier
- brief
- article HTML

Goal:

- identify the issues
- revise the article directly
- preserve the intended format and commerce constraints

Default output:

- improved article
- short summary of what changed

## 3. `audit-brief`

Use when the user provides:

- research dossier
- brief
- optional selected products

Goal:

- inspect whether the brief is strong enough before article generation
- catch weak angle, weak structure, unsupported claims, or bad product logic early

Default output:

- issues in the brief
- improved outline or brief recommendations

## Mode Selection Rule

If the user does not specify a mode:

- use `qa-article` when article HTML is present
- use `audit-brief` when only a brief is present
- use `revise-article` only when the user clearly wants changes applied

## Input Normalization Rule

Always normalize these fields when possible:

- topic
- locale
- primary keyword
- format
- archetype
- selected products
- citations

Missing fields should be inferred from the dossier or brief before asking the user.
