# Run Modes

These are the first operational run modes for `blog-seo-pipeline`.

## Core Rule

The modes are not primarily distinguished by inputs.

`qa-article` and `revise-article` usually rely on the same bundle:

- research dossier
- brief
- article markdown
- selected products when available

The real distinction is:

- what the user wants done
- whether Codex should stop at evaluation or apply changes
- what output artifact should be produced

## 1. `qa-article`

Use when an article bundle is present and the user wants evaluation, QA, review, validation, or refinement advice without asking for direct edits.

Goal:

- assess the article against the dossier and brief
- produce a prioritized QA report
- identify what should change
- do not rewrite the full article unless explicitly asked

Default output:

- findings first
- then a short revision plan

## 2. `revise-article`

Use when an article bundle is present and the user clearly wants changes applied to the article itself.

Goal:

- identify the issues
- revise the article directly
- preserve the intended format and commerce constraints
- still surface the important issues, but treat the article draft as the primary output

Default output:

- improved article
- short summary of what changed

## 3. `audit-brief`

Use when the article does not exist yet, or when the user wants the brief evaluated before article generation.

Typical inputs:

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

- use `qa-article` when article markdown is present
- use `audit-brief` when only a brief is present
- use `revise-article` only when the user clearly wants changes applied

Do not infer `revise-article` from the presence of article markdown alone.

The deciding question is not "Do I have article markdown?"

It is:

- "Is the user asking for review?"
- or "Is the user asking for edits to be applied?"

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

## Operational Discipline

Before doing substantial work:

1. read this file
2. choose the mode explicitly
3. state the mode in the working context

If the mode is `qa-article`, do not drift into full article revision just because you see things you would improve.

