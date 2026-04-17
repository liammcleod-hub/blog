from __future__ import annotations

import json


def fetch_menu_collections(gql, endpoint: str, token: str, menu_id: str) -> list[dict]:
    q = """query($id: ID!) {
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
    res = gql(endpoint, token, q, {"id": menu_id})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    menu = res["data"]["menu"]

    def flatten(items):
        for it in items or []:
            yield it
            yield from flatten(it.get("items") or [])

    def normalize_to_handle(url: str) -> str | None:
        from urllib.parse import urlparse

        path = urlparse(url or "").path
        if not path:
            return None
        parts = [p for p in path.split("/") if p]
        if parts and len(parts[0]) == 2:
            parts = parts[1:]
        if len(parts) < 2 or parts[0] != "collections":
            return None
        return parts[1]

    out: list[dict] = []
    seen: set[str] = set()
    for it in flatten(menu.get("items")):
        if it.get("type") != "COLLECTION":
            continue
        handle = normalize_to_handle(it.get("url") or "")
        if not handle or handle in seen:
            continue
        seen.add(handle)
        out.append({"handle": handle, "label": it.get("title") or ""})
    return out


def fetch_menu_full(gql, endpoint: str, token: str, menu_id: str) -> dict:
    q = """query($id: ID!) {
  menu(id: $id) {
    id
    handle
    title
    items {
      id
      title
      type
      url
      resourceId
      tags
      items {
        id
        title
        type
        url
        resourceId
        tags
        items {
          id
          title
          type
          url
          resourceId
          tags
        }
      }
    }
  }
}""".strip()
    res = gql(endpoint, token, q, {"id": menu_id})
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    menu = res["data"]["menu"]
    if not menu:
        raise SystemExit(f"Menu not found by id: {menu_id}")
    return menu


def menu_update(gql, endpoint: str, token: str, menu: dict) -> dict:
    q = """mutation($id: ID!, $title: String!, $handle: String, $items: [MenuItemUpdateInput!]!) {
  menuUpdate(id: $id, title: $title, handle: $handle, items: $items) {
    menu { id handle title }
    userErrors { field message }
  }
}""".strip()
    vars = {"id": menu["id"], "title": menu["title"], "handle": menu.get("handle"), "items": menu["items"]}
    res = gql(endpoint, token, q, vars)
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"], ensure_ascii=False, indent=2))
    payload = res["data"]["menuUpdate"]
    errs = payload.get("userErrors") or []
    if errs:
        raise SystemExit("UserErrors: " + json.dumps(errs, ensure_ascii=False))
    return payload["menu"]


def rewrite_menu_items_url_handle(items: list[dict], old_handle: str, new_handle: str) -> tuple[list[dict], int]:
    rewritten = 0
    out: list[dict] = []
    needle = f"/collections/{old_handle}"
    replacement = f"/collections/{new_handle}"
    for it in items or []:
        child_items = it.get("items") or []
        new_children, child_rewritten = rewrite_menu_items_url_handle(child_items, old_handle, new_handle)
        rewritten += child_rewritten
        url = it.get("url")
        if isinstance(url, str) and needle in url:
            url = url.replace(needle, replacement)
            rewritten += 1
        updated = {
            "id": it.get("id"),
            "title": it.get("title"),
            "type": it.get("type"),
            "url": url,
            "resourceId": it.get("resourceId"),
            "tags": it.get("tags") or [],
            "items": new_children,
        }
        out.append(updated)
    return out, rewritten


def rewrite_menu_items_resource_id(items: list[dict], old_id: str, new_id: str) -> tuple[list[dict], int]:
    """
    Returns (updated_items, count_rewritten).
    Preserves item shape for MenuItemUpdateInput.
    """
    rewritten = 0
    out: list[dict] = []
    for it in items or []:
        child_items = it.get("items") or []
        new_children, child_rewritten = rewrite_menu_items_resource_id(child_items, old_id, new_id)
        rewritten += child_rewritten
        resource_id = it.get("resourceId")
        if isinstance(resource_id, str) and resource_id == old_id:
            resource_id = new_id
            rewritten += 1
        updated = {
            "id": it.get("id"),
            "title": it.get("title"),
            "type": it.get("type"),
            "url": it.get("url"),
            "resourceId": resource_id,
            "tags": it.get("tags") or [],
            "items": new_children,
        }
        out.append(updated)
    return out, rewritten
