import requests, re

# ADV CHECK 2: Raw sitemap XML count - exact product count verification
print("=== RAW SITEMAP XML PRODUCT COUNT ===")

sitemap_urls = [
    ("products_1", "https://www.bastelschachtel.at/sitemap_products_1.xml?from=6664889663645&to=7739267317976"),
    ("products_2", "https://www.bastelschachtel.at/sitemap_products_2.xml?from=7742089691352&to=10715674378578"),
    ("collections", "https://www.bastelschachtel.at/sitemap_collections_1.xml?from=235993399453&to=676616864082"),
    ("pages", "https://www.bastelschachtel.at/sitemap_pages_1.xml?from=62424449181&to=169166733650"),
    ("blogs", "https://www.bastelschachtel.at/sitemap_blogs_1.xml"),
    ("metaobject_pages", "https://www.bastelschachtel.at/sitemap_metaobject_pages_1.xml"),
]

total_product_locs = 0
total_all_locs = 0

for name, url in sitemap_urls:
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    all_locs = re.findall(r'<loc>([^<]+)</loc>', r.text)
    product_locs = [loc for loc in all_locs if '/products/' in loc]
    collection_locs = [loc for loc in all_locs if '/collections/' in loc]
    page_locs = [loc for loc in all_locs if '/pages/' in loc and '/products/' not in loc]
    blog_locs = [loc for loc in all_locs if '/blogs/' in loc]
    total_product_locs += len(product_locs)
    total_all_locs += len(all_locs)
    print(f"{name}: {len(product_locs)} products, {len(collection_locs)} collections, {len(page_locs)} pages, {len(blog_locs)} blogs = {len(all_locs)} total")

print(f"\nGRAND TOTAL product <loc> entries: {total_product_locs}")
print(f"GRAND TOTAL all <loc> entries: {total_all_locs}")

# Verify products_2.xml HTTP status more carefully
r_p2 = requests.get("https://www.bastelschachtel.at/sitemap_products_2.xml?from=7742089691352&to=10715674378578", 
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
p2_locs = re.findall(r'<loc>([^<]+)</loc>', r_p2.text)
print(f"\nproducts_2.xml verification: HTTP {r_p2.status_code}, {len(p2_locs)} locs found")

# Cross-check: Count unique product handles across both product sitemaps
r_p1 = requests.get("https://www.bastelschachtel.at/sitemap_products_1.xml?from=6664889663645&to=7739267317976",
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
r_p2 = requests.get("https://www.bastelschachtel.at/sitemap_products_2.xml?from=7742089691352&to=10715674378578",
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=30)

p1_handles = set(re.findall(r'/products/([^/?]+)', r_p1.text))
p2_handles = set(re.findall(r'/products/([^/?]+)', r_p2.text))
all_handles = p1_handles | p2_handles
overlap = p1_handles & p2_handles

print(f"\nSitemap overlap check:")
print(f"  sitemap_1 unique handles: {len(p1_handles)}")
print(f"  sitemap_2 unique handles: {len(p2_handles)}")
print(f"  Overlap (duplicates): {len(overlap)}")
print(f"  Combined unique: {len(all_handles)}")
print(f"  Combined + duplicates: {len(p1_handles) + len(p2_handles)}")

print(f"\n  VERIFIED: {len(all_handles)} unique product URLs in sitemap")

# Also check if sitemap has any non-product but /products/ URL patterns
print(f"\nSample product handles from sitemap_1 (first 10):")
for h in sorted(list(p1_handles))[:10]:
    print(f"  {h}")

print(f"\nSample product handles from sitemap_2 (first 10):")
for h in sorted(list(p2_handles))[:10]:
    print(f"  {h}")
