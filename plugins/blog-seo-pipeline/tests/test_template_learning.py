from __future__ import annotations

from pathlib import Path

from scripts.job_state import JobState
from scripts.template_learning import generate_template_proposals


TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"


def test_template_learning_generates_proposals_without_auto_promote():
    proposals = generate_template_proposals(
        JobState(family="deep-dive-guide"),
        "# QA Report\n\nFAQ coverage remains important.",
        TEMPLATE_ROOT,
    )

    assert proposals
    assert any(proposal.action == "no_auto_promote" for proposal in proposals)
