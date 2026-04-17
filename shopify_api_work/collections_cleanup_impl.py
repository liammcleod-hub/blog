"""
Core implementation for Shopify collections cleanup.

This module intentionally contains the heavy lifting. Keep `collections_cleanup_runner.py`
as a thin CLI entrypoint.
"""

import argparse
import json
import pathlib
import subprocess
import sys
import time

from shopify_client import (
    fetch_collection_products,
    fetch_collection_products_by_id,
    gql,
    inspect_collection,
    inspect_collection_by_id,
    list_collections,
    load_config as load_config_file,
    shopify_cfg,
)
from verify_logic import build_collection_keywords, product_is_relevant_to_collection_title, verify_congruency
from proposal_logic import (
    curated_heuristic_suggestions as _curated_heuristic_suggestions,
    infer_curated_candidates as _infer_curated_candidates,
    propose as _propose,
    should_never_touch as _should_never_touch,
)
from shopify_writes import (
    collection_create as _collection_create,
    collection_update as _collection_update,
    ensure_url_redirect as _ensure_url_redirect,
    list_publications as _list_publications,
    publishable_publish as _publishable_publish,
    tags_add as _tags_add,
)
from apply_logic import apply_proposal_actions as _apply_proposal_actions
from orchestrate_reporting import write_orchestrate_files
from manual_rule_inference import infer_manual_rules_from_members
from menu_fetch import (
    fetch_menu_collections as _fetch_menu_collections,
    fetch_menu_full as _fetch_menu_full,
    menu_update as _menu_update,
    rewrite_menu_items_resource_id as _rewrite_menu_items_resource_id,
    rewrite_menu_items_url_handle as _rewrite_menu_items_url_handle,
)


BASE_DIR = pathlib.Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "out"
DEFAULT_ENV_PATH = BASE_DIR / ".env"
DEFAULT_CONFIG_PATH = BASE_DIR / "collections_cleanup_config.json"

DEFAULT_MENU_ID = "gid://shopify/Menu/320750813522"  # MAIN (handle: main)
LEGACY_HANDLE_SUFFIX = "-legacy"
SMART_HANDLE_SUFFIX = "-smart"


def load_config(path: pathlib.Path) -> dict:
    return load_config_file(path, DEFAULT_MENU_ID)


def explain_matches(rule_set: dict | None, products: list[dict]) -> list[dict]:
    rs = rule_set or {}
    rules = rs.get("rules") or []

    def matches_rule(p: dict, rule: dict) -> bool:
        col = (rule.get("column") or "").upper()
        rel = (rule.get("relation") or "").upper()
        cond = rule.get("condition") or ""
        title = p.get("title") or ""
        ptype = p.get("productType") or ""
        tags = p.get("tags") or []
        if col == "TAG":
            if rel != "EQUALS":
                return False
            return cond.lower() in {t.lower() for t in tags}
        if col == "TITLE":
            if rel == "CONTAINS":
                return cond.lower() in title.lower()
            if rel == "EQUALS":
                return title.strip().lower() == cond.strip().lower()
            return False
        if col == "TYPE":
            if rel != "EQUALS":
                return False
            return ptype.strip().lower() == cond.strip().lower()
        return False

    out: list[dict] = []
    for p in products:
        matched = [r for r in rules if matches_rule(p, r)]
        out.append(
            {
                "title": p.get("title"),
                "handle": p.get("handle"),
                "productType": p.get("productType"),
                "vendor": p.get("vendor"),
                "status": p.get("status"),
                "matched_rules": matched,
            }
        )
    return out


