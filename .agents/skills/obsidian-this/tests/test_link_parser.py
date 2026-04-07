from __future__ import annotations

import importlib.util
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "link_parser.py"


def load_module():
    spec = importlib.util.spec_from_file_location("link_parser", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_wikilinks_and_code_paths():
    module = load_module()
    text = "See [[docs/seo/README]] and `docs/reference/README.md` and [[.agents/private-context.md]]."

    assert module.parse_wikilinks(text) == ["docs/seo/README", ".agents/private-context.md"]
    assert module.parse_code_paths(text) == ["docs/reference/README.md"]


def test_h1_and_tag_helpers():
    module = load_module()
    lines = ["# Title", "#seo", "", "Body"]

    assert module.first_h1_line_index(lines) == 0
    assert module.standalone_tag_line_indices(lines) == [1]
