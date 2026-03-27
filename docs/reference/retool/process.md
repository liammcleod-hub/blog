# Retool Operator Process

This document records the current step-by-step Bastelschachtel Retool workflow exactly as it is being used now.

## End-to-End Flow

1. Start with a keyword in Research Lab.
2. Run research with the chosen model and source count.
3. Save and reuse the resulting research dossier.
4. Move to Content Factory.
5. Choose the brief model and article model.
6. Choose output format and content style archetype.
7. Select a previously generated research dossier.
8. Let the system map the keyword to matching catalog products.
9. Select which mapped products should be included.
10. Generate the brief.
11. Generate the full article in HTML.

## Research Lab

The operator enters:

- keyword/topic
- locale
- research type
- optional competitor URL
- source count
- model

The current example model is:

- Perplexity Sonar

Research Lab can produce different research modes, including:

- general research dossier
- SERP landscape
- competitor overview
- product research

The output is a JSON dossier containing:

- topic metadata
- summary
- citations
- competitor blueprints
- competitor findings
- search intents

Reference:

- `research-lab-json-contract.md`

## Content Factory

After research is complete, the operator moves to the Content Factory tab.

### Model selection

The operator chooses:

- brief model
- article model

Current example configuration:

- brief model: DeepSeek
- article model: Claude 3.5 Sonnet

### Output format

The operator chooses one of:

- deep dive guide
- listicle
- product comparison
- expert hacks

The descriptions currently understood for these are:

- deep dive guide: instructional
- listicle: top-n list
- product comparison: buy-review focus
- expert hacks: information-gain focus

### Content style archetype

The operator chooses one of:

- listicle
- deep dive
- product comparison
- expert hacks
- advertorial
- gift guide

### Research dossier selection

The operator selects a saved research dossier generated from Research Lab.

This selected dossier acts as the upstream intelligence for the Content Factory stage.

### Product mapping

After dossier selection, the keyword is mapped against the Bastelschachtel product CSV list stored in the Retool database.

Current mapping behavior:

- simple keyword-to-product-title matching

The system returns relevant catalog products, and the operator can decide which products should be included or excluded in the article.

### Brief generation

Once products are selected, the operator generates the brief.

The brief contains:

- topic
- format
- working title
- angle
- hook options
- key takeaways
- format-specific outline
- internal linking plan
- SEO block
- FAQ
- visual plan

### Article generation

After the brief is created, the operator generates the article.

Current article output format:

- HTML only

The generated article can include:

- heading hierarchy
- intro
- short-answer section
- product sections
- product links
- product images
- bullet lists
- care/how-to sections
- source references

## Important Current Constraints

- Retool is the active execution layer.
- The operator presses the buttons manually.
- Product selection is informed by keyword-to-title mapping, not yet deeper semantic retrieval.
- The article is currently returned as HTML only.
- The brief and article stages may use different models.

## Why This Matters

This process is the real current production workflow.

Future automation or Codex integration must preserve compatibility with this operator flow rather than inventing a disconnected process.
