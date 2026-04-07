from __future__ import annotations

import importlib.util
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "scope.py"


def load_module():
    spec = importlib.util.spec_from_file_location("scope", MODULE_PATH)
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


def test_scope_classifies_graph_fixable_report_only_forbidden_and_candidate():
    module = load_module()
    config = sample_config()

    assert module.classify_path("docs/seo/README.md", config) == module.GRAPH_FIXABLE
    assert (
        module.classify_path(
            "repo-skills/marketing-library/skills/paid-ads/SKILL.md", config
        )
        == module.REPORT_ONLY
    )
    assert module.classify_path("output/generated/article.md", config) == module.FORBIDDEN
    assert (
        module.classify_path("docs/reference/legacy-notes.txt", config)
        == module.NORMALIZATION_CANDIDATE
    )


def test_scope_uses_navigation_doc_config_for_link_class_boundaries():
    module = load_module()
    config = sample_config()

    assert module.is_repo_facing_navigation_doc("README.md", config) is True
    assert module.is_repo_facing_navigation_doc("docs/reference/guide.md", config) is False


def test_titleless_notes_are_not_auto_upgraded_into_taggable_notes():
    module = load_module()
    config = sample_config()

    assert module.note_can_receive_top_tag("docs/reference/README.md", config, has_h1=True) is True
    assert module.note_can_receive_top_tag("docs/reference/legacy-notes.txt", config, has_h1=False) is False
