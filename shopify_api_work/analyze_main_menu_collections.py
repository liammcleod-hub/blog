import collections
import json
import math
import pathlib
from dataclasses import dataclass


@dataclass(frozen=True)
class CohesionScore:
    href: str
    label: str
    collection_handle: str
    collection_title: str
    product_count: int
    distinct_product_types: int
    top_type: str
    top_type_share: float
    inactive_count: int
    entropy: float


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


def load_input(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    base_dir = pathlib.Path(__file__).resolve().parent
    input_path = base_dir / "out" / "main_menu_collections_products.json"
    data = load_input(input_path)

    menu_items = data.get("menu_items") or []
    generated_at = data.get("generated_at") or ""
    storefront_url = data.get("storefront_url") or ""

    product_to_collections: dict[str, set[str]] = collections.defaultdict(set)
    all_products_seen: dict[str, dict] = {}

    scores: list[CohesionScore] = []
    for entry in menu_items:
        href = entry.get("href") or ""
        label = entry.get("label") or ""
        handle = entry.get("collection_handle") or ""
        title = entry.get("collection_title") or handle
        products = entry.get("products") or []

        type_counts: dict[str, int] = collections.Counter(
            (p.get("productType") or "").strip() for p in products
        )
        status_counts: dict[str, int] = collections.Counter(
            (p.get("status") or "").strip() for p in products
        )
        inactive_count = sum(
            c for s, c in status_counts.items() if s and s.upper() != "ACTIVE"
        )

        product_count = len(products)
        distinct_types = len([t for t in type_counts.keys() if t != ""])
        top_type, top_type_count = ("", 0)
        if type_counts:
            top_type, top_type_count = max(
                type_counts.items(), key=lambda kv: (kv[1], kv[0])
            )
        top_share = (top_type_count / product_count) if product_count else 0.0
        entropy = shannon_entropy(type_counts)

        scores.append(
            CohesionScore(
                href=href,
                label=label,
                collection_handle=handle,
                collection_title=title,
                product_count=product_count,
                distinct_product_types=distinct_types,
                top_type=top_type,
                top_type_share=top_share,
                inactive_count=inactive_count,
                entropy=entropy,
            )
        )

        for p in products:
            pid = p.get("id") or p.get("handle") or p.get("title") or ""
            if not pid:
                continue
            product_to_collections[pid].add(handle)
            all_products_seen[pid] = p

    # Cohesion ranking: low top_type_share and high entropy are "less cohesive"
    def score_key(s: CohesionScore):
        return (
            s.top_type_share,
            -s.entropy,
            -s.distinct_product_types,
            -s.product_count,
            s.collection_title,
        )

    worst = sorted(scores, key=score_key)[:30]

    # Most-overlapping products (appear in many menu collections)
    overlap = sorted(
        ((len(cols), pid) for pid, cols in product_to_collections.items()),
        reverse=True,
    )
    top_overlap = overlap[:50]

    out_dir = base_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "main_menu_collections_congruency.md"

    lines: list[str] = []
    lines.append("# Main menu collections — congruency audit (heuristics)\n")
    lines.append(f"- Storefront: {storefront_url}")
    lines.append(f"- Input: `{input_path}`")
    lines.append(f"- Generated from snapshot: {generated_at}")
    lines.append(f"- Menu collections analyzed: {len(scores)}")
    lines.append(f"- Unique products across menu collections: {len(all_products_seen)}\n")

    lines.append("## Least cohesive collections (by productType mix)\n")
    lines.append(
        "Heuristic: low share of the most common `productType` + higher type entropy.\n"
    )
    for s in worst:
        lines.append(
            f"- `{s.collection_title}` (`{s.collection_handle}`): "
            f"{s.product_count} products, "
            f"{s.distinct_product_types} types, "
            f"top type `{s.top_type}` = {s.top_type_share:.0%}, "
            f"inactive={s.inactive_count}"
        )

    lines.append("\n## Products appearing in many menu collections\n")
    for n, pid in top_overlap:
        if n <= 3:
            break
        p = all_products_seen.get(pid) or {}
        lines.append(
            f"- {n} collections: {p.get('title','')} (`{p.get('handle','')}`) [{p.get('productType','')}]"
        )

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()

