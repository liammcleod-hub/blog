import collections
import json
import math
import pathlib
import re
from dataclasses import dataclass


OUT_DIR = pathlib.Path(__file__).resolve().parent / "out"
INPUT_JSON = OUT_DIR / "menu_MAIN_collections_products.json"
OUTPUT_MD = OUT_DIR / "menu_MAIN_KISS_audit.md"

COLLECTION_OVERRIDES: dict[str, dict] = {
    # User confirmed: Gelpaste should NOT include Schablonen etc.
    # Treat as "gel media/paste" only.
    "gelpaste-389": {
        "expected_product_types": {"Holzlasur/ Gel"},
        "required_keywords": {"gel"},
        "recommendation_keywords": {"gel"},
        "type_strict_recommendations": False,
    },
}

PRODUCTTYPE_ROUTING: dict[str, list[str]] = {
    # "Always logical" routing targets (primary first).
    "Schablonen": ["schablonen"],
    "Acrylfarben": ["acryl-farben", "acrylfarbe-matt", "acrylfarbe-glnzend-358", "acrylfarbe-metallic-365"],
    "Wachspasten/ Antikpasten/ Set": ["antikfarben-und-antikpasten", "wachspasten", "metallic-wachspaste"],
    "Bastelzubehör": ["zubehor-werkzeuge-1", "pinsel"],
    "Schere": ["bastelscheren"],
}


STOPWORDS = {
    "und",
    "oder",
    "fur",
    "für",
    "mit",
    "zum",
    "zur",
    "die",
    "der",
    "das",
    "ein",
    "eine",
    "im",
    "in",
    "am",
    "an",
    "des",
    "den",
    "aus",
    "von",
    "auf",
    "bei",
    "als",
    "ohne",
    "nicht",
    "nur",
    "mehr",
    "set",
    "sets",
}


