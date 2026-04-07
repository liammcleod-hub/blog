from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


REQUIRED_KEYS = {
    "graph_roots",
    "forbidden_roots",
    "repo_facing_navigation_docs",
    "tag_rules",
    "skill_note_rules",
    "normalization_candidates",
    "normalization_exclusions",
    "fix_permissions",
}

ALLOWED_TAG_POSITIONS = {"below_h1"}
ALLOWED_FIX_PERMISSION_KEYS = {
    "allow_link_fixes",
    "allow_tag_fixes",
    "allow_format_normalization",
}


def default_config() -> dict:
    return {
        "graph_roots": [],
        "forbidden_roots": [],
        "repo_facing_navigation_docs": [],
        "tag_rules": {
            "default_note_position": "below_h1",
            "allowed_tags": [],
            "zone_defaults": {},
        },
        "skill_note_rules": {
            "roots": [],
            "bottom_only_tag": "#skills",
        },
        "normalization_candidates": [],
        "normalization_exclusions": [],
        "fix_permissions": {
            "allow_link_fixes": True,
            "allow_tag_fixes": True,
            "allow_format_normalization": False,
        },
    }


def validate_config(config: dict) -> None:
    missing = REQUIRED_KEYS - set(config.keys())
    if missing:
        raise ValueError(f"Missing required config keys: {sorted(missing)}")

    tag_rules = config["tag_rules"]
    position = tag_rules.get("default_note_position")
    if position not in ALLOWED_TAG_POSITIONS:
        raise ValueError(
            "Invalid tag placement value: "
            f"{position!r}. Allowed: {sorted(ALLOWED_TAG_POSITIONS)}"
        )

    fix_permissions = config["fix_permissions"]
    unknown = set(fix_permissions.keys()) - ALLOWED_FIX_PERMISSION_KEYS
    if unknown:
        raise ValueError(
            "Unknown fix permission keys: "
            f"{sorted(unknown)}"
        )


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_config(data)
    return data


def save_config(path: Path, config: dict) -> None:
    validate_config(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def create_default_config() -> dict:
    return deepcopy(default_config())
