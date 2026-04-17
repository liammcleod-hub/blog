import json
import pathlib
import time
import sys

from collections_cleanup_impl import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_ENV_PATH,
    OUT_DIR,
    explain_matches,
)
from shopify_client import shopify_cfg, inspect_collection, fetch_collection_products, load_config
from verify_logic import verify_congruency
from diagnose_logic import diagnose_collection, to_markdown


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python diagnose_collection_cmd.py <handle>")
    handle = sys.argv[1]

    endpoint, token = shopify_cfg(pathlib.Path(DEFAULT_ENV_PATH))
    cfg = load_config(pathlib.Path(DEFAULT_CONFIG_PATH), default_menu_id="gid://shopify/Menu/320750813522")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    coll = inspect_collection(endpoint, token, handle)
    products = fetch_collection_products(endpoint, token, handle)
    verification = verify_congruency(coll["title"], coll["handle"], products, cfg=cfg, rule_set=coll.get("ruleSet"))
    diag = diagnose_collection(collection=coll, products=products, verification=verification, explain_matches_fn=explain_matches)

    ts = time.strftime("%Y%m%d-%H%M%S")
    out_json = OUT_DIR / f"diagnose_{handle}_{ts}.json"
    out_md = OUT_DIR / f"diagnose_{handle}_{ts}.md"
    out_json.write_text(json.dumps(diag, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(to_markdown(diag), encoding="utf-8")

    print(json.dumps({"json_path": str(out_json), "md_path": str(out_md)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