def _product_matches_rule(product: dict, rule: dict) -> bool:
    col = (rule.get("column") or "").upper()
    rel = (rule.get("relation") or "").upper()
    cond = rule.get("condition") or ""
    if not cond:
        return False
    title = product.get("title") or ""
    ptype = product.get("productType") or ""
    vendor = product.get("vendor") or ""
    tags = product.get("tags") or []
    if col == "TAG":
        if rel != "EQUALS":
            return False
        return str(cond).strip().lower() in {str(t).strip().lower() for t in tags if isinstance(t, str)}
    if col == "TITLE":
        if rel == "CONTAINS":
            return str(cond).strip().lower() in str(title).lower()
        if rel == "EQUALS":
            return str(title).strip().lower() == str(cond).strip().lower()
        return False
    if col == "TYPE":
        if rel != "EQUALS":
            return False
        return str(ptype).strip().lower() == str(cond).strip().lower()
    if col == "VENDOR":
        if rel != "EQUALS":
            return False
        return str(vendor).strip().lower() == str(cond).strip().lower()
    return False


def simulate_ruleset_on_products(rule_set: dict | None, products: list[dict]) -> dict:
    """
    Read-only simulation of a Shopify SMART ruleSet against an existing product list.

    Used to answer "what would happen if we applied this ruleset" before writing.
    NOTE: This only simulates on the current collection members (no catalog-wide leakage check).
    """
    rs = rule_set or {}
    rules = list(rs.get("rules") or [])
    disj = rs.get("appliedDisjunctively")
    if disj is None:
        disj = True

    total = len(products)
    matched: list[dict] = []
    excluded: list[dict] = []

    for p in products:
        rule_hits = [r for r in rules if _product_matches_rule(p, r)]
        if not rules:
            ok = False
        elif disj:
            ok = len(rule_hits) > 0
        else:
            ok = len(rule_hits) == len(rules)
        row = {"title": p.get("title"), "handle": p.get("handle"), "productType": p.get("productType"), "vendor": p.get("vendor")}
        if ok:
            matched.append(row)
        else:
            excluded.append(row)

    cov = round((len(matched) / total), 4) if total else 0.0
    return {
        "appliedDisjunctively": bool(disj),
        "rules_count": len(rules),
        "members_total": total,
        "members_matched": len(matched),
        "members_excluded": len(excluded),
        "member_coverage": cov,
        "excluded_sample": excluded[:10],
    }


def fetch_menu_collections(endpoint: str, token: str, menu_id: str) -> list[dict]:
    return _fetch_menu_collections(gql, endpoint, token, menu_id)


def fetch_menu_full(endpoint: str, token: str, menu_id: str) -> dict:
    return _fetch_menu_full(gql, endpoint, token, menu_id)


def menu_update(endpoint: str, token: str, menu: dict) -> dict:
    return _menu_update(gql, endpoint, token, menu)


def rewrite_menu_items_resource_id(items: list[dict], old_id: str, new_id: str) -> tuple[list[dict], int]:
    return _rewrite_menu_items_resource_id(items, old_id, new_id)


def list_publications(endpoint: str, token: str) -> list[dict]:
    return _list_publications(gql, endpoint, token)


def publishable_publish(endpoint: str, token: str, publishable_id: str, publication_ids: list[str]) -> dict:
    return _publishable_publish(gql, endpoint, token, publishable_id, publication_ids)


def ensure_url_redirect(endpoint: str, token: str, path: str, target: str) -> dict:
    return _ensure_url_redirect(gql, endpoint, token, path, target)


def rewrite_menu_items_url_handle(items: list[dict], old_handle: str, new_handle: str) -> tuple[list[dict], int]:
    """
    Best-effort rewrite for menu item urls that hardcode /collections/<handle>.
    Returns (updated_items, count_rewritten).
    """
    return _rewrite_menu_items_url_handle(items, old_handle, new_handle)


def propose(
    handle: str,
    coll: dict,
    cfg: dict,
    *,
    products: list[dict] | None = None,
    manual_rule_inference: dict | None = None,
    verification: dict | None = None,
) -> dict:
    return _propose(
        handle,
        coll,
        cfg,
        LEGACY_HANDLE_SUFFIX,
        SMART_HANDLE_SUFFIX,
        DEFAULT_MENU_ID,
        products=products,
        manual_rule_inference=manual_rule_inference,
        verification=verification,
    )


