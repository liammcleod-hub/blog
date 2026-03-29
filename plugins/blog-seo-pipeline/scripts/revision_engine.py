from __future__ import annotations

from dataclasses import dataclass, field

from scripts.analysis_engine import AnalysisResult
from scripts.job_state import JobState


@dataclass
class RevisionValidation:
    approved: bool
    notes: list[str] = field(default_factory=list)


def validate_revision(job_state: JobState, revised_html: str) -> RevisionValidation:
    notes: list[str] = []
    if job_state.family == "deep-dive-guide" and "faq" not in revised_html.lower():
        notes.append("FAQ section missing for deep-dive guide.")
    return RevisionValidation(approved=not notes, notes=notes)


def revise_article(job_state: JobState, analysis_result: AnalysisResult) -> tuple[str, RevisionValidation]:
    html = job_state.article_html or ""
    revised = html

    if job_state.mode != "revise-article":
        return revised, RevisionValidation(approved=True, notes=["Revision skipped outside revise-article mode."])

    if "faq" not in revised.lower():
        revised += "\n<h2>FAQ</h2>\n<p>Weitere Antworten fuer Einsteiger folgen hier.</p>\n"

    if analysis_result.findings and "<h2>Next Steps</h2>" not in revised:
        revised += "\n<h2>Next Steps</h2>\n<p>Arbeite die empfohlenen Korrekturen fuer einen sauberen Publish-Stand ein.</p>\n"

    validation = validate_revision(job_state, revised)
    return revised, validation
