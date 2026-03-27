# Repo Skills Mirror

This folder stores repo-visible mirrors of local Codex skills so they survive normal Git workflows and are easy to inspect on any device.

## Current Rule

- Active runtime copy: `.agents/skills/...`
- Portable mirror copy: `repo-skills/...`

For `blog-seo-pipeline`, keep the active skill under `.agents/skills/blog-seo-pipeline` if you want Codex to auto-discover it from the repo.

The mirrored copy exists to make the skill easy to preserve, review, and recreate elsewhere if needed.
