from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import scope


WIKILINK_HIDDEN_RE = re.compile(r"\[\[(\.agents/[^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TAG_LINE_RE = re.compile(r"^#[A-Za-z0-9_-]+(?:\s+#[A-Za-z0-9_-]+)*$")
CODE_MD_RE = re.compile(r"`([^`\n]+?\.md)`")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _relative(path: Path, repo: Path) -> str:
    return str(path.relative_to(repo)).replace("\\", "/")


def _apply_missing_upward_link(text: str, expected: str) -> str:
    addition = f"\n## Related Docs\n\n- [[{expected}]]\n"
    if "## Related Docs" in text:
        if f"[[{expected}]]" not in text:
            return text.rstrip() + f"\n- [[{expected}]]\n"
        return text
    return text.rstrip() + addition


def _move_tag_below_h1(text: str) -> str:
    lines = text.splitlines()
    h1_index = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if h1_index is None:
        return text

    tag_index = next((i for i, line in enumerate(lines) if TAG_LINE_RE.match(line.strip())), None)
    if tag_index is None or tag_index == h1_index + 1:
        return text

    tag_line = lines.pop(tag_index)
    if tag_index < h1_index:
        h1_index -= 1
    lines.insert(h1_index + 1, tag_line)
    return "\n".join(lines).rstrip() + "\n"


def _replace_plain_md_paths_with_wikilinks(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        target = match.group(1).replace("\\", "/")
        if target.startswith(".agents/"):
            return match.group(0)
        if target.endswith(".md"):
            target = target[:-3]
        return f"[[{target}]]"

    return CODE_MD_RE.sub(repl, text)


def apply_fixes(repo: Path, config: dict, findings: list[dict]) -> list[str]:
    grouped: dict[str, list[dict]] = {}
    for finding in findings:
        grouped.setdefault(finding["path"], []).append(finding)

    touched: list[str] = []
    for rel_path, file_findings in grouped.items():
        classification = scope.classify_path(rel_path, config)
        file_path = repo / rel_path
        text = _read(file_path)
        original = text

        if classification == scope.GRAPH_FIXABLE or scope.is_repo_facing_navigation_doc(rel_path, config):
            for finding in file_findings:
                if finding["kind"] == "missing_upward_link":
                    text = _apply_missing_upward_link(text, finding["expected"])
                elif finding["kind"] == "hidden_fake_click_target":
                    text = WIKILINK_HIDDEN_RE.sub(r"`\1`", text)
                elif finding["kind"] == "tag_placement_mismatch":
                    text = _move_tag_below_h1(text)
                elif finding["kind"] == "visible_note_plain_path":
                    text = _replace_plain_md_paths_with_wikilinks(text)

        elif classification == scope.REPORT_ONLY and file_path.name == "SKILL.md":
            bottom_tag = config.get("skill_note_rules", {}).get("bottom_only_tag", "#skills")
            if bottom_tag not in text.splitlines()[-3:]:
                text = text.rstrip() + f"\n\n{bottom_tag}\n"

        if text != original:
            _write(file_path, text)
            touched.append(rel_path)

    return sorted(touched)
