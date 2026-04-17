from __future__ import annotations


def build_collection_keywords(collection_title: str, collection_handle: str, cfg: dict | None = None) -> set[str]:
    import re

    stop = {
        "dekorieren",
        "mit",
        "und",
        "oder",
        "set",
        "sets",
        "der",
        "die",
        "das",
        "für",
        "fur",
        "the",
        "and",
        "random",
        "micro",
    }
    raw = f"{collection_title} {collection_handle}".lower()
    tokens = [t for t in re.split(r"[^a-z0-9äöüß]+", raw) if t]
    keywords = {t for t in tokens if len(t) >= 5 and t not in stop}

    stems: set[str] = set()
    suffixes = ("en", "ung", "ungen", "er", "ern", "e", "es", "s", "n")
    for k in keywords:
        if len(k) < 6:
            continue
        for suf in suffixes:
            if k.endswith(suf) and len(k) - len(suf) >= 4:
                stems.add(k[: -len(suf)])
                break
    keywords |= stems

    folded: set[str] = set()
    for k in keywords:
        folded.add(k.replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss"))
        folded.add(k.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss"))
    keywords |= folded

    if any("krakelier" in k for k in keywords) or "krakelierlack" in keywords:
        keywords |= {"krakelier", "krakelierlack", "riss", "risslack", "reisslack", "reißlack", "feinriss"}
    if "blattmetall" in keywords:
        keywords |= {"metallfolie", "metallfolien", "metallflocken", "effektfolie", "effektfolien"}
    if "modellierung" in keywords:
        keywords |= {"modellier", "modelliermasse", "modellieren", "modellierpaste"}
    if any("glasatz" in k or "glasätz" in k or "glasaetz" in k for k in keywords):
        keywords |= {"glasatzung", "glasätzung", "glasaetzung", "glasatzungspaste", "glasätzungspaste", "glasaetzungspaste"}

    verify_synonyms = (cfg or {}).get("verify_synonyms") if isinstance(cfg, dict) else None
    if isinstance(verify_synonyms, dict):
        expanded: set[str] = set()
        for k in list(keywords):
            aliases = verify_synonyms.get(k)
            if not aliases:
                continue
            if isinstance(aliases, list):
                for a in aliases:
                    if isinstance(a, str) and a.strip():
                        expanded.add(a.strip().lower())
        keywords |= expanded

    return keywords


def product_is_relevant_to_collection_title(collection_keywords: set[str], product: dict) -> bool:
    title = (product.get("title") or "").lower()
    normalized = title.replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss").replace("Ä", "a").replace("Ö", "o").replace("Ü", "u")
    normalized2 = title.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("Ä", "ae").replace("Ö", "oe").replace("Ü", "ue")
    if any(k in title for k in collection_keywords) or any(k in normalized for k in collection_keywords) or any(k in normalized2 for k in collection_keywords):
        return True

    import re
    from difflib import SequenceMatcher

    tokens = [t for t in re.split(r"[^a-z0-9äöüß]+", title) if t]
    if not tokens:
        return False

    def fold_token(t: str) -> set[str]:
        t = t.strip().lower()
        if not t:
            return set()
        return {
            t,
            t.replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss"),
            t.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss"),
        }

    folded_tokens: list[str] = []
    for tok in tokens:
        folded_tokens.extend(list(fold_token(tok)))

    def similar(a: str, b: str) -> bool:
        if a == b:
            return True
        if len(a) < 5 or len(b) < 5:
            return False
        return SequenceMatcher(None, a, b).ratio() >= 0.88

    for kw in collection_keywords:
        if not kw or len(kw) < 5:
            continue
        for tok in folded_tokens:
            if similar(kw, tok) or (kw in tok) or (tok in kw):
                return True

    return False


def build_keywords_from_rule_set(rule_set: dict | None) -> set[str]:
    rs = rule_set or {}
    rules = rs.get("rules") or []
    keywords: set[str] = set()
    for r in rules:
        cond = (r.get("condition") or "").strip().lower()
        if not cond:
            continue
        keywords.add(cond)
    return keywords


def verify_congruency(collection_title: str, collection_handle: str, products: list[dict], cfg: dict | None = None, rule_set: dict | None = None) -> dict:
    cfg = cfg or {}
    if collection_handle in set(cfg.get("verify_exempt_handles") or []):
        return {
            "passed": True,
            "total_products": len(products),
            "outliers": [],
            "outlier_ratio": 0.0,
            "keywords_used": [],
            "exempt_reason": "verify_exempt_handles",
        }

    def run_with_keywords(keywords: set[str]) -> dict:
        outliers: list[dict] = []
        for p in products:
            if not product_is_relevant_to_collection_title(keywords, p):
                outliers.append({"title": p.get("title"), "handle": p.get("handle"), "productType": p.get("productType")})
        total = len(products)
        inliers = total - len(outliers)
        outlier_ratio = (len(outliers) / total) if total else 0.0
        passed = outlier_ratio <= 0.2
        return {
            "passed": passed,
            "total_products": total,
            "inlier_products": inliers,
            "outlier_products": len(outliers),
            "outliers": outliers,
            "outlier_ratio": round(outlier_ratio, 4),
            "coverage_ratio": round((inliers / total), 4) if total else 0.0,
            "keywords_used": sorted(keywords),
        }

    umbrella = set(cfg.get("verify_umbrella_handles") or [])
    umbrella_force = set(cfg.get("verify_umbrella_force_handles") or [])
    if collection_handle in umbrella and rule_set:
        keywords = build_keywords_from_rule_set(rule_set)
        metrics = {
            "rule_count": len(rule_set.get("rules") or []),
            "appliedDisjunctively": rule_set.get("appliedDisjunctively"),
        }
        if len(keywords) > 30 and collection_handle not in umbrella_force:
            title_keywords = build_collection_keywords(collection_title, collection_handle, cfg=cfg)
            title_result = run_with_keywords(title_keywords)
            title_result["mode"] = "title"
            title_result["umbrella_ruleSet_too_broad"] = True
            title_result["umbrella_ruleSet_keywords_count"] = len(keywords)
            title_result["rule_metrics"] = metrics
            return title_result
        base = run_with_keywords(keywords)
        base["mode"] = "umbrella(ruleSet)"
        base["rule_metrics"] = metrics
        return base

    title_keywords = build_collection_keywords(collection_title, collection_handle, cfg=cfg)
    title_result = run_with_keywords(title_keywords)
    title_result["mode"] = "title"
    if rule_set:
        title_result["rule_metrics"] = {
            "rule_count": len(rule_set.get("rules") or []),
            "appliedDisjunctively": rule_set.get("appliedDisjunctively"),
        }

    if rule_set and not title_result["passed"]:
        t = (collection_title or "").lower()
        looks_umbrella = any(x in t for x in [" & ", " und ", "zubehör", "werkzeug", "material", "farben", "veredelung"])
        if looks_umbrella:
            rs_keywords = build_keywords_from_rule_set(rule_set)
            if len(rs_keywords) > 30:
                return title_result
            rs_result = run_with_keywords(rs_keywords)
            rs_result["mode"] = "umbrella(ruleSet)"
            improved = rs_result["outlier_ratio"] + 0.15 < title_result["outlier_ratio"]
            if rs_result["passed"] or improved:
                chosen = rs_result if (rs_result["passed"] or rs_result["outlier_ratio"] < title_result["outlier_ratio"]) else title_result
                chosen["umbrella_candidate"] = True
                chosen["recommend_add_to_verify_umbrella_handles"] = True
                chosen["comparison"] = {
                    "title": {"passed": title_result["passed"], "outlier_ratio": title_result["outlier_ratio"]},
                    "umbrella": {"passed": rs_result["passed"], "outlier_ratio": rs_result["outlier_ratio"]},
                }
                return chosen

    return title_result
