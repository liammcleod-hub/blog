# Retool Read-Only Plan

This reference defines the intended read-only integration posture for the first Retool connection.

## Read-Only Scope

Codex should only read from Retool-related systems in the first integration phase.

No write-back is required for v1.

## Preferred Fetch Order

1. `research_dossiers`
2. `product_keyword_approvals`
3. `product_catalog`
4. optional intelligence-hub tables such as `product_facts`

## Why This Order

- dossier is the strongest persisted research artifact
- approved products enforce commerce constraints
- product catalog helps validate handles and URLs
- product facts can improve factual QA

## Still Manual in V1

Until persistence is improved, these may still need to be passed in manually:

- generated brief
- final article markdown

## Integration Goal

The first DB or API connection should make it possible to fetch enough context for article QA without changing the current Retool authoring workflow.

