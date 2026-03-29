from __future__ import annotations

from pathlib import Path

from scripts.analysis_engine import AnalysisResult, Finding
from scripts.job_state import JobState
from scripts.render_outputs import render_qa_report, render_revision_plan
from scripts.revision_writer import write_revised_article


TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"


def test_render_qa_report_includes_required_sections():
    text = render_qa_report(
        JobState(topic="peddigrohr"),
        AnalysisResult(
            findings=[Finding("medium", "Missing FAQ block", "No FAQ", "Reduced coverage", "Add FAQ")],
            passed_checks={"brief alignment": "brief present"},
            residual_risks=["Product set missing"],
            publishability="publishable",
        ),
        TEMPLATE_ROOT,
    )

    assert "## Findings" in text
    assert "## Coverage Checks" in text
    assert "## Priority Fixes" in text
    assert "## Residual Risks" in text
    assert "## Publishability" in text


def test_render_revision_plan_includes_required_sections():
    text = render_revision_plan(
        JobState(topic="peddigrohr", family="deep-dive-guide"),
        AnalysisResult(findings=[]),
        [],
        TEMPLATE_ROOT,
    )

    assert "## Objective" in text
    assert "## Required Fixes" in text
    assert "## Recommended Improvements" in text
    assert "## Edit Strategy" in text
    assert "## Validation Notes" in text


def test_write_revised_article_only_writes_in_revise_mode(tmp_path: Path):
    assert write_revised_article(tmp_path, "<h1>Article</h1>", "qa-article") is None

    written = write_revised_article(tmp_path, "<h1>Article</h1>", "revise-article")

    assert written == tmp_path / "article-revised.plugin.html"
    assert written.exists()
