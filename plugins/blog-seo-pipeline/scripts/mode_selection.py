from __future__ import annotations

from scripts.job_state import JobState


def select_mode(job_state: JobState, user_request: str = "") -> str:
    request = user_request.lower()
    wants_edit = any(token in request for token in ["revise", "rewrite", "edit", "apply", "fix article"])

    if job_state.article_html:
        return "revise-article" if wants_edit else "qa-article"
    if job_state.brief:
        return "audit-brief"
    return "audit-brief"
