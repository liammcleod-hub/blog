import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_ENV_PATH, explain_matches, fetch_collection_products, inspect_collection, shopify_cfg


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python explain_collection_cmd.py <handle>")
    handle = sys.argv[1]
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    coll = inspect_collection(endpoint, token, handle)
    products = fetch_collection_products(endpoint, token, handle)
    explained = explain_matches(coll.get("ruleSet"), products)
    print(json.dumps({"collection": {"id": coll["id"], "handle": coll["handle"], "title": coll["title"]}, "products": explained}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
