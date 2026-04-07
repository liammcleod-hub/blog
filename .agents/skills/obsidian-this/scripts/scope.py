from __future__ import annotations

from pathlib import Path


GRAPH_FIXABLE = "graph_fixable"
REPORT_ONLY = "report_only"
FORBIDDEN = "forbidden"
NORMALIZATION_CANDIDATE = "normalization_candidate"
OUT_OF_SCOPE = "out_of_scope"


def _normalize(path: Path | str) -> str:
    return str(path).replace("\\", "/").strip("/")


def _is_within(path: str, roots: list[str]) -> bool:
    return any(path == root.strip("/") or path.startswith(root.strip("/") + "/") for root in roots)


def classify_path(path: Path | str, config: dict) -> str:
    normalized = _normalize(path)

    if _is_within(normalized, config.get("forbidden_roots", [])):
        return FORBIDDEN

    skill_roots = config.get("skill_note_rules", {}).get("roots", [])
    if _is_within(normalized, skill_roots):
        return REPORT_ONLY

    if normalized in config.get("normalization_candidates", []):
        return NORMALIZATION_CANDIDATE

    if _is_within(normalized, config.get("graph_roots", [])):
        return GRAPH_FIXABLE

    return OUT_OF_SCOPE


def is_repo_facing_navigation_doc(path: Path | str, config: dict) -> bool:
    return _normalize(path) in {
        item.strip("/") for item in config.get("repo_facing_navigation_docs", [])
    }


def note_can_receive_top_tag(path: Path | str, config: dict, has_h1: bool) -> bool:
    if not has_h1:
        return False
    return classify_path(path, config) == GRAPH_FIXABLE
