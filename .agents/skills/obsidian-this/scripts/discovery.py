from __future__ import annotations

from pathlib import Path


MARKDOWN_SUFFIXES = {".md"}
NON_MARKDOWN_CANDIDATE_SUFFIXES = {".txt"}
NON_MARKDOWN_EXCLUSION_SUFFIXES = {".html"}
FORBIDDEN_PATH_PARTS = {"output", "template", "templates", "fixtures"}
GRAPH_ROOT_HINTS = {"docs", "notes", "memory", "memories", "wiki", "reference"}


def _is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts if part not in {".", ".."})


def _relative_parts(path: Path, repo: Path) -> tuple[str, ...]:
    return path.relative_to(repo).parts


def _candidate_graph_root(path: Path, repo: Path) -> str | None:
    rel = path.relative_to(repo)
    parts = rel.parts
    if len(parts) < 2:
        return None
    if parts[0].lower() in GRAPH_ROOT_HINTS:
        return parts[0] if len(parts) == 2 else str(Path(parts[0]) / parts[1]).replace("\\", "/")
    return None


def discover_repo(repo: Path) -> dict:
    repo = repo.resolve()
    proposals = {
        "graph_roots": set(),
        "forbidden_roots": set(),
        "repo_facing_navigation_docs": set(),
        "skill_note_roots": set(),
        "normalization_candidates": set(),
        "normalization_exclusions": set(),
    }

    for path in repo.rglob("*"):
        if not path.is_file():
            continue
        if _is_hidden(path.relative_to(repo)):
            continue

        rel = path.relative_to(repo)
        rel_str = str(rel).replace("\\", "/")
        parts_lower = {part.lower() for part in rel.parts}
        suffix = path.suffix.lower()

        if parts_lower & FORBIDDEN_PATH_PARTS:
            proposals["forbidden_roots"].add(rel.parts[0])

        if path.name == "SKILL.md" and "repo-skills" in parts_lower:
            proposals["skill_note_roots"].add("/".join(rel.parts[:3]))

        if suffix in MARKDOWN_SUFFIXES:
            root = _candidate_graph_root(path, repo)
            if root is not None and rel.parts[0].lower() not in FORBIDDEN_PATH_PARTS:
                proposals["graph_roots"].add(root)

            if path.name == "README.md":
                proposals["repo_facing_navigation_docs"].add(rel_str)

        if suffix in NON_MARKDOWN_CANDIDATE_SUFFIXES and rel.parts[0].lower() in GRAPH_ROOT_HINTS:
            proposals["normalization_candidates"].add(rel_str)

        if suffix in NON_MARKDOWN_EXCLUSION_SUFFIXES or parts_lower & FORBIDDEN_PATH_PARTS:
            proposals["normalization_exclusions"].add(rel_str)

    return {key: sorted(value) for key, value in proposals.items()}
