from __future__ import annotations

from collections import Counter


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _tokenize_title(title: str) -> list[str]:
    import re

    stop = {
        "und",
        "oder",
        "mit",
        "fur",
        "für",
        "der",
        "die",
        "das",
        "set",
        "sets",
        "zum",
        "zur",
        "im",
        "in",
        "am",
        "an",
        "the",
        "and",
        "von",
        "aus",
    }
    t = _norm(title)
    toks = [x for x in re.split(r"[^a-z0-9äöüß]+", t) if x]
    return [x for x in toks if len(x) >= 5 and x not in stop]


def _matches_rule(product: dict, rule: dict) -> bool:
    col = (rule.get("column") or "").upper()
    rel = (rule.get("relation") or "").upper()
    cond = rule.get("condition") or ""
    if not cond:
        return False

    if col == "TAG":
        if rel != "EQUALS":
            return False
        tags = product.get("tags") or []
        return _norm(cond) in {_norm(t) for t in tags if isinstance(t, str)}
    if col == "TYPE":
        if rel != "EQUALS":
            return False
        return _norm(product.get("productType") or "") == _norm(cond)
    if col == "VENDOR":
        if rel != "EQUALS":
            return False
        return _norm(product.get("vendor") or "") == _norm(cond)
    if col == "TITLE":
        if rel != "CONTAINS":
            return False
        title = _norm(product.get("title") or "")
        return _norm(cond) in title
    return False


def _rule_alignment_keywords(rule: dict, collection_keywords: set[str]) -> tuple[bool, list[str]]:
    """
    Heuristic: does this rule "look like" the collection title/handle?

    This is NOT full semantic matching. It is a lightweight guard to avoid proposing
    rules that clearly describe something else (e.g. vendor/brand tags) when the
    collection is about a material/product type.
    """
    if not isinstance(rule, dict):
        return False, []
    col = (rule.get("column") or "").upper()
    rel = (rule.get("relation") or "").upper()
    cond = _norm(rule.get("condition") or "")
    if not cond:
        return False, []

    def tokens(s: str) -> set[str]:
        import re

        toks = {t for t in re.split(r"[^a-z0-9äöüß]+", _norm(s)) if t}
        return {t for t in toks if len(t) >= 4}

    cond_tokens = tokens(cond)
    kw_tokens = {_norm(k) for k in (collection_keywords or set()) if isinstance(k, str) and k.strip()}
    if not kw_tokens:
        return False, []

    hits = sorted([t for t in cond_tokens if t in kw_tokens])

    # TITLE contains <keyword> is considered aligned if it hits.
    if col == "TITLE" and rel == "CONTAINS":
        return (len(hits) > 0), hits

    # TAG equals X: aligned only if tokens overlap. (This avoids "pentart" style brand tags
    # unless the collection is explicitly about that brand.)
    if col == "TAG" and rel == "EQUALS":
        return (len(hits) > 0), hits

    # TYPE equals Y: treat as aligned if tokens overlap.
    if col == "TYPE" and rel == "EQUALS":
        return (len(hits) > 0), hits

    # VENDOR equals: almost never title-aligned; keep as non-aligned by default.
    if col == "VENDOR" and rel == "EQUALS":
        return False, []

    return False, hits


