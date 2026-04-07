from __future__ import annotations

from dataclasses import dataclass, field

from scripts.job_state import JobState


@dataclass
class Finding:
    severity: str
    issue: str
    evidence: str
    risk: str
    fix: str


@dataclass
class AnalysisResult:
    findings: list[Finding] = field(default_factory=list)
    passed_checks: dict[str, str] = field(default_factory=dict)
    residual_risks: list[str] = field(default_factory=list)
    publishability: str = "needs_review"
    revision_instructions: list[str] = field(default_factory=list)


def analyze_job(job_state: JobState) -> AnalysisResult:
    result = AnalysisResult()

    if job_state.dossier:
        result.passed_checks["dossier grounding"] = "present"
    else:
        result.findings.append(
            Finding("high", "Missing dossier", "No dossier loaded", "Unsupported claims", "Load or fetch the research dossier.")
        )

    if job_state.brief:
        result.passed_checks["brief alignment"] = "brief present"
    else:
        result.findings.append(
            Finding("medium", "Missing brief", "No brief loaded", "Weak article targeting", "Load or fetch the brief.")
        )

    if job_state.article_html:
        result.passed_checks["article html"] = "article present"
    elif job_state.mode != "audit-brief":
        result.findings.append(
            Finding("high", "Missing article", "No article markdown loaded", "Cannot run article QA", "Load or generate article markdown.")
        )

    if job_state.selected_products:
        result.passed_checks["product truth"] = "selected products present"
    else:
        result.residual_risks.append("Selected products missing; commerce claims should stay conservative.")

    if "faq" in (job_state.article_html or "").lower():
        result.passed_checks["faq coverage"] = "faq detected"
    elif job_state.family == "deep-dive-guide" and job_state.article_html:
        result.findings.append(
            Finding("medium", "Missing FAQ block", "No FAQ section detected", "Reduced beginner coverage", "Add a short FAQ section.")
        )

    result.publishability = "publishable" if not any(f.severity == "high" for f in result.findings) else "not_publishable"
    result.revision_instructions = [f.fix for f in result.findings]
    return result

