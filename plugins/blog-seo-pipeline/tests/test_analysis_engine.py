from __future__ import annotations

from scripts.analysis_engine import analyze_job
from scripts.job_state import JobState


def test_analyze_job_marks_publishable_with_grounding():
    job_state = JobState(
        family="deep-dive-guide",
        dossier={"topic": "peddigrohr"},
        brief="brief",
        article_html="<h1>Article</h1><h2>FAQ</h2>",
        selected_products=[],
    )

    result = analyze_job(job_state)

    assert result.publishability == "publishable"
    assert result.passed_checks["dossier grounding"] == "present"
    assert result.passed_checks["faq coverage"] == "faq detected"


def test_analyze_job_flags_missing_article_for_non_brief_mode():
    job_state = JobState(dossier={"topic": "peddigrohr"}, brief="brief", mode="qa-article")

    result = analyze_job(job_state)

    assert any(finding.issue == "Missing article" for finding in result.findings)