def curated_heuristic_suggestions(collections: list[dict]) -> list[dict]:
    return _curated_heuristic_suggestions(collections)


def should_never_touch(handle: str, title: str, cfg: dict) -> tuple[bool, str | None]:
    return _should_never_touch(handle, title, cfg)


def infer_curated_candidates(menu_handles: list[dict], collections_by_handle: dict[str, dict]) -> list[dict]:
    return _infer_curated_candidates(menu_handles, collections_by_handle)


def _ensure_stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # pyright: ignore[reportGeneralTypeIssues]
    except Exception:
        pass


def collection_update(endpoint: str, token: str, input_obj: dict) -> dict:
    return _collection_update(gql, endpoint, token, input_obj)


def collection_create(endpoint: str, token: str, input_obj: dict) -> dict:
    return _collection_create(gql, endpoint, token, input_obj)


def tags_add(endpoint: str, token: str, id_: str, tags: list[str]) -> dict:
    return _tags_add(gql, endpoint, token, id_, tags)


def apply_proposal_actions(endpoint: str, token: str, proposal: dict) -> dict:
    return _apply_proposal_actions(
        endpoint=endpoint,
        token=token,
        proposal=proposal,
        inspect_collection=inspect_collection,
        fetch_collection_products=fetch_collection_products,
        build_collection_keywords=build_collection_keywords,
        product_is_relevant_to_collection_title=product_is_relevant_to_collection_title,
        tags_add=tags_add,
        collection_update=collection_update,
        collection_create=collection_create,
        fetch_menu_full=fetch_menu_full,
        menu_update=menu_update,
        rewrite_menu_items_resource_id=rewrite_menu_items_resource_id,
        ensure_url_redirect=ensure_url_redirect,
        rewrite_menu_items_url_handle=rewrite_menu_items_url_handle,
        list_publications=list_publications,
        publishable_publish=publishable_publish,
        default_menu_id=DEFAULT_MENU_ID,
    )


def apply_proposal_file(endpoint: str, token: str, proposal_path: pathlib.Path, yes: bool) -> dict:
    if not yes:
        raise SystemExit("Refusing to write without --yes.")

    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    return apply_proposal_actions(endpoint, token, proposal)


def _priority_bucket(verification: dict | None, kind: str, curated: bool) -> str:
    """
    High / Mid / Low priority based on congruency risk.
    - If verify fails -> High
    - If outlier_ratio > 0.2 -> Mid
    - Otherwise Low
    Manual collections in MAIN that are not curated are at least Mid (needs human decision).
    """
    if curated:
        return "Low"
    if kind == "MANUAL":
        return "Mid"
    if not verification:
        return "Mid"
    if verification.get("passed") is False:
        return "High"
    if (verification.get("outlier_ratio") or 0) > 0.2:
        return "Mid"
    return "Low"


