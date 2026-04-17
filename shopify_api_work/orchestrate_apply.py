import json
import pathlib
import sys

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    BASE_DIR,
    _orchestrate_apply,
    load_config,
    shopify_cfg,
    _run_local_script,
)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python orchestrate_apply.py <approval_file>")
    approval_file = pathlib.Path(sys.argv[1])

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))

    res = _orchestrate_apply(endpoint, token, cfg, approval_file, yes=True)
    print(json.dumps(res, ensure_ascii=False, indent=2))

    # Dependencies: after apply we regenerate snapshots/audit (n+1 depends on successful apply).
    _run_local_script(BASE_DIR / "pull_menu_MAIN_collections_products.py")
    _run_local_script(BASE_DIR / "generate_menu_MAIN_kiss_audit.py")


if __name__ == "__main__":
    main()
