import json
import pathlib

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    OUT_DIR,
    _orchestrate_build_proposals,
    _write_orchestrate_files,
    load_config,
    shopify_cfg,
)


def main() -> None:
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    bundle = _orchestrate_build_proposals(endpoint, token, cfg)
    files = _write_orchestrate_files(bundle)
    print(json.dumps({"handoff_required": True, **files}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