def normalize_text(value: str) -> str:
    v = (value or "").lower()
    v = (
        v.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
        .replace("&", " ")
    )
    v = re.sub(r"[^a-z0-9\s\-_/]", " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v


def tokenize(value: str) -> list[str]:
    v = normalize_text(value)
    raw = re.split(r"[\s\-_\/]+", v)
    toks = []
    for t in raw:
        t = t.strip()
        if not t or t in STOPWORDS:
            continue
        if len(t) < 3:
            continue
        toks.append(t)

    # very-light stemming for common plurals (helps e.g. klebepistolen -> klebepistole)
    out: list[str] = []
    seen: set[str] = set()
    for t in toks:
        variants = [t]
        if t.endswith("en") and len(t) >= 5:
            variants.append(t[:-2])
        if t.endswith("n") and len(t) >= 4:
            variants.append(t[:-1])
        if t.endswith("e") and len(t) >= 4:
            variants.append(t[:-1])
        if t.endswith("s") and len(t) >= 4:
            variants.append(t[:-1])
        for vv in variants:
            if vv in STOPWORDS or len(vv) < 3:
                continue
            if vv not in seen:
                seen.add(vv)
                out.append(vv)
    return out


def keyword_match(tokens: list[str], text: str) -> tuple[bool, int]:
    if not tokens:
        return False, 0
    hay = normalize_text(text)
    hay_words = set(hay.split())
    hits = 0
    for t in tokens:
        if not t:
            continue
        # Avoid noisy substring matches for very short tokens (e.g. "gel" matching "kugel").
        if len(t) <= 3:
            if t in hay_words:
                hits += 1
        else:
            if t in hay:
                hits += 1
    return hits > 0, hits


def product_text(product: dict) -> str:
    tags = " ".join(product.get("tags") or [])
    return f"{product.get('title','')} {product.get('handle','')} {tags}"


def top_n_product_types(products: list[dict], n: int = 3) -> list[tuple[str, int]]:
    counter = collections.Counter((p.get("productType") or "").strip() for p in products)
    counter.pop("", None)
    return counter.most_common(n)


def good_vs_outlier(
    products: list[dict],
    expected_types: set[str],
    collection_tokens: list[str],
) -> tuple[list[dict], list[dict]]:
    good: list[dict] = []
    outliers: list[dict] = []
    for p in products:
        ptype = (p.get("productType") or "").strip()
        matches_kw, _ = keyword_match(collection_tokens, product_text(p))
        if (ptype in expected_types) or matches_kw:
            good.append(p)
        else:
            outliers.append(p)
    return good, outliers


def good_vs_outlier_with_required_keywords(
    products: list[dict],
    expected_types: set[str],
    collection_tokens: list[str],
    required_keywords: set[str],
) -> tuple[list[dict], list[dict]]:
    """
    Like good_vs_outlier, but requires at least one keyword hit for "good".
    This prevents broad productTypes from letting unrelated items slip in.
    """
    good: list[dict] = []
    outliers: list[dict] = []
    for p in products:
        ptext = product_text(p)
        ptype = (p.get("productType") or "").strip()
        matches_kw, _ = keyword_match(collection_tokens, ptext)
        meets_required = True
        if required_keywords:
            meets_required, _ = keyword_match(sorted(required_keywords), ptext)
        if meets_required and ((ptype in expected_types) or matches_kw):
            good.append(p)
        else:
            outliers.append(p)
    return good, outliers


def unique_products_across_menu(menu_items: list[dict]) -> dict[str, dict]:
    seen: dict[str, dict] = {}
    for e in menu_items:
        for p in e.get("products") or []:
            pid = p.get("id") or p.get("handle") or ""
            if not pid:
                continue
            seen[pid] = p
    return seen


def product_memberships(menu_items: list[dict]) -> dict[str, set[str]]:
    memberships: dict[str, set[str]] = collections.defaultdict(set)
    for e in menu_items:
        handle = e.get("collection_handle") or ""
        for p in e.get("products") or []:
            pid = p.get("id") or p.get("handle") or ""
            if pid:
                memberships[pid].add(handle)
    return memberships


def shannon_entropy(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    ent = 0.0
    for c in counts.values():
        if c <= 0:
            continue
        p = c / total
        ent -= p * math.log2(p)
    return ent


def collection_broadness(products: list[dict]) -> tuple[int, float]:
    type_counts = collections.Counter((p.get("productType") or "").strip() for p in products)
    type_counts.pop("", None)
    distinct = len(type_counts)
    total = len(products)
    top3 = type_counts.most_common(3)
    top3_share = (sum(c for _, c in top3) / total) if total else 0.0
    return distinct, top3_share


@dataclass(frozen=True)
class Slice:
    label: str
    href_original: str
    slug: str


def extract_slices_for_parent(menu_items: list[dict], parent_handle: str) -> list[Slice]:
    slices: list[Slice] = []
    for e in menu_items:
        if (e.get("collection_handle") or "") != parent_handle:
            continue
        href_original = e.get("href_original") or e.get("href") or ""
        parts = [p for p in href_original.split("/") if p]
        # /collections/<parent>/<slice>
        if len(parts) >= 3 and parts[0] == "collections" and parts[1] == parent_handle:
            slug = parts[2]
            slices.append(
                Slice(label=e.get("label") or slug, href_original=href_original, slug=slug)
            )
    # de-dupe by slug preserving order
    out: list[Slice] = []
    seen: set[str] = set()
    for s in slices:
        if s.slug in seen:
            continue
        seen.add(s.slug)
        out.append(s)
    return out


def rank_recommendations(
    candidates: list[dict],
    tokens: list[str],
    expected_types: set[str],
    already_in: set[str],
    limit: int | None = 15,
) -> list[dict]:
    scored: list[tuple[float, dict]] = []
    for p in candidates:
        pid = p.get("id") or p.get("handle") or ""
        if not pid or pid in already_in:
            continue
        ptype = (p.get("productType") or "").strip()
        if expected_types and ptype not in expected_types:
            continue
        matches, hit_count = keyword_match(tokens, product_text(p))
        if not matches:
            continue
        score = float(hit_count)
        scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], (x[1].get("title") or "").lower()))
    if limit is None:
        return [p for _, p in scored]
    return [p for _, p in scored[:limit]]


