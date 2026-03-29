from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.analysis_engine import analyze_job
from scripts.discovery import discover_job
from scripts.family_classification import classify_family
from scripts.mode_selection import select_mode
from scripts.render_outputs import render_qa_report, render_revision_plan
from scripts.revision_engine import revise_article
from scripts.revision_writer import write_revised_article
from scripts.template_learning import generate_template_proposals

TEMPLATE_ROOT = PLUGIN_ROOT / "templates"


def parse_seed_target(user_input: str) -> dict[str, str]:
    raw = user_input.strip()
    lowered = raw.lower()

    if "latest keyword from retool" in lowered:
        return {"type": "external_latest_keyword", "value": "latest_keyword"}

    if "dossier" in lowered and "output" not in lowered:
        return {"type": "external_dossier", "value": raw}

    if lowered.startswith("blog me this "):
        raw = raw[len("blog me this ") :].strip()
    elif lowered.startswith("revise article "):
        raw = raw[len("revise article ") :].strip()

    path = Path(raw)
    if path.exists():
        return {"type": "local_path", "value": str(path)}

    raise ValueError(f"Could not parse target from input: {user_input}")


def run(user_input: str) -> dict[str, object]:
    seed_target = parse_seed_target(user_input)
    job_state = discover_job(seed_target)

    family, confidence = classify_family(job_state)
    job_state.family = family
    job_state.confidence_flags["family"] = confidence

    mode = select_mode(job_state, user_input)
    job_state.mode = mode

    analysis_result = analyze_job(job_state)
    qa_report = render_qa_report(job_state, analysis_result, TEMPLATE_ROOT)

    revised_path = None
    validation_notes: list[str] = []
    if mode == "revise-article":
        revised_html, validation = revise_article(job_state, analysis_result)
        validation_notes = validation.notes
        if validation.approved:
            revised_path = write_revised_article(Path(job_state.job_dir), revised_html, mode)

    revision_plan = render_revision_plan(job_state, analysis_result, validation_notes, TEMPLATE_ROOT)
    proposals = generate_template_proposals(job_state, qa_report, TEMPLATE_ROOT)

    if not job_state.job_dir:
        raise ValueError("Local job directory is required for plugin output writing.")
    job_dir = Path(job_state.job_dir)
    (job_dir / "qa-report.plugin.md").write_text(qa_report, encoding="utf-8")
    (job_dir / "revision-plan.plugin.md").write_text(revision_plan, encoding="utf-8")
    (job_dir / "template-proposals.plugin.json").write_text(
        json.dumps([asdict(proposal) for proposal in proposals], indent=2),
        encoding="utf-8",
    )

    return {
        "mode": mode,
        "family": family,
        "job_dir": str(job_dir),
        "revised_path": str(revised_path) if revised_path else None,
        "proposal_count": len(proposals),
    }


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/blog_me_this.py \"blog me this <target>\"")
    result = run(sys.argv[1])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
