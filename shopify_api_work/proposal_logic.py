from __future__ import annotations


def _slugify_handle_from_title(title: str) -> str:
    import re

    s = (title or "").strip().lower()
    s = s.replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


def propose(
    handle: str,
    coll: dict,
    cfg: dict,
    legacy_suffix: str,
    smart_suffix: str,
    default_menu_id: str,
    *,
    products: list[dict] | None = None,
    manual_rule_inference: dict | None = None,
    verification: dict | None = None,
) -> dict:
    kind = "SMART" if coll.get("ruleSet") else "MANUAL"
    curated = handle in set(cfg.get("curated_handles") or [])
    rules_overrides = (cfg.get("rules_overrides") or {}).get(handle) or {}

    proposal: dict = {
        "handle": handle,
        "collection_id": coll["id"],
        "title": coll["title"],
        "kind": kind,
        "curated": curated,
        "actions": {},
        "notes": [],
    }

    if curated:
        proposal["notes"].append("Curated: do not auto-remove. Only manual edits with explicit approval.")

    if kind == "SMART":
        rs = coll.get("ruleSet") or {}
        count = (coll.get("productsCount") or {}).get("count", 0)
        if count == 0 and rs and rs.get("appliedDisjunctively") is False:
            proposal["notes"].append("This smart collection is empty and uses AND logic (appliedDisjunctively=false).")
            desired_disj = rules_overrides.get("appliedDisjunctively", True)
            if desired_disj is not None and desired_disj != rs.get("appliedDisjunctively"):
                proposal["actions"]["update_ruleSet"] = {
                    "appliedDisjunctively": bool(desired_disj),
                    "rules": rs.get("rules") or [],
                }
                proposal["notes"].append("Proposed: switch to OR logic to populate the umbrella.")

    if kind == "MANUAL" and not curated:
        manual_to_smart_overrides = cfg.get("manual_to_smart_overrides") or {}
        if handle in manual_to_smart_overrides:
            desired_rs = manual_to_smart_overrides[handle]
            proposal["actions"]["replace_with_smart"] = {
                "legacy_handle": f"{handle}{legacy_suffix}",
                "smart_handle_temp": f"{handle}{smart_suffix}",
                "ruleSet": desired_rs,
                "menu_id": cfg.get("menu_id") or default_menu_id,
                "legacy_title_prefix": "LEGACY: ",
            }
            proposal["notes"].append(
                "Proposed: replace MANUAL collection with a new SMART collection (Shopify can't convert custom->smart)."
            )
        else:
            # If we have observe-time inference for this MANUAL collection, use it to propose a conversion
            # when signals are strong. This remains approval-gated downstream.
            inf = manual_rule_inference or {}
            conv = (inf.get("convertibility") or {}) if isinstance(inf, dict) else {}
            level = (conv.get("level") or "").upper()
            ver = verification if isinstance(verification, dict) else {}
            outlier_ratio = ver.get("outlier_ratio") if isinstance(ver, dict) else None
            outlier_zero = False
            try:
                outlier_zero = (outlier_ratio is not None) and float(outlier_ratio) == 0.0
            except Exception:
                outlier_zero = False

            # Senior-SWE stance: a MANUAL collection with outlier_ratio==0.0 is a strong signal that
            # membership aligns with the collection intent and is often safe to convert to SMART taxonomy,
            # *provided we have a cohesive inferred rule set*.
            should_auto_convert = level == "HIGH" or outlier_zero
            if isinstance(ver, dict) and ver.get("passed") is False:
                # Don't convert a MANUAL collection to SMART if our observe phase says the current
                # membership doesn't match the collection intent. This likely indicates either
                # (a) the collection is curated/semantic and should remain manual, or
                # (b) the membership needs cleanup before any conversion.
                should_auto_convert = False
                proposal["notes"].append("Manual inference present, but verify failed; skipping MANUAL->SMART auto-convert.")
            if should_auto_convert:
                suggested_rs = inf.get("suggested_ruleSet") if isinstance(inf, dict) else None
                inferred_ruleset = suggested_rs if isinstance(suggested_rs, dict) else None
                inferred_rules = (inferred_ruleset.get("rules") if inferred_ruleset else None) or []
                inferred_rules = [r for r in inferred_rules if isinstance(r, dict) and r.get("condition")]
                if inferred_ruleset and inferred_rules and len(inferred_rules) >= 2:
                    final_handle = _slugify_handle_from_title(coll.get("title") or "")
                    proposal["actions"]["replace_with_smart"] = {
                        "legacy_handle": f"{handle}{legacy_suffix}",
                        "smart_handle_temp": f"{handle}{smart_suffix}",
                        "final_handle": final_handle if final_handle else None,
                        "publication_name": "Online Store",
                        "ruleSet": {
                            "appliedDisjunctively": bool(inferred_ruleset.get("appliedDisjunctively", True)),
                            "rules": inferred_rules,
                        },
                        "menu_id": cfg.get("menu_id") or default_menu_id,
                        "legacy_title_prefix": "LEGACY: ",
                    }
                    if outlier_zero:
                        proposal["notes"].append("Proposed: convert MANUAL->SMART because outlier_ratio=0.0 and inferred rules are cohesive.")
                    else:
                        proposal["notes"].append("Proposed: convert MANUAL->SMART based on inferred membership signals (HIGH convertibility).")
                elif inferred_rules:
                    proposal["notes"].append(
                        "Manual conversion candidate, but inferred ruleset is single-signal; skipping auto-convert to avoid pulling unrelated products. Add an explicit manual_to_smart_override or strengthen inferred rules."
                    )
                else:
                    proposal["notes"].append("Manual inference marked HIGH convertibility, but produced no usable rules.")
            elif level in {"MED", "LOW"} and isinstance(inf, dict) and inf:
                # Still surface inference context for humans even if we don't auto-propose conversion.
                proposal["notes"].append(f"Manual inference: convertibility={level} (no auto-conversion proposed).")

    if kind == "MANUAL" and isinstance(manual_rule_inference, dict) and manual_rule_inference:
        proposal["manual_rule_inference"] = manual_rule_inference

    return proposal


