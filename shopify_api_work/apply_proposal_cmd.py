import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_ENV_PATH, apply_proposal_file, shopify_cfg


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python apply_proposal_cmd.py <proposal_path> [--yes]")
    proposal_path = pathlib.Path(sys.argv[1])
    yes = "--yes" in sys.argv[2:]
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    res = apply_proposal_file(endpoint, token, proposal_path, yes=yes)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
