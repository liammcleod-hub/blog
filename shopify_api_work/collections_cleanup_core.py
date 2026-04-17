"""
Collections cleanup CLI dispatcher.

This file intentionally stays small. All implementation details live in
`collections_cleanup_impl.py` and single-purpose command scripts in this folder.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

from collections_cleanup_impl import BASE_DIR


def _run_local_script(script_path: pathlib.Path) -> None:
    subprocess.check_call([sys.executable, str(script_path)])


def _run_local_script_args(script_path: pathlib.Path, extra_args: list[str]) -> None:
    try:
        subprocess.check_call([sys.executable, str(script_path), *extra_args])
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode)


def main() -> None:
    # Defer to the full CLI in the implementation module.
    # Keeping this indirection allows the runner to import `collections_cleanup_core.main`
    # while we keep this file lightweight.
    from collections_cleanup_impl import main as _impl_main

    _impl_main()


if __name__ == "__main__":
    main()

