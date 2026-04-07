from __future__ import annotations

import importlib.util
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "reporting.py"


def load_module():
    spec = importlib.util.spec_from_file_location("reporting", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_render_init_report_contains_summary_counts():
    module = load_module()
    proposals = {
        "graph_roots": ["docs/seo"],
        "forbidden_roots": ["output"],
        "repo_facing_navigation_docs": ["README.md"],
        "skill_note_roots": ["repo-skills/marketing-library/skills"],
        "normalization_candidates": ["docs/legacy.txt"],
        "normalization_exclusions": ["output/generated/article.html"],
    }

    report = module.render_init_report("C:/repo", proposals)

    assert "obsidian-this init: configured repo C:/repo" in report
    assert "- graph roots: 1" in report
    assert "- normalization exclusions: 1" in report


def test_render_check_report_contains_findings_count():
    module = load_module()
    config = {
        "graph_roots": ["docs/seo"],
        "forbidden_roots": ["output"],
        "repo_facing_navigation_docs": ["README.md"],
    }

    report = module.render_check_report("C:/repo", config, [{"kind": "example"}])

    assert "obsidian-this check: audited repo C:/repo" in report
    assert "- findings: 1" in report


def test_render_fix_report_contains_touched_files():
    module = load_module()
    report = module.render_fix_report("C:/repo", ["docs/seo/topic.md"], [{"kind": "x"}])

    assert "obsidian-this fix: updated repo C:/repo" in report
    assert "- touched files: 1" in report
    assert "- touched: docs/seo/topic.md" in report
