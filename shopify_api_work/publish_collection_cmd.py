import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_ENV_PATH, inspect_collection, list_publications, publishable_publish, shopify_cfg


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python publish_collection_cmd.py <handle> [--publication-name \"Online Store\"]")
    handle = sys.argv[1]
    publication_name = "Online Store"
    if "--publication-name" in sys.argv:
        i = sys.argv.index("--publication-name")
        if i + 1 < len(sys.argv):
            publication_name = sys.argv[i + 1]

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    coll = inspect_collection(endpoint, token, handle)
    pubs = list_publications(endpoint, token)
    target = None
    for p in pubs:
        if (p.get("name") or "").strip().lower() == (publication_name or "").strip().lower():
            target = p
            break
    if not target:
        raise SystemExit(
            f"Publication not found by name: {publication_name}. Available: "
            + ", ".join(sorted({p.get('name') or '' for p in pubs if p.get('name')}))
        )
    payload = publishable_publish(endpoint, token, coll["id"], [target["id"]])
    print(json.dumps({"handle": handle, "publication": target, "result": payload}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
