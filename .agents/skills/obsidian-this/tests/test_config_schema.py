from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from unittest.mock import Mock

import pytest


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "config_schema.py"


def load_module():
    spec = importlib.util.spec_from_file_location("config_schema", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_default_config_has_required_keys():
    module = load_module()
    config = module.create_default_config()
    assert set(config.keys()) == module.REQUIRED_KEYS


def test_validate_rejects_missing_required_keys():
    module = load_module()
    config = module.create_default_config()
    config.pop("graph_roots")

    with pytest.raises(ValueError, match="Missing required config keys"):
        module.validate_config(config)


def test_validate_rejects_invalid_tag_position():
    module = load_module()
    config = module.create_default_config()
    config["tag_rules"]["default_note_position"] = "top_of_file"

    with pytest.raises(ValueError, match="Invalid tag placement value"):
        module.validate_config(config)


def test_validate_rejects_unknown_fix_permissions():
    module = load_module()
    config = module.create_default_config()
    config["fix_permissions"]["allow_everything"] = True

    with pytest.raises(ValueError, match="Unknown fix permission keys"):
        module.validate_config(config)


def test_save_and_load_round_trip():
    module = load_module()
    config = module.create_default_config()
    config["graph_roots"] = ["docs"]
    parent = Mock()
    path = Mock()
    path.parent = parent

    written = {}

    def write_text(payload: str, encoding: str) -> None:
        written["payload"] = payload

    def read_text(encoding: str) -> str:
        return written["payload"]

    path.write_text.side_effect = write_text
    path.read_text.side_effect = read_text

    module.save_config(path, config)
    loaded = module.load_config(path)

    assert loaded["graph_roots"] == ["docs"]
    assert loaded["skill_note_rules"]["bottom_only_tag"] == "#skills"
    parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    assert json.loads(written["payload"])["graph_roots"] == ["docs"]
