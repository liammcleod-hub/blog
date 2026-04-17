import json
import pathlib

from collections_cleanup_impl import DEFAULT_ENV_PATH, list_collections, shopify_cfg


def main() -> None:
    try:
        import sys

        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    rows = list_collections(endpoint, token)
    for c in sorted(rows, key=lambda x: (x.get("title") or "", x.get("handle") or "")):
        kind = "SMART" if c.get("ruleSet") else "MANUAL"
        count = (c.get("productsCount") or {}).get("count", 0)
        print(f"{kind}\t{count}\t{c['title']}\t{c['handle']}\t{c['id']}")


if __name__ == "__main__":
    main()
