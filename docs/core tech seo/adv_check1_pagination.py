import requests, re

# ADV CHECK 1: Pagination canonical behavior analysis
# Test: Will Google still crawl/see products on a paginated page if it canonicalizes to base?

headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

print("=== PAGINATION CANONICAL BEHAVIOR TEST ===")

# Test collection with known pagination
collection = "glasatzen"  # Has products
base_url = f"https://www.bastelschachtel.at/collections/{collection}"
r_base = requests.get(base_url, headers=headers, timeout=15)

# Count products on base page
products_base = re.findall(r'/products/[^/?]+', r_base.text)
unique_products_base = set(re.findall(r'/products/([^/?]+)', r_base.text))
print(f"Base page products (unique): {len(unique_products_base)}")

# Check if products on base page have links to page 2
page2_canonical = re.search(r'<link[^>]+rel=[\"\']canonical[\"\'][^>]+href=[\"\']([^"\']+)[\"\']', r_base.text, re.IGNORECASE)
print(f"Base canonical: {page2_canonical.group(1) if page2_canonical else 'NOT FOUND'}")

# Page 2 analysis
r_p2 = requests.get(f"{base_url}?page=2", headers=headers, timeout=15)
p2_canonical = re.search(r'<link[^>]+rel=[\"\']canonical[\"\'][^>]+href=[\"\']([^"\']+)[\"\']', r_p2.text, re.IGNORECASE)
p2_desc = re.search(r'<meta[^>]+name=[\"\']description[\"\'][^>]+content=[\"\']([^\"\']+)', r_p2.text, re.IGNORECASE)
print(f"Page 2 canonical: {p2_canonical.group(1) if p2_canonical else 'NOT FOUND'}")
print(f"Page 2 description: {p2_desc.group(1)[:80] if p2_desc else 'NOT FOUND'}...")

# KEY TEST: Do pagination links exist on the base page?
# These tell Google where to find page 2
pagination_links = re.findall(r'href=["\']([^"\']*page=[^"\']+)["\']', r_base.text)
print(f"\nPagination links found on base page: {len(pagination_links)}")
for pl in pagination_links[:5]:
    print(f"  {pl}")

# The critical question: if page 4 canonicalizes to page 1,
# but page 4 doesn't have a link from page 1,
# does Google know page 4 exists?
# Let's check how many page links the base page shows
print(f"\nAll 'page=' links on base page:")
all_page_links = set([m.group(1) for m in re.finditer(r'href=["\']([^"\']*page=[^"\']+)["\']', r_base.text)])
for pl in sorted(all_page_links):
    print(f"  {pl}")

print("\n=== KEY FINDING ===")
print("If base page has no link to page N, and page N canonicalizes to base,")
print("Google may never discover page N even with sitemap.")
print("Sitemap helps but doesn't guarantee crawling.")
print()
print("Sitemap vs internal links for discovery:")
print("- Sitemap: Google KNOWS about the URL but may not crawl it frequently")
print("- Internal links: Google WILL crawl if it finds the link")
print()
print("If page 4 has no incoming links from any crawled page,")
print("and it canonicalizes to page 1, Google may treat it as:")
print("  1. Known but 'duplicate' — deprioritized")
print("  2. Rarely revisited — may miss product updates")
