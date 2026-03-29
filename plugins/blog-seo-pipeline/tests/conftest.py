from __future__ import annotations

import sys
from pathlib import Path
import shutil

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))


@pytest.fixture
def tmp_path() -> Path:
    base = PLUGIN_ROOT / "tests" / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    target = base / "run"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir()
    yield target
    if target.exists():
        shutil.rmtree(target)
