from __future__ import annotations

from scripts.job_state import JobState
from scripts.mode_selection import select_mode


def test_select_mode_defaults_to_qa_when_article_exists():
    job_state = JobState(article_html="<h1>Article</h1>")

    assert select_mode(job_state, "blog me this local article") == "qa-article"


def test_select_mode_uses_revise_when_edit_intent_is_present():
    job_state = JobState(article_html="<h1>Article</h1>")

    assert select_mode(job_state, "please revise this article") == "revise-article"


def test_select_mode_falls_back_to_audit_brief():
    job_state = JobState(brief="Brief text")

    assert select_mode(job_state, "blog me this brief") == "audit-brief"