def _orchestrate_build_proposals(endpoint: str, token: str, cfg: dict) -> dict:
    menu_id = cfg.get("menu_id") or DEFAULT_MENU_ID
    menu_handles = fetch_menu_collections(endpoint, token, menu_id)
    curated = set(cfg.get("curated_handles") or [])
    never_handles = set(cfg.get("never_touch_handles") or [])

    rows: list[dict] = []
    for m in menu_handles:
        handle = m["handle"]
        coll = inspect_collection(endpoint, token, handle)
        never, never_reason = should_never_touch(handle, coll.get("title") or "", cfg)
        if never:
            rows.append(
                {
                    "handle": handle,
                    "title": coll["title"],
                    "collection_id": coll["id"],
                    "kind": "SMART" if coll.get("ruleSet") else "MANUAL",
                    "curated": bool(handle in curated),
                    "never_touch": True,
                    "never_touch_reason": never_reason,
                    "productsCount": (coll.get("productsCount") or {}).get("count", 0),
                    "verification": None,
                    "priority": "Low",
                    "proposal": None,
                }
            )
            continue
        kind = "SMART" if coll.get("ruleSet") else "MANUAL"
        is_curated = handle in curated

        # Verification uses real products (not just snapshot) so it can be run independently.
        # Run for both SMART and MANUAL so we always have observe metrics visibility.
        products: list[dict] | None = None
        verification: dict | None = None
        manual_rule_inference: dict | None = None
        try:
            products = fetch_collection_products(endpoint, token, handle)
            verification = verify_congruency(
                coll["title"],
                coll["handle"],
                products,
                cfg=cfg,
                rule_set=coll.get("ruleSet"),
            )
            if kind == "MANUAL":
                manual_rule_inference = infer_manual_rules_from_members(
                    products,
                    collection_title=coll.get("title"),
                    collection_handle=coll.get("handle"),
                    cfg=cfg,
                )
        except Exception:
            verification = None
            manual_rule_inference = None

        proposal = propose(handle, coll, cfg, products=products, manual_rule_inference=manual_rule_inference, verification=verification)
        actions = proposal.get("actions") or {}
        dry_run = None
        try:
            if products is not None and isinstance(actions, dict) and actions:
                if "replace_with_smart" in actions and isinstance(actions.get("replace_with_smart"), dict):
                    rs = (actions.get("replace_with_smart") or {}).get("ruleSet")
                    if isinstance(rs, dict):
                        dry_run = simulate_ruleset_on_products(rs, products)
                elif "update_ruleSet" in actions and isinstance(actions.get("update_ruleSet"), dict):
                    rs = actions.get("update_ruleSet")
                    if isinstance(rs, dict):
                        dry_run = simulate_ruleset_on_products(rs, products)
        except Exception:
            dry_run = None

        rows.append(
            {
                "handle": handle,
                "title": coll["title"],
                "collection_id": coll["id"],
                "kind": kind,
                "curated": bool(is_curated),
                "never_touch": bool(handle in never_handles),
                "productsCount": (coll.get("productsCount") or {}).get("count", 0),
                "ruleSet": coll.get("ruleSet") if kind == "SMART" else None,
                "verification": verification,
                "manual_rule_inference": manual_rule_inference,
                "proposal_dry_run": dry_run,
                "priority": _priority_bucket(verification, kind, bool(is_curated)),
                "proposal": proposal,
            }
        )

    # Split for reporting
    by_priority: dict[str, list[dict]] = {"High": [], "Mid": [], "Low": []}
    for r in rows:
        by_priority[r["priority"]].append(r)
    for k in by_priority:
        by_priority[k].sort(key=lambda x: (x["title"] or "", x["handle"] or ""))

    # Build approval file with explicit per-item gate
    approvals: list[dict] = []
    for r in rows:
        prop = r.get("proposal")
        if not prop:
            continue
        actions = prop.get("actions") or {}
        if not isinstance(actions, dict) or not actions:
            continue
        approvals.append(
            {
                "approve": "",
                "approved": False,
                "priority": r["priority"],
                "handle": r["handle"],
                "title": r["title"],
                "kind": r["kind"],
                "collection_id": r.get("collection_id"),
                "actions": actions,
                "dry_run": r.get("proposal_dry_run"),
                "verification": r.get("verification"),
                "proposal_file": None,
            }
        )

    return {"menu_id": menu_id, "rows": rows, "by_priority": by_priority, "approvals": approvals}


def _write_orchestrate_files(bundle: dict) -> dict:
    return write_orchestrate_files(bundle, OUT_DIR, BASE_DIR)


