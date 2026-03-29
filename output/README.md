# Output

Read this file first when using `output/`.

## Purpose

This folder stores generated or workflow-output artifacts that support Bastelschachtel operations.

It is not one single system. Treat it as an output area with subfolders that each have their own rules.

## Main Subfolders

- `content-jobs/`
  Bastelschachtel blog/content workflow bundles for the `blog-seo-pipeline`
- `playwright/`
  browser captures and verification artifacts

## How To Use This Folder

When working in `output/`:

1. Read this `README.md`
2. Go to the relevant subfolder
3. Read that subfolder's `README.md` first when it exists

## Important Note

For Bastelschachtel blog workflow work, the most important subfolder here is:

- `output/content-jobs/`

Its own `README.md` is the source of truth for job-bundle structure and expected files.

## Working Rule

- Do not assume all files under `output/` are canonical source docs.
- Treat them as generated or process artifacts unless a subfolder README says otherwise.
