from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from scripts.job_state import JobState


@dataclass
class TemplateProposal:
    target: str
    action: str
    reason: str


def generate_template_proposals(job_state: JobState, qa_report_text: str, template_root: Path) -> list[TemplateProposal]:
    proposals: list[TemplateProposal] = []
    if "FAQ" in qa_report_text and job_state.family == "deep-dive-guide":
        proposals.append(
            TemplateProposal(
                target="deep-dive-guide.plugin-family.tmpl",
                action="keep_required_section",
                reason="Deep-dive jobs repeatedly expect an FAQ block.",
            )
        )
    proposals.append(
        TemplateProposal(
            target="qa-report.plugin-base.tmpl",
            action="no_auto_promote",
            reason="Ordinary runs must generate proposals without silently rewriting templates.",
        )
    )
    return proposals