def _orchestrate_apply(endpoint: str, token: str, cfg: dict, approval_file: pathlib.Path, yes: bool) -> dict:
    if not yes:
        raise SystemExit("Refusing to write without --yes.")
    data = json.loads(approval_file.read_text(encoding="utf-8-sig"))
    items = data.get("items") or []
    applied: list[dict] = []
    skipped: list[dict] = []
    failed: list[dict] = []

    for it in items:
        approve_mark = str(it.get("approve") or "").strip().lower()
        is_approved = bool(it.get("approved")) or approve_mark == "x"
        if not is_approved:
            skipped.append({"handle": it.get("handle"), "title": it.get("title"), "priority": it.get("priority")})
            continue
        handle = it["handle"]
        collection_id = it.get("collection_id")
        # Snapshot before for safe rollback on verify fail (rule updates only).
        before = inspect_collection_by_id(endpoint, token, collection_id) if collection_id else inspect_collection(endpoint, token, handle)
        before_ruleset = before.get("ruleSet")
        proposal = {
            "handle": handle,
            "collection_id": before["id"],
            "title": before["title"],
            "kind": "SMART" if before.get("ruleSet") else "MANUAL",
            "curated": bool(handle in set(cfg.get("curated_handles") or [])),
            "actions": it.get("actions") or {},
            "notes": ["Applied via orchestrate approval file."],
        }
        try:
            res = apply_proposal_actions(endpoint, token, proposal)
            # Post-apply verify for SMART collections
            after = inspect_collection_by_id(endpoint, token, before["id"]) if before.get("id") else inspect_collection(endpoint, token, handle)
            if after.get("ruleSet"):
                products = fetch_collection_products_by_id(endpoint, token, after["id"]) if after.get("id") else fetch_collection_products(endpoint, token, handle)
                ver = verify_congruency(after["title"], after["handle"], products)
                if not ver.get("passed"):
                    # Roll back only if we were updating ruleSet (keep rollback KISS).
                    if "update_ruleSet" in (proposal.get("actions") or {}) and before_ruleset:
                        collection_update(endpoint, token, {"id": after["id"], "ruleSet": before_ruleset})
                    raise SystemExit(f"Verification failed after apply for {handle}: {json.dumps(ver, ensure_ascii=False)}")
            applied.append({"handle": handle, "result": res})
        except Exception as e:
            failed.append({"handle": handle, "error": str(e)})

    return {"applied": applied, "skipped": skipped, "failed": failed}


def _run_local_script(script_path: pathlib.Path) -> None:
    subprocess.check_call([sys.executable, str(script_path)])


def _run_local_script_args(script_path: pathlib.Path, extra_args: list[str]) -> None:
    try:
        subprocess.check_call([sys.executable, str(script_path), *extra_args])
    except subprocess.CalledProcessError as e:
        # Pass through underlying script errors without a Python stack trace.
        raise SystemExit(e.returncode)


