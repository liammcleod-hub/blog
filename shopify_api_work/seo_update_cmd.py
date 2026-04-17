import json
import pathlib
import sys

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    DEFAULT_MENU_ID,
    collection_update,
    ensure_url_redirect,
    fetch_menu_full,
    inspect_collection,
    load_config,
    menu_update,
    rewrite_menu_items_url_handle,
    shopify_cfg,
)


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # Keep argument parsing minimal: core CLI enforces required args already.
    if len(sys.argv) < 5:
        raise SystemExit("Usage: python seo_update_cmd.py <handle> <seo_title> <seo_description> <description_html_file> [--new-handle H] [--update-menu]")

    handle = sys.argv[1]
    seo_title = sys.argv[2]
    seo_description = sys.argv[3]
    description_html_file = sys.argv[4]
    new_handle = None
    update_menu = "--update-menu" in sys.argv[5:]
    if "--new-handle" in sys.argv:
        i = sys.argv.index("--new-handle")
        if i + 1 < len(sys.argv):
            new_handle = sys.argv[i + 1]

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))

    coll = inspect_collection(endpoint, token, handle)
    old_handle = coll["handle"]
    final_handle = new_handle or old_handle
    desc_html = pathlib.Path(description_html_file).read_text(encoding="utf-8")

    updated = collection_update(
        endpoint,
        token,
        {
            "id": coll["id"],
            "handle": final_handle,
            "descriptionHtml": desc_html,
            "seo": {"title": seo_title, "description": seo_description},
        },
    )

    out = {"handle_before": old_handle, "handle_after": updated["handle"], "collection": updated}
    if old_handle != final_handle:
        out["redirects"] = [
            ensure_url_redirect(endpoint, token, f"/collections/{old_handle}", f"/collections/{final_handle}"),
            ensure_url_redirect(endpoint, token, f"/en/collections/{old_handle}", f"/en/collections/{final_handle}"),
        ]
    if update_menu and old_handle != final_handle:
        menu_id = cfg.get("menu_id") or DEFAULT_MENU_ID
        menu = fetch_menu_full(endpoint, token, menu_id)
        new_items, rewritten = rewrite_menu_items_url_handle(menu.get("items") or [], old_handle, final_handle)
        menu["items"] = new_items
        menu_update(endpoint, token, menu)
        out["menu_url_rewritten"] = rewritten

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
