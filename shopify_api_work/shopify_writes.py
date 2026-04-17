from __future__ import annotations

import json
import time


def list_publications(gql, endpoint: str, token: str) -> list[dict]:
    q = """query($first:Int!, $after:String){
  publications(first:$first, after:$after) {
    pageInfo { hasNextPage endCursor }
    nodes { id name }
  }
}""".strip()
    after = None
    out: list[dict] = []
    while True:
        res = gql(endpoint, token, q, {"first": 100, "after": after})
        if res.get("errors"):
            raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
        conn = res["data"]["publications"]
        out.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
        time.sleep(0.05)
    return out


def publishable_publish(gql, endpoint: str, token: str, publishable_id: str, publication_ids: list[str]) -> dict:
    q = """mutation($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    userErrors { field message }
    publishable { __typename }
  }
}""".strip()
    input_obj = [{"publicationId": pid} for pid in publication_ids]
    res = gql(endpoint, token, q, {"id": publishable_id, "input": input_obj})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    payload = res["data"]["publishablePublish"]
    errs = payload.get("userErrors") or []
    if errs:
        raise SystemExit("UserErrors: " + json.dumps(errs, ensure_ascii=False))
    return payload


def collection_update(gql, endpoint: str, token: str, input_obj: dict) -> dict:
    q = """mutation($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection { id handle title sortOrder ruleSet { appliedDisjunctively } }
    userErrors { field message }
  }
}""".strip()
    res = gql(endpoint, token, q, {"input": input_obj})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    payload = res["data"]["collectionUpdate"]
    if payload.get("userErrors"):
        raise SystemExit("UserErrors: " + json.dumps(payload["userErrors"], ensure_ascii=False))
    return payload["collection"]


def collection_create(gql, endpoint: str, token: str, input_obj: dict) -> dict:
    q = """mutation($input: CollectionInput!) {
  collectionCreate(input: $input) {
    collection { id handle title sortOrder ruleSet { appliedDisjunctively } }
    userErrors { field message }
  }
}""".strip()
    res = gql(endpoint, token, q, {"input": input_obj})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    payload = res["data"]["collectionCreate"]
    if payload.get("userErrors"):
        raise SystemExit("UserErrors: " + json.dumps(payload["userErrors"], ensure_ascii=False))
    return payload["collection"]


def tags_add(gql, endpoint: str, token: str, id_: str, tags: list[str]) -> dict:
    q = """mutation($id: ID!, $tags: [String!]!) {
  tagsAdd(id: $id, tags: $tags) {
    userErrors { field message }
  }
}""".strip()
    res = gql(endpoint, token, q, {"id": id_, "tags": tags})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    payload = res["data"]["tagsAdd"]
    errs = payload.get("userErrors") or []
    if errs:
        raise SystemExit("UserErrors: " + json.dumps(errs, ensure_ascii=False))
    return payload


def find_url_redirect(gql, endpoint: str, token: str, path: str) -> dict | None:
    q = """query($first:Int!, $query:String!) {
  urlRedirects(first:$first, query:$query) {
    nodes { id path target }
  }
}""".strip()
    query = f"path:{path}"
    res = gql(endpoint, token, q, {"first": 10, "query": query})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    nodes = (res.get("data") or {}).get("urlRedirects", {}).get("nodes") or []
    for n in nodes:
        if (n.get("path") or "").strip() == path.strip():
            return n
    return None


def url_redirect_create(gql, endpoint: str, token: str, path: str, target: str) -> dict:
    q = """mutation($urlRedirect: UrlRedirectInput!) {
  urlRedirectCreate(urlRedirect: $urlRedirect) {
    urlRedirect { id path target }
    userErrors { field message }
  }
}""".strip()
    res = gql(endpoint, token, q, {"urlRedirect": {"path": path, "target": target}})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    payload = res["data"]["urlRedirectCreate"]
    errs = payload.get("userErrors") or []
    if errs:
        raise SystemExit("UserErrors: " + json.dumps(errs, ensure_ascii=False))
    return payload["urlRedirect"]


def ensure_url_redirect(gql, endpoint: str, token: str, path: str, target: str) -> dict:
    existing = find_url_redirect(gql, endpoint, token, path)
    if existing:
        return {"status": "exists", "urlRedirect": existing}
    created = url_redirect_create(gql, endpoint, token, path, target)
    return {"status": "created", "urlRedirect": created}

