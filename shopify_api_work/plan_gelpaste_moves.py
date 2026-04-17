import json
import pathlib
import ssl
import sys
import urllib.request


def load_env(path: pathlib.Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def gql(url: str, token: str, query: str, variables: dict | None = None) -> dict:
    payload = {"query": query, "variables": variables or {}}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        method="POST",
    )
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    base_dir = pathlib.Path(__file__).resolve().parent
    env = load_env(base_dir / ".env")
    shop = env["SHOPIFY_STORE_URL"]
    ver = env.get("SHOPIFY_API_VERSION", "2026-01")
    token = env["SHOPIFY_ACCESS_TOKEN"]
    url = f"https://{shop}/admin/api/{ver}/graphql.json"

    removed_product_ids = [
        "gid://shopify/Product/10528177520978",
        "gid://shopify/Product/6665222520989",
        "gid://shopify/Product/6665424273565",
        "gid://shopify/Product/6665508847773",
        "gid://shopify/Product/6665883582621",
        "gid://shopify/Product/6987172413597",
        "gid://shopify/Product/6987207999645",
    ]

    nodes_q = """query($ids:[ID!]!){
  nodes(ids:$ids){
    __typename
    ... on Product { id title handle productType tags status }
  }
}""".strip()
    res = gql(url, token, nodes_q, {"ids": removed_product_ids})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    products = [
        n for n in (res.get("data") or {}).get("nodes") or []
        if n and n.get("__typename") == "Product"
    ]

    # Load menu dataset (post-amendment snapshot)
    menu_path = base_dir / "out" / "menu_MAIN_collections_products.json"
    menu = json.loads(menu_path.read_text(encoding="utf-8"))
    menu_items = menu.get("menu_items") or []

    repo_root = base_dir.parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    import Code.shopify_api_work.generate_menu_MAIN_kiss_audit as kiss

    # Canonical per collection handle (largest list)
    products_by_collection: dict[str, list[dict]] = {}
    title_by_collection: dict[str, str] = {}
    for e in menu_items:
        handle = e.get("collection_handle") or ""
        if not handle:
            continue
        prods = e.get("products") or []
        if handle not in products_by_collection or len(prods) > len(products_by_collection[handle]):
            products_by_collection[handle] = prods
            title_by_collection[handle] = e.get("collection_title") or handle

    tokens_by_collection: dict[str, list[str]] = {}
    for handle, title in title_by_collection.items():
        toks = kiss.tokenize(title) + kiss.tokenize(handle)
        tokens_by_collection[handle] = list(dict.fromkeys(toks))

    expected_types_by_collection: dict[str, set[str]] = {}
    for handle, prods in products_by_collection.items():
        expected_types_by_collection[handle] = {t for t, _ in kiss.top_n_product_types(prods, n=3)}

    memberships = kiss.product_memberships(menu_items)

    for p in products:
        targets = kiss.recommend_move_targets(
            p,
            current_collection_handle="gelpaste-389",
            memberships=memberships,
            title_by_collection=title_by_collection,
            expected_types_by_collection=expected_types_by_collection,
            tokens_by_collection=tokens_by_collection,
            limit=5,
        )
        pretty = [f"{title_by_collection.get(h, h)} ({h})" for h in targets]
        print(
            f"- {p['title']} (`{p['handle']}`) [{p.get('productType') or ''}]"
            + (f" -> {', '.join(pretty)}" if pretty else " -> (no strong target found)")
        )


if __name__ == "__main__":
    main()

