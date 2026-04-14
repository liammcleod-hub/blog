import os, requests, json, re

SHOPIFY_TOKEN = "$SHOPIFY_ACCESS_TOKEN"
SHOP = "bastelschachtel.myshopify.com"

# Get total product count
r_count = requests.get(
    f"https://{SHOP}/admin/api/2024-01/products.json",
    params={"limit": 1, "fields": "id"},
    headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN},
    timeout=30
)
total_products = int(r_count.headers.get("X-Total-Count", 0))
print(f"Total products in Shopify: {total_products}")

# Get products in pages (to get handles)
all_products = []
page = 1
while True:
    r = requests.get(
        f"https://{SHOP}/admin/api/2024-01/products.json",
        params={"limit": 250, "page": page, "fields": "id,title,handle,status,published_at"},
        headers={"X-Shopify-Access-Token": SHOPIFY_TOKEN},
        timeout=30
    )
    prods = r.json().get("products", [])
    all_products.extend(prods)
    if len(prods) < 250 or len(all_products) >= total_products:
        break
    page += 1
    if page > 20:
        break

print(f"Products fetched: {len(all_products)} of {total_products}")

# Get sitemap product URLs
r1 = requests.get(
    "https://www.bastelschachtel.at/sitemap_products_1.xml?from=6664889663645&to=7739267317976",
    headers={"User-Agent": "Mozilla/5.0"}, timeout=30
)
r2 = requests.get(
    "https://www.bastelschachtel.at/sitemap_products_2.xml?from=7742089691352&to=10715674378578",
    headers={"User-Agent": "Mozilla/5.0"}, timeout=30
)

locs1 = re.findall(r"<loc>(https://www\.bastelschachtel\.at/products/([^/?]+)[^<]*)</loc>", r1.text)
locs2 = re.findall(r"<loc>(https://www\.bastelschachtel\.at/products/([^/?]+)[^<]*)</loc>", r2.text)

sitemap_urls = set()
for url, handle in (locs1 + locs2):
    sitemap_urls.add(handle)

print(f"\nIndexed product URLs in sitemap: {len(sitemap_urls)}")

# Compare
api_handles = set(p.get("handle", "") for p in all_products if p.get("handle"))
missing_handles = api_handles - sitemap_urls
in_sitemap_not_in_api = sitemap_urls - api_handles

print(f"\nIn API ({len(api_handles)} handles) but NOT in sitemap: {len(missing_handles)}")
print(f"In sitemap but NOT in API: {len(in_sitemap_not_in_api)}")

# Count statuses
draft = [p for p in all_products if p.get("status") == "draft"]
active = [p for p in all_products if p.get("status") == "active"]
archived = [p for p in all_products if p.get("status") == "archived"]
unpublished = [p for p in all_products if not p.get("published_at")]

print(f"\nStatus breakdown:")
print(f"  Draft: {len(draft)}")
print(f"  Active: {len(active)}")
print(f"  Archived: {len(archived)}")
print(f"  Unpublished (no published_at): {len(unpublished)}")

# Sample of missing products
missing_products = [p for p in all_products if p.get("handle") in missing_handles]
print(f"\nSample missing products (in API but not sitemap, first 15):")
for p in missing_products[:15]:
    print(f"  [{p.get('status')}] {p.get('title','N/A')[:60]} | handle: {p.get('handle')} | published: {p.get('published_at','NONE')}")

# Sample of in-sitemap but not in API
print(f"\nIn sitemap but NOT in API (sample):")
for h in sorted(list(in_sitemap_not_in_api))[:10]:
    print(f"  {h}")