def infer_manual_rules_from_members(
    products: list[dict],
    *,
    collection_title: str | None = None,
    collection_handle: str | None = None,
    cfg: dict | None = None,
) -> dict:
    """
    Infer a lightweight, *member-only* approximation of what rules could reproduce
    a MANUAL collection's membership if expressed as a SMART ruleSet.

    This is intentionally conservative: it measures only coverage over current members
    (no full-catalog leakage/precision yet).
    """
    total = len(products)
    if total == 0:
        return {
            "total_members": 0,
            "candidates": [],
            "rule_breadth_estimate_80": 0,
            "rule_breadth_estimate_90": 0,
            "selected_rules_80": [],
            "selected_rules_90": [],
            "convertibility": {"level": "LOW", "reasons": ["empty_collection"]},
        }

    # Collect candidate conditions.
    tag_counter: Counter[str] = Counter()
    tag_repr: dict[str, str] = {}
    type_counter: Counter[str] = Counter()
    type_repr: dict[str, str] = {}
    vendor_counter: Counter[str] = Counter()
    vendor_repr: dict[str, str] = {}
    title_kw_counter: Counter[str] = Counter()

    for p in products:
        for t in (p.get("tags") or []):
            if not isinstance(t, str) or not t.strip():
                continue
            k = _norm(t)
            tag_counter[k] += 1
            tag_repr.setdefault(k, t.strip())
        pt = p.get("productType")
        if isinstance(pt, str) and pt.strip():
            k = _norm(pt)
            type_counter[k] += 1
            type_repr.setdefault(k, pt.strip())
        v = p.get("vendor")
        if isinstance(v, str) and v.strip():
            k = _norm(v)
            vendor_counter[k] += 1
            vendor_repr.setdefault(k, v.strip())
        title = p.get("title")
        if isinstance(title, str) and title.strip():
            for tok in _tokenize_title(title):
                title_kw_counter[tok] += 1

    # Build candidate rule objects in Shopify-ish rule shape.
    candidates: list[dict] = []

    def add_rule(*, rule: dict, kind: str, count: int) -> None:
        cov = round(count / total, 4) if total else 0.0
        candidates.append(
            {
                "rule": rule,
                "kind": kind,
                "member_matches": int(count),
                "member_coverage": cov,
            }
        )

    for k, c in tag_counter.most_common(25):
        add_rule(rule={"column": "TAG", "relation": "EQUALS", "condition": tag_repr.get(k, k)}, kind="TAG", count=c)
    for k, c in type_counter.most_common(15):
        add_rule(rule={"column": "TYPE", "relation": "EQUALS", "condition": type_repr.get(k, k)}, kind="TYPE", count=c)
    for k, c in vendor_counter.most_common(15):
        add_rule(rule={"column": "VENDOR", "relation": "EQUALS", "condition": vendor_repr.get(k, k)}, kind="VENDOR", count=c)
    for k, c in title_kw_counter.most_common(25):
        # Avoid extremely generic title tokens by requiring at least 10% member frequency.
        if c / total < 0.1:
            continue
        add_rule(rule={"column": "TITLE", "relation": "CONTAINS", "condition": k}, kind="TITLE", count=c)

    # Collection-keyword alignment (optional but strongly preferred when available).
    collection_keywords: set[str] = set()
    try:
        if collection_title or collection_handle:
            from verify_logic import build_collection_keywords

            collection_keywords = build_collection_keywords(collection_title or "", collection_handle or "", cfg=cfg or {})
    except Exception:
        collection_keywords = set()

    for c in candidates:
        aligned, hits = _rule_alignment_keywords(c.get("rule") or {}, collection_keywords)
        c["alignment"] = {"aligned": bool(aligned), "hits": hits}
        # Simple scalar score: prioritize coverage, then alignment, then rule kind preference.
        # Prefer TITLE/TYPE over TAG for alignment, because TAG can be broad/uncontrolled.
        bonus = 0.0
        if aligned:
            bonus += 0.25
            if c.get("kind") == "TITLE":
                bonus += 0.1
            if c.get("kind") == "TYPE":
                bonus += 0.05
        else:
            # Penalize non-aligned broad TAG rules heavily unless they cover *all* members.
            if c.get("kind") == "TAG" and float(c.get("member_coverage") or 0.0) < 1.0:
                bonus -= 0.35
            if c.get("kind") == "VENDOR":
                bonus -= 0.2
        c["score"] = round(float(c.get("member_coverage") or 0.0) + bonus, 4)

    candidates.sort(key=lambda x: (-float(x.get("score") or 0.0), -float(x.get("member_coverage") or 0.0), x.get("kind") or "", str(x.get("rule") or "")))

    # Greedy set cover over members.
    def select_to_threshold(threshold: float) -> list[dict]:
        uncovered = {p.get("handle") for p in products if p.get("handle")}
        # If handles are missing, fall back to index IDs to avoid empty uncovered set.
        if not uncovered:
            uncovered = {str(i) for i in range(len(products))}

        def product_key(p: dict, idx: int) -> str:
            h = p.get("handle")
            return h if h else str(idx)

        selected: list[dict] = []
        covered: set[str] = set()

        # Precompute matches for candidates.
        cand_matches: list[tuple[dict, set[str]]] = []
        for cand in candidates:
            r = cand.get("rule") or {}
            m: set[str] = set()
            for idx, p in enumerate(products):
                if _matches_rule(p, r):
                    m.add(product_key(p, idx))
            cand_matches.append((cand, m))

        target = int(round(threshold * len(uncovered)))
        while len(covered) < target and cand_matches:
            best_i = None
            best_gain = 0
            for i, (_c, mset) in enumerate(cand_matches):
                gain = len(mset - covered)
                if gain > best_gain:
                    best_gain = gain
                    best_i = i
            if best_i is None or best_gain == 0:
                break
            cand, mset = cand_matches.pop(best_i)
            selected.append(cand)
            covered |= mset
            # Remove fully redundant candidates quickly.
            cand_matches = [(c, ms) for (c, ms) in cand_matches if len(ms - covered) > 0]

        return selected

    def _precompute_candidate_matches() -> tuple[set[str], list[tuple[dict, set[str]]]]:
        universe = {p.get("handle") for p in products if p.get("handle")}
        if not universe:
            universe = {str(i) for i in range(len(products))}

        def product_key(p: dict, idx: int) -> str:
            h = p.get("handle")
            return h if h else str(idx)

        cand_matches: list[tuple[dict, set[str]]] = []
        for cand in candidates:
            r = cand.get("rule") or {}
            m: set[str] = set()
            for idx, p in enumerate(products):
                if _matches_rule(p, r):
                    m.add(product_key(p, idx))
            cand_matches.append((cand, m))
        return universe, cand_matches

    sel_80 = select_to_threshold(0.8)
    sel_90 = select_to_threshold(0.9)

    # If selection is single-signal, try to "upgrade" it to a safer multi-signal ruleset
    # by finding a second strong attribute and using AND logic (appliedDisjunctively=false).
    universe, cand_matches_all = _precompute_candidate_matches()

    def _best_and_pair(min_member_coverage: float) -> dict | None:
        # Only consider candidates that cover a large fraction of current members.
        eligible: list[tuple[dict, set[str]]] = []
        for cand, mset in cand_matches_all:
            try:
                cov = len(mset) / len(universe) if universe else 0.0
            except Exception:
                cov = 0.0
            if cov < min_member_coverage:
                continue
            # Prefer at least one title-aligned rule.
            eligible.append((cand, mset))

        best = None
        best_score = -1.0
        for i in range(len(eligible)):
            c1, m1 = eligible[i]
            r1 = c1.get("rule") or {}
            k1 = c1.get("kind")
            for j in range(i + 1, len(eligible)):
                c2, m2 = eligible[j]
                if c2.get("kind") == k1:
                    # Avoid same-kind duplicates when building an AND pair (often redundant).
                    continue
                inter = m1 & m2
                if not inter:
                    continue
                inter_cov = len(inter) / len(universe) if universe else 0.0
                if inter_cov < 0.8:
                    continue
                aligned1 = bool((c1.get("alignment") or {}).get("aligned"))
                aligned2 = bool((c2.get("alignment") or {}).get("aligned"))
                if not (aligned1 or aligned2):
                    continue

                # Score: prioritize intersection coverage and alignment, penalize VENDOR-only dominance.
                s = inter_cov
                if aligned1:
                    s += 0.15
                if aligned2:
                    s += 0.15
                if (c1.get("kind") == "VENDOR") ^ (c2.get("kind") == "VENDOR"):
                    s += 0.05  # vendor+something can be a useful narrowing constraint
                if c1.get("kind") == "VENDOR" and c2.get("kind") == "VENDOR":
                    s -= 0.25

                if s > best_score:
                    best_score = s
                    best = {
                        "appliedDisjunctively": False,
                        "rules": [r1, (c2.get("rule") or {})],
                        "member_coverage_intersection": round(inter_cov, 4),
                        "debug": {
                            "rule1": c1.get("rule"),
                            "rule2": c2.get("rule"),
                            "aligned": [aligned1, aligned2],
                        },
                    }
        return best

    suggested_ruleset = None
    if len(sel_80) <= 1:
        # If a single rule covers the members, it's likely too broad for auto-convert.
        # Try to propose an AND pair that keeps member coverage high while narrowing leakage risk.
        suggested_ruleset = _best_and_pair(0.6)

    if suggested_ruleset is None and len(sel_80) >= 2:
        suggested_ruleset = {"appliedDisjunctively": True, "rules": [c["rule"] for c in sel_80], "member_coverage_intersection": None}

    # Convertibility heuristic: fewer, stronger non-title rules => safer.
    reasons: list[str] = []
    breadth_80 = len(sel_80)
    breadth_90 = len(sel_90)
    top_cov = float(candidates[0]["member_coverage"]) if candidates else 0.0
    title_heavy = sum(1 for s in sel_80 if s.get("kind") == "TITLE") >= max(1, (len(sel_80) // 2))
    has_aligned = any(((s.get("alignment") or {}).get("aligned") is True) for s in sel_80)

    level = "LOW"
    if breadth_80 <= 3 and top_cov >= 0.6 and has_aligned:
        level = "HIGH"
        reasons.append("few_strong_aligned_signals_cover_members")
    elif breadth_80 <= 6 and top_cov >= 0.4 and has_aligned:
        level = "MED"
        reasons.append("moderate_aligned_signal_set_covers_members")
    else:
        reasons.append("many_or_weak_signals_needed")
    if title_heavy:
        reasons.append("title_keyword_overfit_risk")
    if not has_aligned:
        reasons.append("no_title_alignment_in_selected_rules")

    return {
        "total_members": total,
        "candidates": candidates[:40],
        "rule_breadth_estimate_80": breadth_80,
        "rule_breadth_estimate_90": breadth_90,
        "selected_rules_80": [c["rule"] for c in sel_80],
        "selected_rules_90": [c["rule"] for c in sel_90],
        "convertibility": {"level": level, "reasons": reasons},
        "collection_keywords": sorted(collection_keywords)[:50],
        "suggested_ruleSet": suggested_ruleset,
    }
