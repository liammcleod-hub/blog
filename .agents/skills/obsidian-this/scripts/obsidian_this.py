from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import config_schema
import checks
import discovery
import fix_engine
import reporting


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="obsidian-this",
        description=(
            "Portable Obsidian graph bootstrapper and maintenance entrypoint. "
            "Use 'init', 'check', or 'fix'."
        ),
    )
    parser.add_argument(
        "command",
        choices=("init", "check", "fix"),
        help="Operation to run against the target repo.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Target repo root. Defaults to the current working directory.",
    )
    return parser


def format_repo_path(repo: Path) -> str:
    try:
        return str(repo.resolve())
    except FileNotFoundError:
        return str(repo)


def handle_init(repo: Path) -> int:
    proposals = discovery.discover_repo(repo)
    config = config_schema.create_default_config()
    config["graph_roots"] = proposals["graph_roots"]
    config["forbidden_roots"] = proposals["forbidden_roots"]
    config["repo_facing_navigation_docs"] = proposals["repo_facing_navigation_docs"]
    config["skill_note_rules"]["roots"] = proposals["skill_note_roots"]
    config["normalization_candidates"] = proposals["normalization_candidates"]
    config["normalization_exclusions"] = proposals["normalization_exclusions"]
    config_path = repo / ".obsidian-this" / "config.json"
    config_schema.save_config(config_path, config)
    print(reporting.render_init_report(format_repo_path(repo), proposals))
    return 0


def handle_check(repo: Path) -> int:
    config_path = repo / ".obsidian-this" / "config.json"
    if not config_path.exists():
        print(
            "obsidian-this check: missing repo config at "
            f"{format_repo_path(config_path)}"
        )
        return 1

    config = config_schema.load_config(config_path)
    findings = checks.run_checks(repo, config)
    print(reporting.render_check_report(format_repo_path(repo), config, findings))
    return 0


def handle_fix(repo: Path) -> int:
    config_path = repo / ".obsidian-this" / "config.json"
    if not config_path.exists():
        print(
            "obsidian-this fix: missing repo config at "
            f"{format_repo_path(config_path)}"
        )
        return 1

    config = config_schema.load_config(config_path)
    findings = checks.run_checks(repo, config)
    touched = fix_engine.apply_fixes(repo, config, findings)
    print(reporting.render_fix_report(format_repo_path(repo), touched, findings))
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    repo = Path(args.repo)

    handlers = {
        "init": handle_init,
        "check": handle_check,
        "fix": handle_fix,
    }
    return handlers[args.command](repo)


if __name__ == "__main__":
    raise SystemExit(main())
