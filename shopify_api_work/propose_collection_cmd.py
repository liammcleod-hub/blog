import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_CONFIG_PATH, DEFAULT_ENV_PATH, DEFAULT_MENU_ID, OUT_DIR, fetch_collection_products, fetch_menu_collections, inspect_collection, load_config, propose, shopify_cfg
from manual_rule_inference import infer_manual_rules_from_members


def _find_latest_observe_file(out_dir: pathlib.Path) -> pathlib.Path | None:
    files = sorted(out_dir.glob("observe_*.json"), key=lambda p: p.name, reverse=True)
    return files[0] if files else None


def _load_observe_inference(out_file: pathlib.Path, handle: str) -> dict | None:
    try:
        data = json.loads(out_file.read_text(encoding="utf-8"))
    except Exception:
        return None
    rows = data.get("rows") or []
    for r in rows:
        if (r.get("handle") or "") == handle:
            inf = r.get("manual_rule_inference")
            return inf if isinstance(inf, dict) else None
    return None


def _load_observe_verification(out_file: pathlib.Path, handle: str) -> dict | None:
    try:
        data = json.loads(out_file.read_text(encoding="utf-8"))
    except Exception:
        return None
    rows = data.get("rows") or []
    for r in rows:
        if (r.get("handle") or "") == handle:
            ver = r.get("verification")
            return ver if isinstance(ver, dict) else None
    return None


def main() -> None:
    try:
        import sys as _sys

        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python propose_collection_cmd.py <handle> [--menu-only] [--observe-file <path>]")
    handle = sys.argv[1]
    menu_only = "--menu-only" in sys.argv[2:]
    observe_file = None
    if "--observe-file" in sys.argv[2:]:
        try:
            idx = sys.argv.index("--observe-file")
            observe_file = pathlib.Path(sys.argv[idx + 1])
        except Exception:
            raise SystemExit("--observe-file requires a file path argument")

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if menu_only:
        menu_id = cfg.get("menu_id") or DEFAULT_MENU_ID
        menu_handles = {m["handle"] for m in fetch_menu_collections(endpoint, token, menu_id)}
        if handle not in menu_handles:
            raise SystemExit(f"--menu-only: handle not present in MAIN menu: {handle}")

    coll = inspect_collection(endpoint, token, handle)
    products = None
    manual_inf = None

    # Prefer most recent observe snapshot (reproducible) for MANUAL inference.
    if not coll.get("ruleSet"):
        snap = observe_file
        if snap is None:
            snap = _find_latest_observe_file(OUT_DIR)
        if snap is not None and snap.exists():
            manual_inf = _load_observe_inference(snap, handle)

    # Prefer observe snapshot verification when available (reproducible), for both SMART and MANUAL.
    snap_for_ver = observe_file
    if snap_for_ver is None:
        snap_for_ver = _find_latest_observe_file(OUT_DIR)
    verification = _load_observe_verification(snap_for_ver, handle) if snap_for_ver and snap_for_ver.exists() else None

    # Fallback: compute inference from live members if no snapshot is available.
    try:
        products = fetch_collection_products(endpoint, token, handle)
        if not coll.get("ruleSet") and manual_inf is None:
            manual_inf = infer_manual_rules_from_members(
                products,
                collection_title=coll.get("title"),
                collection_handle=coll.get("handle"),
                cfg=cfg,
            )
    except Exception:
        products = None

    try:
        if products is not None:
            from verify_logic import verify_congruency

            # Only recompute if we don't already have a snapshot verification.
            if verification is None:
                verification = verify_congruency(coll["title"], coll["handle"], products, cfg=cfg, rule_set=coll.get("ruleSet"))
    except Exception:
        if verification is None:
            verification = None

    prop_obj = propose(handle, coll, cfg, products=products, manual_rule_inference=manual_inf, verification=verification)
    out_path = OUT_DIR / f"proposal_{handle}.json"
    out_path.write_text(json.dumps(prop_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))
    print(json.dumps(prop_obj, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