def rank_slice_recommendations(
    candidates: list[dict],
    tokens: list[str],
    affinity_types: set[str],
    already_in: set[str],
) -> list[dict]:
    """
    Slice recommendations should be comprehensive.
    We include every product that matches the slice keywords, then rank:
      1) matches affinity productType (if known)
      2) higher keyword hit count
      3) title
    """
    scored: list[tuple[tuple[int, int, str], dict]] = []
    for p in candidates:
        pid = p.get("id") or p.get("handle") or ""
        if not pid or pid in already_in:
            continue
        matches, hit_count = keyword_match(tokens, product_text(p))
        if not matches:
            continue
        ptype = (p.get("productType") or "").strip()
        type_match = 1 if (ptype and ptype in affinity_types) else 0
        title = (p.get("title") or "").lower()
        scored.append(((type_match, hit_count, title), p))
    scored.sort(key=lambda x: (-x[0][0], -x[0][1], x[0][2]))
    return [p for _, p in scored]


def recommend_move_targets(
    product: dict,
    current_collection_handle: str,
    memberships: dict[str, set[str]],
    title_by_collection: dict[str, str],
    expected_types_by_collection: dict[str, set[str]],
    tokens_by_collection: dict[str, list[str]],
    limit: int = 3,
) -> list[str]:
    """
    Suggest where an outlier product should go (within MENU=MAIN collections).

    Priority:
      1) Collections the product already appears in (other than current)
      2) Best-fit collections by productType + keyword overlap
    """
    pid = product.get("id") or product.get("handle") or ""
    ptype = (product.get("productType") or "").strip()
    text = product_text(product)

    already = sorted((memberships.get(pid) or set()) - {current_collection_handle})
    # If we have an explicit routing rule for the productType, we strictly apply it
    # (to avoid nonsensical cross-family suggestions).
    routed = PRODUCTTYPE_ROUTING.get(ptype) or []
    if routed:
        targets = []
        for h in routed:
            if h in title_by_collection and h != current_collection_handle:
                targets.append(h)
        # If product already exists elsewhere, keep only logical routed subset (if any overlap),
        # otherwise still prefer routed.
        if already:
            overlap = [h for h in already if h in targets]
            if overlap:
                return overlap[:limit]
        return targets[:limit]

    if already:
        return already[:limit]

    # Keyword-based specializations (only within the same logical family)
    if ptype == "Bastelzubehör":
        if ("pinsel" in normalize_text(text)) and ("pinsel" in title_by_collection):
            return ["pinsel"][:limit]

    candidates: list[tuple[tuple[int, int, int, str], str]] = []
    for handle, exp_types in expected_types_by_collection.items():
        if handle == current_collection_handle:
            continue
        toks = tokens_by_collection.get(handle, [])
        kw_ok, kw_hits = keyword_match(toks, text)
        type_ok = 1 if (ptype and ptype in exp_types) else 0
        if not kw_ok and not type_ok:
            continue

        specificity = -len(exp_types) if exp_types else 0
        title = (title_by_collection.get(handle, handle) or handle).lower()
        key = (type_ok, kw_hits, specificity, title)
        candidates.append((key, handle))

    candidates.sort(key=lambda x: (-x[0][0], -x[0][1], -x[0][2], x[0][3]))
    return [h for _, h in candidates[:limit]]


