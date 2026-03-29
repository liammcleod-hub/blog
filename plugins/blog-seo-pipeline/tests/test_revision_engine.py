from __future__ import annotations

from scripts.analysis_engine import AnalysisResult, Finding
from scripts.job_state import JobState
from scripts.revision_engine import revise_article


def test_revise_article_skips_outside_revise_mode():
    html, validation = revise_article(
        JobState(mode="qa-article", article_html="<h1>Article</h1>", family="deep-dive-guide"),
        AnalysisResult(),
    )

    assert html == "<h1>Article</h1>"
    assert validation.approved is True
    assert "skipped" in validation.notes[0].lower()


def test_revise_article_adds_required_sections_in_revise_mode():
    analysis_result = AnalysisResult(
        findings=[
            Finding("medium", "Missing FAQ block", "No FAQ", "Reduced coverage", "Add a short FAQ section."),
        ]
    )
    html, validation = revise_article(
        JobState(mode="revise-article", article_html="<h1>Article</h1>", family="deep-dive-guide"),
        analysis_result,
    )

    assert "<h2>FAQ</h2>" in html
    assert "<h2>Next Steps</h2>" in html
    assert validation.approved is True
