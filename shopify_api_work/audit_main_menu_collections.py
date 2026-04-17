import json
import pathlib
import ssl
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
import re


@dataclass(frozen=True)
class ShopifyConfig:
    shop_domain: str
    api_version: str
    access_token: str


def load_env_file(path: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def load_shopify_config(env_path: str) -> ShopifyConfig:
    env = load_env_file(env_path)
    shop_domain = env.get("SHOPIFY_STORE_URL") or env.get("SHOPIFY_SHOP_DOMAIN")
    if not shop_domain:
        raise RuntimeError(
            "Missing SHOPIFY_STORE_URL or SHOPIFY_SHOP_DOMAIN in env file."
        )
    api_version = env.get("SHOPIFY_API_VERSION") or "2026-01"
    access_token = env.get("SHOPIFY_ACCESS_TOKEN")
    if not access_token:
        raise RuntimeError("Missing SHOPIFY_ACCESS_TOKEN in env file.")
    return ShopifyConfig(
        shop_domain=shop_domain, api_version=api_version, access_token=access_token
    )


def shopify_admin_graphql(cfg: ShopifyConfig, query: str, variables: dict | None = None):
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
    with urllib.request.urlopen(
        req, context=ssl.create_default_context(), timeout=60
    ) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_storefront_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(
        req, context=ssl.create_default_context(), timeout=60
    ) as resp:
        return resp.read().decode("utf-8", errors="replace")


class MenuDrawerCollectionLinkParser(HTMLParser):
    """
    Extract <a> links inside Dawn-like menu drawer navigation:
      <nav class="menu-drawer__navigation"> ... <a href="/collections/...">Label</a>
    """

    def __init__(self):
        super().__init__()
        self._in_target_nav = False
        self._in_a = False
        self._current_href: str | None = None
        self._current_text: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs):
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        if tag == "nav":
            class_attr = attrs_dict.get("class", "")
            if "menu-drawer__navigation" in class_attr.split():
                self._in_target_nav = True
                return
        if self._in_target_nav and tag == "a":
            href = attrs_dict.get("href")
            if href:
                self._in_a = True
                self._current_href = href
                self._current_text = []

    def handle_endtag(self, tag: str):
        if self._in_target_nav and tag == "nav":
            self._in_target_nav = False
            return
        if tag == "a" and self._in_a:
            text = " ".join("".join(self._current_text).split()).strip()
            self.links.append((self._current_href or "", text))
            self._in_a = False
            self._current_href = None
            self._current_text = []

    def handle_data(self, data: str):
        if self._in_a:
            self._current_text.append(data)


def parse_main_menu_collection_links(storefront_html: str) -> list[dict]:
    parser = MenuDrawerCollectionLinkParser()
    parser.feed(storefront_html)

    items: list[dict] = []
    seen: set[str] = set()
    for href, label in parser.links:
        if not href.startswith("/collections/"):
            continue
        if href in seen:
            continue
        seen.add(href)
        items.append({"href": href, "label": label})
    return items


def parse_collection_handle_and_tag(href: str) -> tuple[str, str | None]:
    # Examples:
    #   /collections/abc
    #   /collections/abc/tag-slug
    path = urllib.parse.urlparse(href).path
    parts = [p for p in path.split("/") if p]
    # ['collections', '<handle>', '<optional tag>']
    if len(parts) < 2 or parts[0] != "collections":
        raise ValueError(f"Not a collection href: {href}")
    handle = parts[1]
    tag = parts[2] if len(parts) >= 3 else None
    if tag:
        tag = urllib.parse.unquote(tag)
    return handle, tag


def resolve_canonical_collection_path(storefront_base_url: str, href: str) -> str | None:
    """
    For links like /collections/<handle>/<something>, Shopify sometimes canonicalizes
    to /collections/<handle> (i.e., the extra segment isn't a real tag filter).

    Returns canonical *path* (e.g. /collections/abc) when present, else None.
    """
    url = urllib.parse.urljoin(storefront_base_url, href)
    html = fetch_storefront_html(url)
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    if not m:
        return None
    canonical_url = m.group(1)
    canonical_path = urllib.parse.urlparse(canonical_url).path
    if canonical_path.startswith("/collections/"):
        return canonical_path
    return None


def fetch_collection_products(cfg: ShopifyConfig, handle: str) -> dict:
    query = """
query($handle: String!, $first: Int!, $after: String) {
  collectionByHandle(handle: $handle) {
    id
    title
    handle
    products(first: $first, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes { id title handle vendor productType status tags }
    }
  }
}
""".strip()

    after: str | None = None
    all_products: list[dict] = []
    collection_title: str | None = None
    collection_id: str | None = None

    while True:
        res = shopify_admin_graphql(
            cfg, query, {"handle": handle, "first": 250, "after": after}
        )
        if res.get("errors"):
            return {"handle": handle, "error": res["errors"]}

        coll = (res.get("data") or {}).get("collectionByHandle")
        if not coll:
            return {"handle": handle, "missing": True}

        collection_title = coll.get("title")
        collection_id = coll.get("id")

        products_conn = coll.get("products") or {}
        nodes = products_conn.get("nodes") or []
        all_products.extend(nodes)

        page_info = products_conn.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        after = page_info.get("endCursor")
        time.sleep(0.05)

    return {
        "id": collection_id,
        "title": collection_title,
        "handle": handle,
        "products": all_products,
    }


