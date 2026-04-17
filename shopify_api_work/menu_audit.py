import json
import pathlib

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    DEFAULT_MENU_ID,
    OUT_DIR,
    fetch_menu_collections,
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
    curated = set(cfg.get("curated_handles") or [])

    questions: list[dict] = []
    for m in menu_handles:
        handle = m["handle"]
        coll = inspect_collection(endpoint, token, handle)
        kind = "SMART" if coll.get("ruleSet") else "MANUAL"
        count = (coll.get("productsCount") or {}).get("count", 0)

        if kind == "MANUAL" and handle not in curated:
            questions.append(
                {
                    "handle": handle,
                    "title": coll["title"],
                    "kind": kind,
                    "products": count,
                    "question": "This is MANUAL but appears in MAIN menu. Should it stay curated/manual, or be converted to SMART taxonomy?",
                }
            )
        if kind == "SMART":
            rs = coll.get("ruleSet") or {}
            if count == 0 and rs.get("appliedDisjunctively") is False:
                questions.append(
                    {
                        "handle": handle,
                        "title": coll["title"],
                        "kind": kind,
                        "products": count,
                        "question": "Smart collection is empty with AND logic. Likely should be OR logic (appliedDisjunctively=true).",
                    }
                )

    out_json = OUT_DIR / "menu_audit_questions.json"
    out_md = OUT_DIR / "menu_audit_questions.md"
    out_json.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = ["# MAIN menu audit — questions", ""]
    md_lines.append(f"- Menu collections: {len(menu_handles)}")
    md_lines.append(f"- Questions: {len(questions)}")
    md_lines.append("")
    for q in questions:
        md_lines.append(f"## {q['title']} (`{q['handle']}`)")
        md_lines.append(f"- Kind: {q['kind']}")
        md_lines.append(f"- Products: {q['products']}")
        md_lines.append(f"- Question: {q['question']}")
        md_lines.append("")
    out_md.write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")

    print(str(out_json))
    print(str(out_md))


if __name__ == "__main__":
    main()