def curated_heuristic_suggestions(collections: list[dict]) -> list[dict]:
    keywords = [
        "deko",
        "dekoration",
        "halloween",
        "weihnacht",
        "winter",
        "herbst",
        "sommer",
        "fruehling",
        "frühling",
        "ostern",
        "hochzeit",
        "baby",
        "geburt",
        "mama",
        "papa",
        "valentin",
        "love",
    ]
    deny = [
        "zubehor",
        "zubehör",
        "werkzeug",
        "material",
        "farben",
        "papiere",
        "schablonen",
        "servietten",
        "reispapier",
        "silikonformen",
        "kleber",
        "stempel",
    ]

    out: list[dict] = []
    for c in collections:
        title = (c.get("title") or "").lower()
        handle = (c.get("handle") or "").lower()
        hay = f"{title} {handle}"
        reasons = [k for k in keywords if k in hay]
        if not reasons:
            continue
        if any(d in hay for d in deny):
            continue
        # Keep output shape stable: existing tools expect key "reason".
        out.append({"handle": c.get("handle"), "title": c.get("title"), "reason": reasons})
    out.sort(key=lambda x: (x.get("title") or "", x.get("handle") or ""))
    return out


def should_never_touch(handle: str, title: str, cfg: dict) -> tuple[bool, str | None]:
    curated = set(cfg.get("curated_handles") or [])
    if handle in curated:
        return True, "curated_handles"
    never_handles = set(cfg.get("never_touch_handles") or [])
    if handle in never_handles:
        return True, "never_touch_handles"
    keywords = [k.lower() for k in (cfg.get("never_touch_title_keywords") or []) if isinstance(k, str) and k.strip()]
    t = (title or "").lower()
    for k in keywords:
        if k in t:
            return True, f"never_touch_title_keywords:{k}"
    return False, None


def infer_curated_candidates(menu_handles: list[dict], collections_by_handle: dict[str, dict]) -> list[dict]:
    seasonal = [
        "deko",
        "dekoration",
        "weihnacht",
        "halloween",
        "ostern",
        "frühling",
        "fruehling",
        "sommer",
        "herbst",
        "winter",
        "valentin",
        "hochzeit",
        "geburt",
        "baby",
        "mama",
        "papa",
        "you and me",
        "you & me",
    ]
    campaign = [
        "dekorieren mit",
        "richtige anwendung",
        "mal anders",
        "wir ",
        "du ",
        "ihr ",
        "mein ",
        "dein ",
        "ideen",
        "inspiration",
        "tutorial",
        "anleitung",
    ]

    out: list[dict] = []
    for m in menu_handles:
        handle = m["handle"]
        coll = collections_by_handle.get(handle)
        if not coll:
            continue
        title = coll.get("title") or ""
        hay = f"{title} {handle}".lower()

        reasons: list[str] = []
        never = False
        if any(k in hay for k in seasonal):
            reasons.append("seasonal/event/story keyword")
            never = True
        if "!" in title or "?" in title:
            reasons.append("punctuation (!/?) suggests campaign/curated")
            never = True
        if any(k in hay for k in campaign):
            reasons.append("campaign/tutorial phrasing")

        if reasons:
            out.append(
                {
                    "handle": handle,
                    "title": title,
                    "proposed": "never_touch" if never else "curated",
                    "reasons": reasons,
                }
            )

    out.sort(key=lambda x: (x["proposed"], x["title"] or "", x["handle"] or ""))
    return out
