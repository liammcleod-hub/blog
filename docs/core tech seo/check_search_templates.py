import os, requests

# Check search, cart, account templates for no money-page risk
templates_to_check = [
    "templates/search.avada-seo.liquid",
    "templates/cart.discountyard.liquid", 
    "templates/gift_card.liquid",
    "sections/search-results.liquid",
    "sections/main-cart.liquid",
    "sections/main-404.liquid",
    "templates/page.rapid-search-results-page.liquid",
]

TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN', '')
if not TOKEN:
    raise SystemExit('Missing SHOPIFY_ACCESS_TOKEN (set it in your environment or .env)')
THEME = "196991385938"

for key in templates_to_check:
    import json, subprocess
    result = subprocess.run([
        "curl", "-s",
        f"https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/{THEME}/assets.json?asset%5Bkey%5D={key}",
        "-H", f"X-Shopify-Access-Token: {TOKEN}"
    ], capture_output=True, text=True)
    try:
        d = json.loads(result.stdout)
        v = d.get("asset", {}).get("value", "")
        has_noindex = "noindex" in v.lower()
        has_meta_robots = "meta" in v.lower() and "robots" in v.lower()
        # Check for any collection/page reference that could be a "money page"
        collection_refs = [line.strip() for line in v.split("\n") if "collection" in line.lower() and "render" in line.lower()]
        search_results = [line.strip() for line in v.split("\n") if "search" in line.lower() and "results" in line.lower()]
        
        print(f"\n=== {key} ===")
        print(f"  noindex found: {has_noindex}")
        print(f"  meta robots: {has_meta_robots}")
        print(f"  collection refs: {len(collection_refs)}")
        print(f"  search results refs: {len(search_results)}")
        if collection_refs:
            for r in collection_refs[:3]:
                print(f"    {r[:100]}")
        if search_results:
            for r in search_results[:3]:
                print(f"    {r[:100]}")
    except Exception as e:
        print(f"\n=== {key} === ERROR: {e}")
