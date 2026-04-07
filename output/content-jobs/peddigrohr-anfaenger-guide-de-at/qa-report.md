# QA Report

## Findings

### Medium: Some project recommendations still rely on editorial fit more than explicit product facts

- Where: strength guidance and recommendation table, plus the project recommendation section in `article-revised.md`
- Problem: the articleâ€™s pairings are coherent for a beginner guide, but `selected-products.json` does not carry enough technical product detail to fully prove statements like which project is the better first step or when 3mm is the better choice.
- Consequence: the page reads credibly, but a stricter product-facts review would still classify parts of the recommendation layer as inference rather than hard-evidenced product truth.
- Recommended fix: if richer Retool product facts become available, tighten the wording around project suitability and material-strength fit even further.

### Low: The comparison intent is covered, but only as a short orientation block

- Where: the `Peddigrohr oder Holzschliff` section in `article-revised.md`
- Problem: this satisfies the mixed-intent requirement from the dossier and SEO inference rules, but it is intentionally brief and does not try to be a full material comparison page.
- Consequence: acceptable for this beginner guide, but it will not fully absorb comparison-intent traffic on its own.
- Recommended fix: keep this block short here and cover the deeper comparison in a dedicated article later if that query becomes a priority.

## What Checks Passed

- Dossier grounding: strong
- Brief alignment: strong
- Format/archetype match: strong for a beginner-focused deep-dive guide
- Tutorial intent coverage: strong; the article includes setup, first movement, common mistakes, and starter-project guidance
- Internal link coherence: strong; links stay within the selected-product set and are placed naturally in-body
- Brand voice: strong; warm, calm, practical, and not overly transactional
- HTML structure: strong; no obvious malformed anchors or runaway link issues

## Notes

- `run-modes.md` would have made `qa-article` the default mode for this handoff. This report reflects that mode.
- I did not find a raw-byte match for the usual mojibake markers during the follow-up scan, so any visible garbling in terminal output should be treated cautiously until verified in the actual publish/render environment.

## Publishability

- Status: publishable after normal editorial review
- Blocking issues: none confirmed
- Main residual risk: recommendation specificity is still limited by the thin product metadata in the current export bundle