def main():
    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    menu_items = data.get("menu_items") or []
    generated_at = data.get("generated_at") or ""
    store_url = data.get("storefront_url") or ""

    all_products = unique_products_across_menu(menu_items)
    memberships = product_memberships(menu_items)

    # Choose canonical product list per collection handle (largest list)
    products_by_collection: dict[str, list[dict]] = {}
    title_by_collection: dict[str, str] = {}
    for e in menu_items:
        handle = e.get("collection_handle") or ""
        if not handle:
            continue
        products = e.get("products") or []
        if (handle not in products_by_collection) or (
            len(products) > len(products_by_collection[handle])
        ):
            products_by_collection[handle] = products
            title_by_collection[handle] = e.get("collection_title") or handle

    # Build collection tokens (title + handle)
    tokens_by_collection: dict[str, list[str]] = {}
    for handle, title in title_by_collection.items():
        toks = tokenize(title) + tokenize(handle)
        tokens_by_collection[handle] = list(dict.fromkeys(toks))  # stable unique

    # Apply overrides to tokens (required/recommendation keywords should count as intent tokens)
    for handle, override in COLLECTION_OVERRIDES.items():
        if handle not in tokens_by_collection:
            continue
        extra = list(override.get("required_keywords") or []) + list(
            override.get("recommendation_keywords") or []
        )
        if extra:
            tokens_by_collection[handle] = list(
                dict.fromkeys(tokens_by_collection[handle] + sorted(set(extra)))
            )

    expected_types_by_collection: dict[str, set[str]] = {}
    for handle, products in products_by_collection.items():
        override = COLLECTION_OVERRIDES.get(handle) or {}
        if override.get("expected_product_types") is not None:
            expected_types_by_collection[handle] = set(override["expected_product_types"])
        else:
            expected_types_by_collection[handle] = {t for t, _ in top_n_product_types(products, n=3)}

    def include_collection(handle: str, products: list[dict]) -> tuple[bool, int, int]:
        expected = expected_types_by_collection.get(handle) or set()
        override = COLLECTION_OVERRIDES.get(handle) or {}
        required = set(override.get("required_keywords") or set())
        if required:
            good, outliers = good_vs_outlier_with_required_keywords(
                products, expected, tokens_by_collection.get(handle, []), required
            )
        else:
            good, outliers = good_vs_outlier(products, expected, tokens_by_collection.get(handle, []))
        total = len(products)
        out_count = len(outliers)
        if total == 0:
            return True, out_count, total
        if total <= 20:
            return out_count >= 2, out_count, total
        # for larger collections, require at least 5 outliers AND >= 8%
        return (out_count >= 5 and (out_count / total) >= 0.08), out_count, total

    # Special collection
    parent_tools_handle = "zubehor-werkzeuge-1"
    tools_slices = extract_slices_for_parent(menu_items, parent_tools_handle)
    slice_tokens_map: dict[str, list[str]] = {}
    for s in tools_slices:
        toks = tokenize(s.label) + tokenize(s.slug)
        slice_tokens_map[s.slug] = list(dict.fromkeys(toks))

    # For slice affinity, look at all products across MENU that match slice keywords
    slice_affinity_types: dict[str, set[str]] = {}
    for slug, toks in slice_tokens_map.items():
        matched = []
        for p in all_products.values():
            ok, _ = keyword_match(toks, product_text(p))
            if ok:
                matched.append(p)
        top3 = {t for t, _ in top_n_product_types(matched, n=3)}
        slice_affinity_types[slug] = top3

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    # Keep doc minimal: only incongruent collections (plus zubehor special)
    lines.append("# MENU=MAIN — KISS collections audit\n")
    lines.append(f"- Snapshot: {generated_at}")
    lines.append(f"- Storefront: {store_url}\n")

    # Parent tools collection: always include (user request)
    parent_products = products_by_collection.get(parent_tools_handle, [])
    parent_title = title_by_collection.get(parent_tools_handle, parent_tools_handle)
    parent_expected = {t for t, _ in top_n_product_types(parent_products, n=3)}
    parent_distinct, parent_top3_share = collection_broadness(parent_products)

    # Parent: define tool tokens = union of slice tokens (plus its own)
    tool_union_tokens = list(
        dict.fromkeys(
            (tokens_by_collection.get(parent_tools_handle, []))
            + [t for toks in slice_tokens_map.values() for t in toks]
        )
    )

    parent_good: list[dict] = []
    parent_outliers: list[dict] = []
    for p in parent_products:
        ptype = (p.get("productType") or "").strip()
        ok_kw, _ = keyword_match(tool_union_tokens, product_text(p))
        if ptype in parent_expected or ok_kw:
            parent_good.append(p)
        else:
            parent_outliers.append(p)

    # Priority order (highest impact → lowest), for collections that appear in this doc
    priority_rows: list[tuple[int, float, int, str, str]] = []
    for handle, products in products_by_collection.items():
        if handle == parent_tools_handle:
            continue
        include, out_count, total = include_collection(handle, products)
        if not include or total == 0:
            continue
        priority_rows.append(
            (
                out_count,
                out_count / total,
                total,
                title_by_collection.get(handle, handle),
                handle,
            )
        )
    if parent_products:
        priority_rows.append(
            (
                len(parent_outliers),
                (len(parent_outliers) / len(parent_products)) if parent_products else 0.0,
                len(parent_products),
                parent_title,
                parent_tools_handle,
            )
        )
    priority_rows.sort(key=lambda r: (-r[0], -r[1], -r[2], r[3].lower()))
    if priority_rows:
        lines.append("## Priority order (highest impact → lowest)\n")
        for idx, (out_count, ratio, total, title, handle) in enumerate(priority_rows, start=1):
            lines.append(f"{idx}. `{title}` (`{handle}`) — needs amending: {out_count}/{total} ({ratio:.0%})")
        lines.append("")

    lines.append(f"## {parent_title} (`{parent_tools_handle}`)\n")
    lines.append(f"- Still good: {len(parent_good)} products")
    lines.append(f"- Needs amending: {len(parent_outliers)} products")
    lines.append(
        f"- Expected `productType` (top 3): {', '.join(sorted(parent_expected)) or '(none)'}"
    )
    lines.append(
        f"- Broadness note: {parent_distinct} types, top-3 share={parent_top3_share:.0%}\n"
    )

    if parent_outliers:
        lines.append("### Needs amending\n")
        for p in parent_outliers[:30]:
            move_targets = recommend_move_targets(
                p,
                current_collection_handle=parent_tools_handle,
                memberships=memberships,
                title_by_collection=title_by_collection,
                expected_types_by_collection=expected_types_by_collection,
                tokens_by_collection=tokens_by_collection,
                limit=3,
            )
            move_hint = ""
            if move_targets:
                pretty = ", ".join(
                    f"`{title_by_collection.get(h, h)}` ({h})" for h in move_targets
                )
                move_hint = f" -> Move to: {pretty}"
            lines.append(
                f"- {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
                + move_hint
            )
        if len(parent_outliers) > 30:
            lines.append(f"- … and {len(parent_outliers) - 30} more")
        lines.append("")

    # Parent recommendations: items matching tool tokens but missing from parent (usually none)
    parent_already = {p.get("id") or p.get("handle") or "" for p in parent_products}
    parent_recs = rank_recommendations(
        list(all_products.values()),
        tool_union_tokens,
        expected_types=parent_expected,
        already_in=parent_already,
        limit=15,
    )
    lines.append("### What should be in it (recommendations)\n")
    if parent_recs:
        for p in parent_recs:
            lines.append(
                f"- {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
            )
    else:
        lines.append("- (No obvious missing products found; main work is moving outliers out and/or splitting into child slices.)")
    lines.append("")

    # Slices: include all slices (user request), but keep each minimal
    if tools_slices:
        lines.append("### Child slices (intended sub-categories)\n")
        for s in tools_slices:
            toks = slice_tokens_map.get(s.slug, [])
            affinity = slice_affinity_types.get(s.slug, set())

            in_parent = []
            for p in parent_products:
                ok, _ = keyword_match(toks, product_text(p))
                if ok:
                    in_parent.append(p)

            still_good = []
            needs_amending = []
            for p in in_parent:
                ptype = (p.get("productType") or "").strip()
                if affinity and ptype in affinity:
                    still_good.append(p)
                else:
                    # if affinity empty (no global matches), we treat as needs-amending
                    needs_amending.append(p)

            lines.append(f"#### {s.label} (`{s.href_original}`)")
            lines.append(f"- Still good: {len(still_good)}")
            lines.append(f"- Needs amending: {len(needs_amending)}")
            lines.append(
                f"- Expected `productType` (affinity top 3): {', '.join(sorted(affinity)) or '(none)'}"
            )

            # Recommendations: products in catalog that match slice keywords & affinity
            already = {p.get('id') or p.get('handle') or '' for p in in_parent}
            recs = rank_slice_recommendations(
                list(all_products.values()),
                toks,
                affinity_types=affinity,
                already_in=already,
            )
            if len(in_parent) == 0:
                lines.append("- Needs amending: currently matches 0 products by keyword\n")
            else:
                lines.append("")
                if needs_amending:
                    lines.append("  - Needs amending (examples):")
                    for p in needs_amending[:10]:
                        move_targets = recommend_move_targets(
                            p,
                            current_collection_handle=parent_tools_handle,
                            memberships=memberships,
                            title_by_collection=title_by_collection,
                            expected_types_by_collection=expected_types_by_collection,
                            tokens_by_collection=tokens_by_collection,
                            limit=3,
                        )
                        move_hint = ""
                        if move_targets:
                            pretty = ", ".join(
                                f"`{title_by_collection.get(h, h)}` ({h})"
                                for h in move_targets
                            )
                            move_hint = f" -> Move to: {pretty}"
                        lines.append(
                            f"    - {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
                            + move_hint
                        )
            lines.append("")
            if recs:
                lines.append("  - What should be in it (recommendations):")
                for p in recs:
                    lines.append(
                        f"    - {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
                    )
                lines.append("")
            else:
                lines.append("  - What should be in it (recommendations): (no clear candidates found)")
                lines.append("")

    # Other collections: only include incongruent ones
    other_handles = sorted(h for h in products_by_collection.keys() if h != parent_tools_handle)
    for handle in other_handles:
        products = products_by_collection.get(handle, [])
        include, out_count, total = include_collection(handle, products)
        if not include:
            continue

        title = title_by_collection.get(handle, handle)
        expected = expected_types_by_collection.get(handle) or set()
        override = COLLECTION_OVERRIDES.get(handle) or {}
        required = set(override.get("required_keywords") or set())
        if required:
            good, outliers = good_vs_outlier_with_required_keywords(
                products, expected, tokens_by_collection.get(handle, []), required
            )
        else:
            good, outliers = good_vs_outlier(products, expected, tokens_by_collection.get(handle, []))

        already_ids = {p.get("id") or p.get("handle") or "" for p in products}
        recommendation_tokens = tokens_by_collection.get(handle, [])
        type_strict = True
        if override:
            rec_kw = set(override.get("recommendation_keywords") or set())
            if rec_kw:
                recommendation_tokens = list(dict.fromkeys(recommendation_tokens + sorted(rec_kw)))
            type_strict = bool(override.get("type_strict_recommendations", True))
        recs = rank_recommendations(
            list(all_products.values()),
            recommendation_tokens,
            expected if type_strict else set(),
            already_in=already_ids,
            limit=15,
        )

        lines.append(f"\n## {title} (`{handle}`)\n")
        lines.append(f"- Still good: {len(good)} products")
        lines.append(f"- Needs amending: {len(outliers)} products")
        lines.append(f"- Expected `productType` (top 3): {', '.join(sorted(expected)) or '(none)'}\n")

        if outliers:
            lines.append("### Needs amending\n")
            for p in outliers[:30]:
                move_targets = recommend_move_targets(
                    p,
                    current_collection_handle=handle,
                    memberships=memberships,
                    title_by_collection=title_by_collection,
                    expected_types_by_collection=expected_types_by_collection,
                    tokens_by_collection=tokens_by_collection,
                    limit=3,
                )
                move_hint = ""
                if move_targets:
                    pretty = ", ".join(
                        f"`{title_by_collection.get(h, h)}` ({h})" for h in move_targets
                    )
                    move_hint = f" -> Move to: {pretty}"
                lines.append(
                    f"- {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
                    + move_hint
                )
            if len(outliers) > 30:
                lines.append(f"- … and {len(outliers) - 30} more")
            lines.append("")

        if recs:
            lines.append("### What should be in it (recommendations)\n")
            for p in recs:
                lines.append(
                    f"- {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
                )
            lines.append("")
        else:
            lines.append("### What should be in it (recommendations)\n")
            lines.append("- (No clear candidates found via keyword+top-3-type heuristic; this one likely needs a manual rule.)\n")

    OUTPUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(OUTPUT_MD))


if __name__ == "__main__":
    main()
