import json
import time
import pathlib

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    DEFAULT_MENU_ID,
    OUT_DIR,
    fetch_menu_collections,
    fetch_collection_products,
    inspect_collection,
    load_config,
    shopify_cfg,
    verify_congruency,
)


def main() -> None:
    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    menu_id = cfg.get("menu_id") or DEFAULT_MENU_ID
    menu_handles = fetch_menu_collections(endpoint, token, menu_id)

    curated = set(cfg.get("curated_handles") or [])
    never_touch = set(cfg.get("never_touch_handles") or [])
    exempt = set(cfg.get("verify_exempt_handles") or [])
    existing_umbrella = set(cfg.get("verify_umbrella_handles") or [])

    suggestions: list[dict] = []
    skipped: list[dict] = []

    for m in menu_handles:
        handle = m["handle"]
        if handle in exempt:
            skipped.append({"handle": handle, "reason": "verify_exempt_handles"})
            continue
        if handle in curated or handle in never_touch:
            skipped.append({"handle": handle, "reason": "curated/never_touch"})
            continue

        coll = inspect_collection(endpoint, token, handle)
        if not coll.get("ruleSet"):
            skipped.append({"handle": handle, "reason": "manual_collection"})
            continue

        products = fetch_collection_products(endpoint, token, handle)
        v = verify_congruency(coll["title"], handle, products, cfg=cfg, rule_set=coll.get("ruleSet"))
        if v.get("mode") == "umbrella(ruleSet)":
            skipped.append({"handle": handle, "reason": "already_umbrella_mode"})
            continue

        outlier_ratio = float(v.get("outlier_ratio") or 0.0)
        title_l = (coll.get("title") or "").lower()
        looks_umbrella_title = (" & " in title_l) or (" und " in title_l)

        if outlier_ratio >= 0.6 or looks_umbrella_title:
            if handle in existing_umbrella:
                skipped.append({"handle": handle, "reason": "already_in_verify_umbrella_handles"})
            else:
                suggestions.append(
                    {
                        "handle": handle,
                        "title": coll.get("title"),
                        "outlier_ratio": outlier_ratio,
                        "products": len(products),
                        "reason": "smart_high_outliers_or_umbrella_title",
                        "recommend_add_to_verify_umbrella_handles": True,
                    }
                )
        else:
            skipped.append({"handle": handle, "reason": "low_outlier_ratio"})

    suggestions.sort(key=lambda x: (-float(x.get("outlier_ratio") or 0.0), -int(x.get("products") or 0), x.get("handle") or ""))
    bundle = {"menu": {"id": menu_id, "handle": "main"}, "suggestions": suggestions, "skipped": skipped}

    ts = time.strftime("%Y%m%d-%H%M%S")
    json_path = OUT_DIR / f"umbrella_suggest_{ts}.json"
    md_path = OUT_DIR / f"umbrella_suggest_{ts}.md"
    json_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

    lines: list[str] = []
    lines.append("# Umbrella Suggest (MAIN menu only)")
    lines.append("")
    lines.append("## Suggested additions to `verify_umbrella_handles`")
    if not suggestions:
        lines.append("- (none)")
    else:
        for s in suggestions:
            lines.append(f"- {s['title']} (`{s['handle']}`) products={s['products']} outlier_ratio={s['outlier_ratio']:.4f}")
    lines.append("")
    lines.append("## Next Step")
    lines.append("- If you agree, add the suggested handles into `verify_umbrella_handles` in `collections_cleanup_config.json`.")
    lines.append("- Re-run `orchestrate --mode propose` afterwards.")
    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(json.dumps({"handoff_required": True, "json_path": str(json_path), "md_path": str(md_path), "count": len(suggestions)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
