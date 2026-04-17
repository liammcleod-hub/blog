import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_CONFIG_PATH, DEFAULT_ENV_PATH, fetch_collection_products, inspect_collection, load_config, shopify_cfg, verify_congruency


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python verify_collection_cmd.py <handle>")
    handle = sys.argv[1]
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))
    coll = inspect_collection(endpoint, token, handle)
    products = fetch_collection_products(endpoint, token, handle)
    res = verify_congruency(coll["title"], coll["handle"], products, cfg=cfg, rule_set=coll.get("ruleSet"))
    print(json.dumps({"collection": {"id": coll["id"], "handle": coll["handle"], "title": coll["title"]}, "verification": res}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
