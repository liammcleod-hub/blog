import json
import pathlib

from collections_cleanup_impl import DEFAULT_ENV_PATH, OUT_DIR, curated_heuristic_suggestions, list_collections, shopify_cfg


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    rows = list_collections(endpoint, token)
    suggestions = curated_heuristic_suggestions(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "curated_suggestions.json"
    out_path.write_text(json.dumps(suggestions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))
    print(json.dumps(suggestions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

