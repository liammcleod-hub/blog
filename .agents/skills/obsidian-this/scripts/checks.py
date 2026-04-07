from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import link_parser
import scope


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _relative(path: Path, repo: Path) -> str:
    return str(path.relative_to(repo)).replace("\\", "/")


def _expected_readme_link(rel_path: str) -> str | None:
    parts = rel_path.split("/")
    if len(parts) < 2:
        return None
    if parts[-1] == "README.md":
        return None
    return "/".join(parts[:-1] + ["README"])


def run_checks(repo: Path, config: dict) -> list[dict]:
    findings: list[dict] = []
    for path in repo.rglob("*.md"):
        rel = _relative(path, repo)
        classification = scope.classify_path(rel, config)
        text = _read_text(path)
        lines = text.splitlines()
        wikilinks = link_parser.parse_wikilinks(text)
        code_paths = link_parser.parse_code_paths(text)
        h1_index = link_parser.first_h1_line_index(lines)
        tag_indices = link_parser.standalone_tag_line_indices(lines)

        if classification == scope.GRAPH_FIXABLE:
            expected_readme = _expected_readme_link(rel)
            readme_path = path.parent / "README.md"
            if expected_readme and readme_path.exists() and expected_readme not in wikilinks:
                findings.append(
                    {
                        "kind": "missing_upward_link",
                        "path": rel,
                        "expected": expected_readme,
                    }
                )

            if h1_index is None and tag_indices:
                findings.append({"kind": "titleless_tag_ambiguity", "path": rel})
            elif tag_indices and h1_index is not None:
                if h1_index + 1 not in tag_indices:
                    findings.append({"kind": "tag_placement_mismatch", "path": rel})

        if scope.is_repo_facing_navigation_doc(rel, config):
            for code_path in code_paths:
                if code_path.endswith(".md") and not code_path.startswith(".agents/"):
                    findings.append(
                        {
                            "kind": "visible_note_plain_path",
                            "path": rel,
                            "target": code_path,
                        }
                    )

        for target in wikilinks:
            if target.startswith(".agents/"):
                findings.append(
                    {
                        "kind": "hidden_fake_click_target",
                        "path": rel,
                        "target": target,
                    }
                )

        if classification == scope.REPORT_ONLY and path.name == "SKILL.md":
            bottom_tag = config.get("skill_note_rules", {}).get("bottom_only_tag", "#skills")
            if bottom_tag not in [line.strip() for line in lines[-3:]]:
                findings.append(
                    {
                        "kind": "missing_bottom_skill_tag",
                        "path": rel,
                        "expected": bottom_tag,
                    }
                )

    return findings
