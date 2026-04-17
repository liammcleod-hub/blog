import json
import pathlib
import sys

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    load_config,
    save_config,
    shopify_cfg,
)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Missing required arg: <approval_file> [config_path]")
    approval_file = pathlib.Path(sys.argv[1])
    cfg_path = pathlib.Path(sys.argv[2]) if len(sys.argv) >= 3 else pathlib.Path(DEFAULT_CONFIG_PATH)

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    _ = (endpoint, token)  # curation apply is config-only (no Shopify writes)

    cfg = load_config(cfg_path)
    obj = json.loads(approval_file.read_text(encoding="utf-8-sig"))
    items = obj.get("items") or []

    curated = set(cfg.get("curated_handles") or [])
    never_touch = set(cfg.get("never_touch_handles") or [])

    applied: list[dict] = []
    skipped: list[dict] = []
    for it in items:
        handle = (it.get("handle") or "").strip()
        decision = (it.get("decision") or "").strip()
        if not handle or decision not in {"never_touch", "curated", "taxonomy"}:
            skipped.append({"handle": handle or None, "reason": "missing_or_invalid_decision"})
            continue

        if decision == "curated":
            curated.add(handle)
            never_touch.add(handle)
        elif decision == "never_touch":
            never_touch.add(handle)
            curated.discard(handle)
        elif decision == "taxonomy":
            curated.discard(handle)
            never_touch.discard(handle)

        applied.append({"handle": handle, "decision": decision})

    cfg["curated_handles"] = sorted(curated)
    cfg["never_touch_handles"] = sorted(never_touch)
    save_config(cfg_path, cfg)

    print(json.dumps({"applied": applied, "skipped": skipped, "config_path": str(cfg_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
