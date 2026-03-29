from __future__ import annotations

from pathlib import Path

from scripts.analysis_engine import AnalysisResult
from scripts.job_state import JobState


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _format_findings(analysis_result: AnalysisResult) -> str:
    if not analysis_result.findings:
        return "- No blocking findings."
    lines = []
    for finding in analysis_result.findings:
        lines.append(f"### {finding.severity.title()}: {finding.issue}")
        lines.append(f"- issue: {finding.issue}")
        lines.append(f"- evidence: {finding.evidence}")
        lines.append(f"- risk: {finding.risk}")
        lines.append(f"- fix: {finding.fix}")
        lines.append("")
    return "\n".join(lines).strip()


def _format_coverage(analysis_result: AnalysisResult) -> str:
    if not analysis_result.passed_checks:
        return "- No checks passed."
    return "\n".join(f"- {key}: {value}" for key, value in analysis_result.passed_checks.items())


def _format_priority_fixes(analysis_result: AnalysisResult) -> str:
    fixes = [finding.fix for finding in analysis_result.findings]
    if not fixes:
        return "- No required fixes."
    return "\n".join(f"- {fix}" for fix in fixes)


def _format_residual_risks(analysis_result: AnalysisResult) -> str:
    if not analysis_result.residual_risks:
        return "- No material residual risks."
    return "\n".join(f"- {risk}" for risk in analysis_result.residual_risks)


def render_qa_report(job_state: JobState, analysis_result: AnalysisResult, template_root: Path) -> str:
    template = _read(template_root / "base" / "qa-report.plugin-base.tmpl")
    return template.format(
        findings_section=_format_findings(analysis_result),
        coverage_checks_section=_format_coverage(analysis_result),
        priority_fixes_section=_format_priority_fixes(analysis_result),
        residual_risks_section=_format_residual_risks(analysis_result),
        publishability_section=analysis_result.publishability,
    )


def render_revision_plan(
    job_state: JobState,
    analysis_result: AnalysisResult,
    validation_notes: list[str],
    template_root: Path,
) -> str:
    template = _read(template_root / "base" / "revision-plan.plugin-base.tmpl")
    objective = f"Improve {job_state.family or 'article'} for topic '{job_state.topic or 'unknown'}'."
    required_fixes = _format_priority_fixes(analysis_result)
    recommended = "- Tighten copy only after factual and structural fixes." if analysis_result.findings else "- No extra improvements required."
    edit_strategy = "full rewrite" if validation_notes else "surgical patch"
    validation = "\n".join(f"- {note}" for note in validation_notes) if validation_notes else "- Validation passed."
    return template.format(
        objective_section=objective,
        required_fixes_section=required_fixes,
        recommended_improvements_section=recommended,
        edit_strategy_section=edit_strategy,
        validation_notes_section=validation,
    )
