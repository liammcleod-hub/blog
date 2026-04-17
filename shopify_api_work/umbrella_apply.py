import json
import pathlib
import sys

from collections_cleanup_impl import DEFAULT_CONFIG_PATH, load_config


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python umbrella_apply.py <umbrella_suggest.json>")
    suggest_path = pathlib.Path(sys.argv[1])
    cfg_path = pathlib.Path(sys.argv[2]) if len(sys.argv) >= 3 else pathlib.Path(DEFAULT_CONFIG_PATH)

    bundle = json.loads(suggest_path.read_text(encoding="utf-8-sig"))
    suggestions = bundle.get("suggestions") or []

    cfg = load_config(cfg_path)
    umbrella = set(cfg.get("verify_umbrella_handles") or [])
    force = set(cfg.get("verify_umbrella_force_handles") or [])

    added: list[str] = []
    for s in suggestions:
        handle = (s.get("handle") or "").strip()
        if not handle:
            continue
        outlier_ratio = float(s.get("outlier_ratio") or 0.0)
        if outlier_ratio <= 0.0:
            continue
        if handle not in umbrella:
            umbrella.add(handle)
            added.append(handle)

    # Special case: you explicitly want this to behave as umbrella even if its ruleSet is broad.
    if "zubehor-werkzeuge-1" in umbrella:
        force.add("zubehor-werkzeuge-1")

    cfg["verify_umbrella_handles"] = sorted(umbrella)
    if force:
        cfg["verify_umbrella_force_handles"] = sorted(force)

    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"config_path": str(cfg_path), "added": added, "umbrella_count": len(umbrella)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
