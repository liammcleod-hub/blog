import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_ENV_PATH, ensure_url_redirect, shopify_cfg


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if len(sys.argv) < 3:
        raise SystemExit("Usage: python redirect_create_cmd.py <path> <target>")
    path = sys.argv[1]
    target = sys.argv[2]

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    res = ensure_url_redirect(endpoint, token, path, target)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
