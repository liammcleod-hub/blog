from __future__ import annotations

import importlib.util
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKS_PATH = SKILL_ROOT / "scripts" / "checks.py"
FIXTURE_REPO = SKILL_ROOT / "tests" / "fixtures" / "generic-repo"


def load_module():
    spec = importlib.util.spec_from_file_location("checks", CHECKS_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_config() -> dict:
    return {
        "graph_roots": ["docs/seo", "docs/reference"],
        "forbidden_roots": ["output"],
        "repo_facing_navigation_docs": ["README.md", "docs/reference/README.md"],
        "tag_rules": {
            "default_note_position": "below_h1",
            "allowed_tags": ["seo", "reference"],
            "zone_defaults": {},
        },
        "skill_note_rules": {
            "roots": ["repo-skills/marketing-library/skills"],
            "bottom_only_tag": "#skills",
        },
        "normalization_candidates": ["docs/reference/legacy-notes.txt"],
        "normalization_exclusions": ["output/generated/article.html"],
        "fix_permissions": {
            "allow_link_fixes": True,
            "allow_tag_fixes": True,
            "allow_format_normalization": False,
        },
    }


def test_checks_report_expected_finding_classes():
    module = load_module()
    findings = module.run_checks(FIXTURE_REPO, sample_config())
    kinds = {finding["kind"] for finding in findings}

    assert "missing_upward_link" in kinds
    assert "hidden_fake_click_target" in kinds
    assert "visible_note_plain_path" in kinds
    assert "missing_bottom_skill_tag" in kinds
    assert "titleless_tag_ambiguity" in kinds
