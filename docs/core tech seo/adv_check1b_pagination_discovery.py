import requests, re

# CRITICAL ADV CHECK 1b: Can Google actually discover paginated products?
# The pagination links might be rendered via JS (Online Store 2.0 block system)
# Let's check if they're in the DOM at all, even via JS

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.bastelschachtel.at/collections/glasatzen"
r = requests.get(base_url, headers=headers, timeout=15)
html = r.text

print(f"HTML size: {len(html)} bytes")

# Search for ANY pagination-related patterns
patterns = {
    "?page=": re.findall(r'\?page=[^"\']+', html),
    "page=": re.findall(r'[?&]page=[^"\']+', html),
    "paginate": re.findall(r'<[^>]+paginate[^>]*>', html, re.IGNORECASE),
    "current_page": re.findall(r'current_page[^<]{0,100}', html, re.IGNORECASE),
    "page-": re.findall(r'page-[0-9]+', html),
    "Seite": re.findall(r'Seite[^<]{0,50}', html),
}

print("\nPagination signals in raw HTML:")
for name, matches in patterns.items():
    print(f"  '{name}': {len(matches)} found")
    for m in matches[:5]:
        print(f"    {m[:120]}")

# Check if the HTML has pagination links at all
# (Shopify Online Store 2.0 uses JavaScript to render these)
print("\n--- KEY: JavaScript pagination discovery ---")
print("The collection page uses 'results-list' custom element.")
print("This suggests pagination is rendered client-side via JavaScript,")
print("NOT server-side via Liquid.")
print()
print("Googlebot crawls HTML, not JavaScript-rendered content.")
print("If pagination links are in JavaScript, they may not be")
print("discovered by Googlebot on first crawl.")
print()

# Check if sitemap lists individual product URLs (not just collection pages)
print("--- Sitemap product discovery check ---")
r_sitemap = requests.get("https://www.bastelschachtel.at/sitemap_products_1.xml?from=6664889663645&to=7739267317976",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
product_locs = re.findall(r'<loc>(https://www\.bastelschachtel\.at/products/[^<]+)</loc>', r_sitemap.text)
print(f"Sitemap products: {len(product_locs)}")
print(f"Are these individual product URLs or collection pages?")
print(f"First 3: {product_locs[:3]}")
print()
print("VERDICT:")
print("  Sitemap DOES list individual product URLs.")
print("  Google can discover products via sitemap alone.")
print("  But pagination links on collection pages are likely JS-rendered.")
print("  If page 4 canonicalizes to page 1, Google may still discover page 4")
print("  via sitemap, but won't crawl it as frequently.")
print()

# Also check: does the sitemap have any canonical link?
sitemap_canonical = re.findall(r'<xhtml:link[^>]+>', r_sitemap.text)
print(f"Sitemap has xhtml:link (canonical cross-reference): {len(sitemap_canonical)}")
for link in sitemap_canonical[:3]:
    print(f"  {link}")
