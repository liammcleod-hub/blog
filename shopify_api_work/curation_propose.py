import json
import pathlib
import time

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    DEFAULT_MENU_ID,
    OUT_DIR,
    fetch_menu_collections,
    infer_curated_candidates,
    inspect_collection,
    load_config,
    shopify_cfg,
)


def main() -> None:
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    menu_id = cfg.get("menu_id") or DEFAULT_MENU_ID
    menu_handles = fetch_menu_collections(endpoint, token, menu_id)

    collections_by_handle: dict[str, dict] = {}
    for m in menu_handles:
        c = inspect_collection(endpoint, token, m["handle"])
        collections_by_handle[m["handle"]] = c

    suggestions = infer_curated_candidates(menu_handles, collections_by_handle)
    ts = time.strftime("%Y%m%d-%H%M%S")
    report_path = OUT_DIR / f"curation_report_{ts}.md"
    approval_path = OUT_DIR / f"curation_approval_{ts}.json"

    lines = ["# Curation Inference (MAIN menu only)", "", "## Next Step (Approval Gate)"]
    lines.append(f"Edit and mark decisions in: `{approval_path}`")
    lines.append('Use `"decision": "never_touch"` or `"decision": "curated"` or `"decision": "taxonomy"`.')
    lines.append("")
    for s in suggestions:
        lines.append(f"- [{s['proposed']}] {s['title']} (`{s['handle']}`) reasons={', '.join(s['reasons'])}")
    report_path.write_text("\n".join(lines), encoding="utf-8")

    approval_items = []
    for s in suggestions:
        approval_items.append(
            {
                "handle": s["handle"],
                "title": s["title"],
                "proposed": s["proposed"],
                "decision": "",
                "reasons": s["reasons"],
            }
        )
    approval_path.write_text(json.dumps({"generated_at": ts, "menu_id": menu_id, "items": approval_items}, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"handoff_required": True, "report_path": str(report_path), "approval_path": str(approval_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
