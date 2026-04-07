from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "obsidian_this.py"


def load_module():
    spec = importlib.util.spec_from_file_location("obsidian_this", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_script_exists():
    assert SCRIPT_PATH.exists()


def test_parser_accepts_three_commands():
    module = load_module()
    parser = module.build_parser()
    for command in ("init", "check", "fix"):
        parsed = parser.parse_args([command])
        assert parsed.command == command


def test_cli_runs_placeholder_check():
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "obsidian-this check: missing repo config" in result.stdout
