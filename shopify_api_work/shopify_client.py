import json
import pathlib
import ssl
import time
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


def gql(endpoint_url: str, token: str, query: str, variables: dict | None = None) -> dict:
    payload = {"query": query, "variables": variables or {}}
    req = urllib.request.Request(
        endpoint_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        method="POST",
    )
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def shopify_cfg(env_path: pathlib.Path) -> tuple[str, str]:
    env = load_env(env_path)
    shop = env.get("SHOPIFY_STORE_URL") or env.get("SHOPIFY_SHOP_DOMAIN")
    if not shop:
        raise SystemExit("Missing SHOPIFY_STORE_URL (or SHOPIFY_SHOP_DOMAIN) in env.")
    ver = env.get("SHOPIFY_API_VERSION") or "2026-01"
    token = env.get("SHOPIFY_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Missing SHOPIFY_ACCESS_TOKEN in env.")
    endpoint = f"https://{shop}/admin/api/{ver}/graphql.json"
    return endpoint, token


def load_config(path: pathlib.Path, default_menu_id: str) -> dict:
    if not path.exists():
        return {
            "menu_id": default_menu_id,
            "curated_handles": [],
            "never_touch_handles": [],
            "never_touch_title_keywords": [],
            "rules_overrides": {},
            "manual_to_smart_overrides": {},
        }
    # PowerShell's Set-Content may introduce a UTF-8 BOM; tolerate it.
    return json.loads(path.read_text(encoding="utf-8-sig"))


def list_collections(endpoint: str, token: str) -> list[dict]:
    q = """query($first:Int!, $after:String){
  collections(first:$first, after:$after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      handle
      title
      sortOrder
      productsCount { count }
      ruleSet { appliedDisjunctively }
    }
  }
}""".strip()
    after = None
    out: list[dict] = []
    while True:
        res = gql(endpoint, token, q, {"first": 250, "after": after})
        if res.get("errors"):
            raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
        conn = res["data"]["collections"]
        out.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
        time.sleep(0.05)
    return out


def inspect_collection(endpoint: str, token: str, handle: str) -> dict:
    q = """query($handle:String!){
  collectionByHandle(handle:$handle){
    id
    title
    handle
    sortOrder
    productsCount { count }
    ruleSet {
      appliedDisjunctively
      rules { column relation condition }
    }
  }
}""".strip()
    res = gql(endpoint, token, q, {"handle": handle})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    coll = (res.get("data") or {}).get("collectionByHandle")
    if not coll:
        raise SystemExit(f"Collection not found by handle: {handle}")
    return coll


def inspect_collection_by_id(endpoint: str, token: str, collection_id: str) -> dict:
    q = """query($id:ID!){
  node(id:$id){
    __typename
    ... on Collection {
      id
      title
      handle
      sortOrder
      productsCount { count }
      ruleSet {
        appliedDisjunctively
        rules { column relation condition }
      }
    }
  }
}""".strip()
    res = gql(endpoint, token, q, {"id": collection_id})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    node = (res.get("data") or {}).get("node") or {}
    if node.get("__typename") != "Collection":
        raise SystemExit(f"Collection not found by id: {collection_id}")
    return node


def fetch_collection_products(endpoint: str, token: str, handle: str) -> list[dict]:
    q = """query($handle:String!, $first:Int!, $after:String){
  collectionByHandle(handle:$handle){
    id
    handle
    products(first:$first, after:$after){
      pageInfo { hasNextPage endCursor }
      nodes {
        id
        title
        handle
        vendor
        productType
        status
        tags
      }
    }
  }
}""".strip()
    after = None
    out: list[dict] = []
    while True:
        res = gql(endpoint, token, q, {"handle": handle, "first": 250, "after": after})
        if res.get("errors"):
            raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
        coll = (res.get("data") or {}).get("collectionByHandle")
        if not coll:
            raise SystemExit(f"Collection not found by handle: {handle}")
        conn = coll["products"]
        out.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
        time.sleep(0.05)
    return out


def fetch_collection_products_by_id(endpoint: str, token: str, collection_id: str) -> list[dict]:
    q = """query($id:ID!, $first:Int!, $after:String){
  node(id:$id){
    __typename
    ... on Collection {
      id
      handle
      products(first:$first, after:$after){
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          title
          handle
          vendor
          productType
          status
          tags
        }
      }
    }
  }
}""".strip()
    after = None
    out: list[dict] = []
    while True:
        res = gql(endpoint, token, q, {"id": collection_id, "first": 250, "after": after})
        if res.get("errors"):
            raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
        node = (res.get("data") or {}).get("node") or {}
        if node.get("__typename") != "Collection":
            raise SystemExit(f"Collection not found by id: {collection_id}")
        conn = node["products"]
        out.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
        time.sleep(0.05)
    return out