def main():
    # Ensure stdout supports UTF-8 (Windows PowerShell defaults to cp1252).
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=str(DEFAULT_ENV_PATH))
    ap.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))

    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list")

    sub.add_parser("suggest-curated")

    sub.add_parser("menu-audit")

    ins = sub.add_parser("inspect")
    ins.add_argument("--handle", required=True)

    exp = sub.add_parser("explain")
    exp.add_argument("--handle", required=True)

    ver = sub.add_parser("verify")
    ver.add_argument("--handle", required=True)

    diag = sub.add_parser("diagnose")
    diag.add_argument("--handle", required=True)

    sub.add_parser("umbrella-suggest")

    prop = sub.add_parser("propose")
    prop.add_argument("--handle", required=True)
    prop.add_argument("--menu-only", action="store_true")

    app = sub.add_parser("apply")
    app.add_argument("--proposal", required=True)
    app.add_argument("--yes", action="store_true")

    pub = sub.add_parser("publish")
    pub.add_argument("--handle", required=True)
    pub.add_argument("--publication-name", default="Online Store")
    pub.add_argument("--yes", action="store_true")

    seo = sub.add_parser("seo")
    seo.add_argument("--handle", required=True)
    seo.add_argument("--new-handle")
    seo.add_argument("--seo-title", required=True)
    seo.add_argument("--seo-description", required=True)
    seo.add_argument("--description-html-file", required=True)
    seo.add_argument("--update-menu", action="store_true")
    seo.add_argument("--yes", action="store_true")

    red = sub.add_parser("redirect")
    red.add_argument("--path", required=True)
    red.add_argument("--target", required=True)
    red.add_argument("--yes", action="store_true")

    orch = sub.add_parser("orchestrate")
    orch.add_argument("--mode", choices=["propose", "apply"], required=True)
    orch.add_argument("--approval-file")
    orch.add_argument("--yes", action="store_true")

    cur = sub.add_parser("curation")
    cur.add_argument("--mode", choices=["propose", "apply"], required=True)
    cur.add_argument("--approval-file")
    cur.add_argument("--yes", action="store_true")

    args = ap.parse_args()

    endpoint, token = shopify_cfg(pathlib.Path(args.env))
    cfg = load_config(pathlib.Path(args.config))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.cmd == "list":
        _run_local_script(BASE_DIR / "list_collections.py")
        return

    if args.cmd == "suggest-curated":
        _run_local_script(BASE_DIR / "suggest_curated_cmd.py")
        return

    if args.cmd == "menu-audit":
        _run_local_script(BASE_DIR / "menu_audit.py")
        return

    if args.cmd == "inspect":
        _run_local_script_args(BASE_DIR / "inspect_collection_cmd.py", [args.handle])
        return

    if args.cmd == "explain":
        _run_local_script_args(BASE_DIR / "explain_collection_cmd.py", [args.handle])
        return

    if args.cmd == "verify":
        _run_local_script_args(BASE_DIR / "verify_collection_cmd.py", [args.handle])
        return

    if args.cmd == "diagnose":
        _run_local_script_args(BASE_DIR / "diagnose_collection_cmd.py", [args.handle])
        return

    if args.cmd == "umbrella-suggest":
        _run_local_script(BASE_DIR / "umbrella_suggest.py")
        return

    if args.cmd == "propose":
        extra = [args.handle]
        if args.menu_only:
            extra.append("--menu-only")
        _run_local_script_args(BASE_DIR / "propose_collection_cmd.py", extra)
        return

    if args.cmd == "apply":
        extra = [args.proposal]
        if args.yes:
            extra.append("--yes")
        _run_local_script_args(BASE_DIR / "apply_proposal_cmd.py", extra)
        return

    if args.cmd == "publish":
        if not args.yes:
            raise SystemExit("Refusing to write without --yes.")
        _run_local_script_args(BASE_DIR / "publish_collection_cmd.py", [args.handle, "--publication-name", args.publication_name])
        return

    if args.cmd == "seo":
        if not args.yes:
            raise SystemExit("Refusing to write without --yes.")
        extra = [args.handle, args.seo_title, args.seo_description, args.description_html_file]
        if args.new_handle:
            extra += ["--new-handle", args.new_handle]
        if args.update_menu:
            extra.append("--update-menu")
        _run_local_script_args(BASE_DIR / "seo_update_cmd.py", extra)
        return

    if args.cmd == "redirect":
        if not args.yes:
            raise SystemExit("Refusing to write without --yes.")
        _run_local_script_args(BASE_DIR / "redirect_create_cmd.py", [args.path, args.target])
        return

    if args.cmd == "orchestrate":
        if args.mode == "propose":
            _run_local_script(BASE_DIR / "orchestrate_propose.py")
            return
        if args.mode == "apply":
            if not args.approval_file:
                raise SystemExit("Missing --approval-file for orchestrate apply.")
            if not args.yes:
                raise SystemExit("Refusing to write without --yes.")
            _run_local_script_args(BASE_DIR / "orchestrate_apply.py", [args.approval_file])
            return

    if args.cmd == "curation":
        if args.mode == "propose":
            _run_local_script(BASE_DIR / "curation_propose.py")
            return

        if args.mode == "apply":
            if not args.approval_file:
                raise SystemExit("Missing --approval-file for curation apply.")
            if not args.yes:
                raise SystemExit("Refusing to write without --yes.")
            _run_local_script_args(BASE_DIR / "curation_apply.py", [args.approval_file, args.config])
            return


if __name__ == "__main__":
    main()