def filter_products_by_tag(products: list[dict], tag: str) -> list[dict]:
    wanted = tag.strip().lower()
    out: list[dict] = []
    for p in products:
        tags = p.get("tags") or []
        if any((t or "").strip().lower() == wanted for t in tags):
            out.append(p)
    return out


def summarize_collection(products: list[dict]) -> dict:
    by_type: dict[str, int] = {}
    by_vendor: dict[str, int] = {}
    status: dict[str, int] = {}
    for p in products:
        by_type[p.get("productType") or ""] = by_type.get(p.get("productType") or "", 0) + 1
        by_vendor[p.get("vendor") or ""] = by_vendor.get(p.get("vendor") or "", 0) + 1
        status[p.get("status") or ""] = status.get(p.get("status") or "", 0) + 1

    def top(d: dict[str, int], n: int = 10):
        return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:n]

    return {
        "product_count": len(products),
        "top_product_types": top(by_type),
        "top_vendors": top(by_vendor),
        "status_counts": top(status, n=10),
    }


def main():
    base_dir = pathlib.Path(__file__).resolve().parent
    env_path = str(base_dir / ".env")
    cfg = load_shopify_config(env_path)

    storefront_url = f"https://{cfg.shop_domain}/"
    html = fetch_storefront_html(storefront_url)
    menu_items = parse_main_menu_collection_links(html)

    # Distinct collections referenced by the menu (including tag-filter variants)
    parsed_items: list[dict] = []
    handles: set[str] = set()
    for item in menu_items:
        href = item["href"]
        handle, requested_tag = parse_collection_handle_and_tag(href)

        effective_tag = requested_tag
        effective_href = href
        if requested_tag is not None:
            canonical_path = resolve_canonical_collection_path(storefront_url, href)
            if canonical_path and canonical_path != urllib.parse.urlparse(href).path:
                effective_href = canonical_path
                handle, _ = parse_collection_handle_and_tag(canonical_path)
                effective_tag = None

        parsed_items.append(
            {
                "href": effective_href,
                "href_original": href,
                "label": item.get("label") or "",
                "collection_handle": handle,
                "tag_filter_requested": requested_tag,
                "tag_filter_effective": effective_tag,
            }
        )
        handles.add(handle)

    collections_by_handle: dict[str, dict] = {}
    handles_sorted = sorted(handles)
    for idx, handle in enumerate(handles_sorted, start=1):
        collections_by_handle[handle] = fetch_collection_products(cfg, handle)
        if idx % 5 == 0:
            time.sleep(0.2)

    # Attach per-menu-entry product list (filtered if tag filter is present)
    enriched_menu_items: list[dict] = []
    for item in parsed_items:
        coll = collections_by_handle.get(item["collection_handle"]) or {
            "handle": item["collection_handle"],
            "missing": True,
        }
        products = coll.get("products") or []
        if item.get("tag_filter_effective"):
            products = filter_products_by_tag(products, item["tag_filter_effective"])
        enriched_menu_items.append(
            {
                **item,
                "collection_title": coll.get("title"),
                "collection_id": coll.get("id"),
                "products": products,
                "summary": summarize_collection(products),
                "collection_error": coll.get("error"),
                "collection_missing": bool(coll.get("missing")),
            }
        )

    output = {
        "storefront_url": storefront_url,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "menu_collection_links_count": len(menu_items),
        "distinct_collection_handles_count": len(handles_sorted),
        "menu_items": enriched_menu_items,
    }

    out_dir = base_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "main_menu_collections_products.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = out_dir / "main_menu_collections_products.md"
    lines: list[str] = []
    lines.append(f"# Main menu collections + products\n")
    lines.append(f"- Storefront: {storefront_url}\n")
    lines.append(f"- Generated: {output['generated_at']}\n")
    lines.append(f"- Menu collection links: {output['menu_collection_links_count']}\n")
    lines.append(f"- Distinct collection handles: {output['distinct_collection_handles_count']}\n")
    lines.append("")  # blank

    for entry in enriched_menu_items:
        title = entry.get("collection_title") or entry["collection_handle"]
        label = entry.get("label") or ""
        requested_tag = entry.get("tag_filter_requested")
        effective_tag = entry.get("tag_filter_effective")
        href_original = entry.get("href_original") or entry["href"]
        href_effective = entry.get("href") or href_original
        lines.append(f"## {label}  ({href_original})")
        if href_effective != href_original:
            lines.append(f"- Canonical/effective: `{href_effective}`")
        lines.append(f"- Collection: `{title}` (`{entry['collection_handle']}`)")
        if requested_tag:
            lines.append(f"- Tag requested: `{requested_tag}`")
        if effective_tag:
            lines.append(f"- Tag effective: `{effective_tag}`")
        lines.append(f"- Products: {entry['summary']['product_count']}")
        if entry.get("collection_missing"):
            lines.append("- ERROR: collection missing")
        if entry.get("collection_error"):
            lines.append(f"- ERROR: {entry['collection_error']}")
        # quick preview list for scanning (full list stays in JSON)
        preview = entry.get("products") or []
        for p in preview[:25]:
            lines.append(f"  - {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]")
        if len(preview) > 25:
            lines.append(f"  - … and {len(preview) - 25} more")
        lines.append("")

    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(str(json_path))
    print(str(md_path))


if __name__ == "__main__":
    main()
