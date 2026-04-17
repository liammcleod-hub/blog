from __future__ import annotations

import json
import pathlib


def apply_proposal_actions(
    *,
    endpoint: str,
    token: str,
    proposal: dict,
    inspect_collection,
    fetch_collection_products,
    build_collection_keywords,
    product_is_relevant_to_collection_title,
    tags_add,
    collection_update,
    collection_create,
    fetch_menu_full,
    menu_update,
    rewrite_menu_items_resource_id,
    ensure_url_redirect,
    rewrite_menu_items_url_handle,
    list_publications,
    publishable_publish,
    default_menu_id: str,
) -> dict:
    """
    Apply a proposal (writes). Returns a dict with a small verification payload.
    All Shopify operations are provided as callables to keep this module focused.
    """
    handle = proposal["handle"]
    actions = proposal.get("actions") or {}
    result: dict = {"handle": handle, "applied": [], "notes": []}

    if "update_ruleSet" in actions:
        upd = actions["update_ruleSet"]
        preserve = actions.get("preserve_relevant_existing_products", True)
        keep_tag = None
        preserved_count = 0

        coll = inspect_collection(endpoint, token, handle)
        if preserve:
            products_before = fetch_collection_products(endpoint, token, handle)
            keywords = build_collection_keywords(coll["title"], coll["handle"])
            keepers = [p for p in products_before if product_is_relevant_to_collection_title(keywords, p)]
            if keepers:
                keep_tag = f"keep:{handle}"
                keep_rule = {"column": "TAG", "relation": "EQUALS", "condition": keep_tag}
                existing_rules = list(upd.get("rules") or [])
                if not any(
                    (r.get("column"), r.get("relation"), r.get("condition"))
                    == (keep_rule["column"], keep_rule["relation"], keep_rule["condition"])
                    for r in existing_rules
                ):
                    existing_rules.append(keep_rule)
                upd = {**upd, "appliedDisjunctively": True, "rules": existing_rules}
                for p in keepers:
                    tags_add(endpoint, token, p["id"], [keep_tag])
                    preserved_count += 1

        input_obj = {"id": proposal["collection_id"], "ruleSet": upd}
        updated = collection_update(endpoint, token, input_obj)
        result["applied"].append({"action": "update_ruleSet", "collection": updated})
        if preserve:
            result["applied"].append({"action": "preserve_relevant_existing_products", "keep_tag": keep_tag, "preserved_count": preserved_count})

        # Keep collections visible after rule changes (safe default).
        publication_name = actions.get("publication_name") or "Online Store"
        pubs = list_publications(endpoint, token)
        target = None
        for p in pubs:
            if (p.get("name") or "").strip().lower() == str(publication_name).strip().lower():
                target = p
                break
        if not target:
            raise SystemExit(
                f"Publication not found by name: {publication_name}. Available: "
                + ", ".join(sorted({p.get('name') or '' for p in pubs if p.get('name')}))
            )
        publish_payload = publishable_publish(endpoint, token, proposal["collection_id"], [target["id"]])
        result["applied"].append({"action": "publishablePublish", "publication": target, "result": publish_payload})
        return result

    if "replace_with_smart" in actions:
        rep = actions["replace_with_smart"]
        legacy_handle = rep["legacy_handle"]
        smart_temp = rep["smart_handle_temp"]
        desired_rs = rep["ruleSet"]
        legacy_title_prefix = rep.get("legacy_title_prefix") or "LEGACY: "
        final_handle = rep.get("final_handle")
        menu_id = rep.get("menu_id") or default_menu_id
        publication_name = rep.get("publication_name") or "Online Store"

        current = inspect_collection(endpoint, token, handle)
        if current.get("ruleSet"):
            raise SystemExit(f"Refusing: {handle} is already SMART.")

        created = collection_create(endpoint, token, {"title": current["title"], "handle": smart_temp, "ruleSet": desired_rs})
        result["applied"].append({"action": "create_smart_temp", "collection": created})

        legacy = None
        promoted = None
        try:
            legacy = collection_update(endpoint, token, {"id": current["id"], "handle": legacy_handle, "title": f"{legacy_title_prefix}{current['title']}"})
            result["applied"].append({"action": "rename_old_to_legacy", "collection": legacy})

            promoted = collection_update(endpoint, token, {"id": created["id"], "handle": handle})
            result["applied"].append({"action": "promote_smart_to_original_handle", "collection": promoted})

            if final_handle and final_handle != handle:
                promoted = collection_update(endpoint, token, {"id": created["id"], "handle": final_handle})
                result["applied"].append({"action": "promote_smart_to_final_handle", "collection": promoted})
                result["applied"].append(
                    {
                        "action": "redirects_handle_normalization",
                        "redirects": [
                            ensure_url_redirect(endpoint, token, f"/collections/{handle}", f"/collections/{final_handle}"),
                            ensure_url_redirect(endpoint, token, f"/en/collections/{handle}", f"/en/collections/{final_handle}"),
                        ],
                    }
                )

            menu = fetch_menu_full(endpoint, token, menu_id)
            new_items, rewritten = rewrite_menu_items_resource_id(menu.get("items") or [], old_id=current["id"], new_id=created["id"])
            if rewritten == 0:
                raise SystemExit(f"Safety stop: no MAIN menu items referenced old collection id {current['id']}.")
            menu["items"] = new_items
            if final_handle and final_handle != handle:
                rewritten_items, rewritten_urls = rewrite_menu_items_url_handle(menu.get("items") or [], handle, final_handle)
                if rewritten_urls:
                    menu["items"] = rewritten_items
            updated_menu = menu_update(endpoint, token, menu)
            result["applied"].append({"action": "menuUpdate_rewrite_resourceId", "menu": updated_menu, "rewritten": rewritten})

            # Ensure the new collection is published to the storefront publication.
            pubs = list_publications(endpoint, token)
            target = None
            for p in pubs:
                if (p.get("name") or "").strip().lower() == str(publication_name).strip().lower():
                    target = p
                    break
            if not target:
                raise SystemExit(
                    f"Publication not found by name: {publication_name}. Available: "
                    + ", ".join(sorted({p.get('name') or '' for p in pubs if p.get('name')}))
                )
            publish_payload = publishable_publish(endpoint, token, created["id"], [target["id"]])
            result["applied"].append({"action": "publishablePublish", "publication": target, "result": publish_payload})
        except Exception:
            try:
                if promoted:
                    collection_update(endpoint, token, {"id": created["id"], "handle": smart_temp})
                if legacy:
                    collection_update(endpoint, token, {"id": current["id"], "handle": handle, "title": current["title"]})
            except Exception:
                pass
            raise

        post_new = inspect_collection(endpoint, token, handle)
        post_legacy = inspect_collection(endpoint, token, legacy_handle)
        menu_post = fetch_menu_full(endpoint, token, menu_id)
        _, rewritten_post = rewrite_menu_items_resource_id(menu_post.get("items") or [], old_id=current["id"], new_id=created["id"])
        result["verification"] = {
            "new": {
                "id": post_new["id"],
                "handle": post_new["handle"],
                "title": post_new["title"],
                "productsCount": (post_new.get("productsCount") or {}).get("count", 0),
                "isSmart": bool(post_new.get("ruleSet")),
            },
            "legacy": {
                "id": post_legacy["id"],
                "handle": post_legacy["handle"],
                "title": post_legacy["title"],
                "productsCount": (post_legacy.get("productsCount") or {}).get("count", 0),
                "isSmart": bool(post_legacy.get("ruleSet")),
            },
            "menu": {
                "id": menu_post["id"],
                "handle": menu_post.get("handle"),
                "title": menu_post.get("title"),
                "still_references_old_collection_id": rewritten_post > 0,
            },
        }
        return result

    result["notes"].append("No actionable changes in proposal.")
    return result


def apply_proposal_file(*, endpoint: str, token: str, proposal_path: pathlib.Path, yes: bool, apply_proposal_actions_fn) -> dict:
    if not yes:
        raise SystemExit("Refusing to write without --yes.")
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    return apply_proposal_actions_fn(proposal)
