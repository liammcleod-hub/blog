from __future__ import annotations

import re
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
CODE_PATH_RE = re.compile(r"`([^`\n]+?\.(?:md|txt|html))`")
TAG_LINE_RE = re.compile(r"^#[A-Za-z0-9_-]+(?:\s+#[A-Za-z0-9_-]+)*$")


def parse_wikilinks(text: str) -> list[str]:
    return [match.group(1).strip() for match in WIKILINK_RE.finditer(text)]


def parse_code_paths(text: str) -> list[str]:
    return [match.group(1).strip().replace("\\", "/") for match in CODE_PATH_RE.finditer(text)]


def first_h1_line_index(lines: list[str]) -> int | None:
    for index, line in enumerate(lines):
        if line.startswith("# "):
            return index
    return None


def standalone_tag_line_indices(lines: list[str]) -> list[int]:
    return [index for index, line in enumerate(lines) if TAG_LINE_RE.match(line.strip())]


def has_h1(text: str) -> bool:
    return first_h1_line_index(text.splitlines()) is not None

