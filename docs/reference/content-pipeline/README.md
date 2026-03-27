# Content Pipeline References

This folder contains Codex-side references for the Bastelschachtel blog SEO pipeline.

These docs sit on top of the Retool references and define how Codex should ingest, validate, and eventually fetch pipeline artifacts.

## Documents

- `v1-ingest-contract.md`: first narrow handoff contract for QA and refinement
- `retool-readonly-access-plan.md`: read-only access plan for Retool-backed data
- `retool-readonly-api-spec.md`: proposed thin API surface for Retool-backed reads
- `run-modes.md`: first operational modes for using the skill
- `qa-report-template.md`: expected QA output structure
- `revision-plan-template.md`: expected revision planning structure
- `seo-inference-rules.md`: rules for inferring required content structure from audit + SEO skills

## Related Runtime Folder

The preferred working bundle location for actual article jobs is:

- `output/content-jobs/`
