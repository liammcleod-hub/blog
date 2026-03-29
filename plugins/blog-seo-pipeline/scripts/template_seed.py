from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TemplateSeedResult:
    ok: bool
    calibration_sources: list[str]


def validate_template_seed(template_root: Path) -> TemplateSeedResult:
    required = [
        template_root / "base" / "qa-report.plugin-base.tmpl",
        template_root / "base" / "revision-plan.plugin-base.tmpl",
        template_root / "families" / "deep-dive-guide.plugin-family.tmpl",
        template_root / "families" / "product-comparison.plugin-family.tmpl",
        template_root / "families" / "curation-listicle.plugin-family.tmpl",
    ]
    ok = all(path.exists() for path in required)
    return TemplateSeedResult(
        ok=ok,
        calibration_sources=[
            "output/content-jobs/_template/",
            "docs/reference/content-pipeline/qa-report-template.md",
            "docs/reference/content-pipeline/revision-plan-template.md",
        ],
    )
