import json
import pathlib
import ssl
import sys
import time
import urllib.parse
import urllib.request

# Ensure repo root is importable when running this script directly.
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Code.shopify_api_work.audit_main_menu_collections import (
    fetch_collection_products,
    filter_products_by_tag,
    load_shopify_config,
    parse_collection_handle_and_tag,
    resolve_canonical_collection_path,
    summarize_collection,
)


def shopify_admin_graphql(cfg, query: str, variables: dict | None = None) -> dict:
    url = f"https://{cfg.shop_domain}/admin/api/{cfg.api_version}/graphql.json"
    payload = {"query": query, "variables": variables or {}}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": cfg.access_token,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize_menu_url_to_href(url: str) -> str | None:
    path = urllib.parse.urlparse(url).path
    if not path:
        return None
    parts = [p for p in path.split("/") if p]
    if parts and len(parts[0]) == 2:
        path = "/" + "/".join(parts[1:])
    if not path.startswith("/collections/"):
        return None
    return path


def flatten_menu_items(items):
    for it in items or []:
        yield it
        for child in flatten_menu_items(it.get("items") or []):
            yield child


def main():
    base_dir = pathlib.Path(__file__).resolve().parent
    cfg = load_shopify_config(str(base_dir / ".env"))
    storefront_url = f"https://{cfg.shop_domain}/"

    menu_id = "gid://shopify/Menu/320750813522"  # MAIN (handle: main)
    menu_query = """query($id: ID!) {
  menu(id: $id) {
    id
    handle
    title
    items {
      id
      title
      url
      type
      items {
        id
        title
        url
        type
        items {
          id
          title
          url
          type
        }
      }
    }
  }
}""".strip()
    res = shopify_admin_graphql(cfg, menu_query, {"id": menu_id})
    if res.get("errors"):
        raise SystemExit(json.dumps(res, ensure_ascii=False, indent=2))
    menu = res["data"]["menu"]

    collection_links = []
    seen_href = set()
    for item in flatten_menu_items(menu.get("items")):
        if item.get("type") != "COLLECTION":
            continue
        href = normalize_menu_url_to_href(item.get("url") or "")
        if not href or href in seen_href:
            continue
        seen_href.add(href)
        collection_links.append({"href": href, "label": item.get("title") or ""})

    parsed = []
    handles = set()
    for link in collection_links:
        href = link["href"]
        handle, requested_tag = parse_collection_handle_and_tag(href)
        effective_href = href
        effective_tag = requested_tag
        if requested_tag is not None:
            canonical_path = resolve_canonical_collection_path(storefront_url, href)
            if canonical_path and canonical_path != urllib.parse.urlparse(href).path:
                effective_href = canonical_path
                handle, _ = parse_collection_handle_and_tag(canonical_path)
                effective_tag = None

        parsed.append(
            {
                "href": effective_href,
                "href_original": href,
                "label": link["label"],
                "collection_handle": handle,
                "tag_filter_requested": requested_tag,
                "tag_filter_effective": effective_tag,
            }
        )
        handles.add(handle)

    collections_by_handle = {}
    for idx, handle in enumerate(sorted(handles), start=1):
        collections_by_handle[handle] = fetch_collection_products(cfg, handle)
        if idx % 5 == 0:
            time.sleep(0.2)

    menu_items = []
    for it in parsed:
        coll = collections_by_handle.get(it["collection_handle"]) or {
            "handle": it["collection_handle"],
            "missing": True,
        }
        products = coll.get("products") or []
        if it.get("tag_filter_effective"):
            products = filter_products_by_tag(products, it["tag_filter_effective"])
        menu_items.append(
            {
                **it,
                "collection_title": coll.get("title"),
                "collection_id": coll.get("id"),
                "collection_missing": bool(coll.get("missing")),
                "collection_error": coll.get("error"),
                "products": products,
                "summary": summarize_collection(products),
            }
        )

    output = {
        "storefront_url": storefront_url,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_menu": {"id": menu_id, "handle": menu.get("handle"), "title": menu.get("title")},
        "menu_collection_links_count": len(collection_links),
        "distinct_collection_handles_count": len(handles),
        "menu_items": menu_items,
    }

    out_dir = base_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "menu_MAIN_collections_products.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = out_dir / "menu_MAIN_collections_products.md"
    lines = []
    lines.append("# MENU=MAIN collections + products\n")
    lines.append(f"- Storefront: {storefront_url}")
    lines.append(f"- Menu: {menu.get('title')} (handle `{menu.get('handle')}`)")
    lines.append(f"- Generated: {output['generated_at']}")
    lines.append(f"- Collection links in menu: {output['menu_collection_links_count']}")
    lines.append("")

    for e in menu_items:
        title = e.get("collection_title") or e["collection_handle"]
        lines.append(f"## {e.get('label') or ''}  ({e.get('href_original')})")
        if e.get("href") != e.get("href_original"):
            lines.append(f"- Canonical/effective: `{e.get('href')}`")
        lines.append(f"- Collection: `{title}` (`{e['collection_handle']}`)")
        if e.get("tag_filter_requested"):
            lines.append(f"- Tag requested: `{e.get('tag_filter_requested')}`")
        if e.get("tag_filter_effective"):
            lines.append(f"- Tag effective: `{e.get('tag_filter_effective')}`")
        lines.append(f"- Products: {e['summary']['product_count']}")
        preview = e.get("products") or []
        for p in preview[:25]:
            lines.append(
                f"  - {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
            )
        if len(preview) > 25:
            lines.append(f"  - … and {len(preview) - 25} more")
        lines.append("")

    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(str(json_path))
    print(str(md_path))


if __name__ == "__main__":
    main()
