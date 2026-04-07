from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CHECKS_PATH = SKILL_ROOT / "scripts" / "checks.py"
FIX_PATH = SKILL_ROOT / "scripts" / "fix_engine.py"
FIXTURE_REPO = SKILL_ROOT / "tests" / "fixtures" / "generic-repo"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
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


def test_fix_engine_applies_only_deterministic_changes():
    repo = Path(r"C:\Users\Hp\.codex\memories\obsidian-this-test-repo")
    if repo.exists():
        shutil.rmtree(repo)
    shutil.copytree(FIXTURE_REPO, repo)

    checks = load_module(CHECKS_PATH, "checks")
    fix_engine = load_module(FIX_PATH, "fix_engine")
    config = sample_config()
    findings = checks.run_checks(repo, config)
    touched = fix_engine.apply_fixes(repo, config, findings)

    assert "README.md" in touched
    assert "docs/reference/guide.md" in touched
    assert "repo-skills/marketing-library/skills/paid-ads/SKILL.md" in touched

    readme_text = (repo / "README.md").read_text(encoding="utf-8")
    assert "[[docs/reference/README]]" in readme_text

    guide_text = (repo / "docs/reference/guide.md").read_text(encoding="utf-8")
    assert "`.agents/private-context.md`" in guide_text

    skill_text = (repo / "repo-skills/marketing-library/skills/paid-ads/SKILL.md").read_text(encoding="utf-8")
    assert skill_text.rstrip().endswith("#skills")

    article_text = (repo / "output/generated/article.html").read_text(encoding="utf-8")
    assert "<html>" in article_text
