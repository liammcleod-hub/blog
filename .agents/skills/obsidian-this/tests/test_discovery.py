from __future__ import annotations

import importlib.util
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "discovery.py"
FIXTURE_REPO = SKILL_ROOT / "tests" / "fixtures" / "generic-repo"


def load_module():
    spec = importlib.util.spec_from_file_location("discovery", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_discovery_proposes_graph_roots_and_navigation_docs():
    module = load_module()
    proposals = module.discover_repo(FIXTURE_REPO)

    assert "docs/seo" in proposals["graph_roots"]
    assert "docs/reference" in proposals["graph_roots"]
    assert "README.md" in proposals["repo_facing_navigation_docs"]
    assert "docs/reference/README.md" in proposals["repo_facing_navigation_docs"]


def test_discovery_finds_skill_note_roots_and_forbidden_roots():
    module = load_module()
    proposals = module.discover_repo(FIXTURE_REPO)

    assert "repo-skills/marketing-library/skills" in proposals["skill_note_roots"]
    assert "output" in proposals["forbidden_roots"]


def test_discovery_separates_normalization_candidates_and_exclusions():
    module = load_module()
    proposals = module.discover_repo(FIXTURE_REPO)

    assert "docs/reference/legacy-notes.txt" in proposals["normalization_candidates"]
    assert "output/generated/article.html" in proposals["normalization_exclusions"]
