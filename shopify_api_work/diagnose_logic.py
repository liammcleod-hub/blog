from __future__ import annotations

import json
from collections import defaultdict


def _rule_key(rule: dict) -> str:
    col = (rule.get("column") or "").upper()
    rel = (rule.get("relation") or "").upper()
    cond = (rule.get("condition") or "").strip()
    return f"{col} {rel} {cond}".strip()


def diagnose_collection(
    *,
    collection: dict,
    products: list[dict],
    verification: dict,
    explain_matches_fn,
) -> dict:
    """
    Read-only diagnosis of why a collection is failing congruency:
    - which rules are admitting outliers (SMART)
    - which rules are high-noise candidates for tightening
    """
    rule_set = collection.get("ruleSet") or {}
    rules = list(rule_set.get("rules") or [])
    applied_disj = rule_set.get("appliedDisjunctively")

    outliers = verification.get("outliers") or []
    outlier_handles = {o.get("handle") for o in outliers if o.get("handle")}
    outlier_products = [p for p in products if p.get("handle") in outlier_handles]
    inlier_products = [p for p in products if p.get("handle") not in outlier_handles]

    explained = explain_matches_fn(rule_set if rule_set else None, products)
    explained_by_handle = {p.get("handle"): p for p in explained if p.get("handle")}

    # Count matches per rule for outliers vs inliers.
    counts = defaultdict(lambda: {"outlier": 0, "inlier": 0})
    for p in outlier_products:
        matched = (explained_by_handle.get(p.get("handle")) or {}).get("matched_rules") or []
        for r in matched:
            counts[_rule_key(r)]["outlier"] += 1
    for p in inlier_products:
        matched = (explained_by_handle.get(p.get("handle")) or {}).get("matched_rules") or []
        for r in matched:
            counts[_rule_key(r)]["inlier"] += 1

    rule_stats: list[dict] = []
    for r in rules:
        key = _rule_key(r)
        c = counts.get(key) or {"outlier": 0, "inlier": 0}
        out_c = int(c["outlier"])
        in_c = int(c["inlier"])
        total = out_c + in_c
        precision = (in_c / total) if total else 1.0
        rule_stats.append(
            {
                "rule": r,
                "key": key,
                "outlier_matches": out_c,
                "inlier_matches": in_c,
                "precision": round(precision, 4),
                "match_total": total,
            }
        )

    # High-noise candidates: match many outliers and have low precision.
    tighten_candidates = [
        s
        for s in rule_stats
        if s["outlier_matches"] >= 2 and s["precision"] <= 0.5
    ]
    tighten_candidates.sort(key=lambda x: (-x["outlier_matches"], x["precision"], -x["match_total"], x["key"]))

    # "Umbrella risk" proxy: many rules or AND logic.
    rule_breadth = len(rules)
    umbrella_risk = "HIGH" if rule_breadth >= 20 else ("MED" if rule_breadth >= 10 else "LOW")
    if applied_disj is False:
        umbrella_risk = "HIGH"

    return {
        "collection": {
            "id": collection.get("id"),
            "handle": collection.get("handle"),
            "title": collection.get("title"),
            "kind": "SMART" if collection.get("ruleSet") else "MANUAL",
            "appliedDisjunctively": applied_disj,
            "rules_count": rule_breadth,
        },
        "verification": verification,
        "metrics": {
            "total_products": len(products),
            "outliers": len(outlier_products),
            "inliers": len(inlier_products),
            "outlier_ratio": verification.get("outlier_ratio"),
            "umbrella_risk": umbrella_risk,
        },
        "rules": {
            "stats": rule_stats,
            "tighten_candidates": tighten_candidates[:15],
        },
        "outliers": [
            {
                "title": p.get("title"),
                "handle": p.get("handle"),
                "productType": p.get("productType"),
                "matched_rules": (explained_by_handle.get(p.get("handle")) or {}).get("matched_rules") or [],
            }
            for p in outlier_products
        ],
    }


def to_markdown(d: dict) -> str:
    c = d["collection"]
    m = d["metrics"]
    lines: list[str] = []
    lines.append(f"# Diagnose: {c['title']} (`{c['handle']}`)")
    lines.append("")
    lines.append(f"- Kind: {c['kind']}")
    if c["kind"] == "SMART":
        lines.append(f"- Rules: {c['rules_count']} (appliedDisjunctively={c.get('appliedDisjunctively')})")
    lines.append(f"- Products: {m['total_products']}")
    lines.append(f"- Outliers: {m['outliers']} (ratio={m.get('outlier_ratio')})")
    lines.append(f"- Umbrella risk: {m['umbrella_risk']}")
    lines.append("")

    lines.append("## Tighten candidates (top)")
    tcs = (d.get("rules") or {}).get("tighten_candidates") or []
    if not tcs:
        lines.append("- (none)")
    else:
        for s in tcs:
            lines.append(
                f"- outliers={s['outlier_matches']} inliers={s['inlier_matches']} precision={s['precision']} :: `{s['key']}`"
            )
    lines.append("")

    lines.append("## Outliers")
    outs = d.get("outliers") or []
    if not outs:
        lines.append("- (none)")
    else:
        for o in outs[:50]:
            lines.append(f"- {o.get('title')} (`{o.get('handle')}`) type={o.get('productType')}")
    if len(outs) > 50:
        lines.append(f"- … plus {len(outs) - 50} more")
    lines.append("")
    return "\n".join(lines) + "\n"

