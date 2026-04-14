import os, requests, re, json, subprocess

TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN', '')
if not TOKEN:
    raise SystemExit('Missing SHOPIFY_ACCESS_TOKEN (set it in your environment or .env)')
THEME = "196991385938"

# ============================================================
# DEEP DIVE: product-card.js infinite scroll
# ============================================================
print("=== INFINITE SCROLL DEEP DIVE ===")

def get_asset(key):
    result = subprocess.run([
        "curl", "-s",
        "https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/" + THEME + "/assets.json?asset%5Bkey%5D=" + key,
        "-H", "X-Shopify-Access-Token: " + TOKEN
    ], capture_output=True, text=True, errors="replace")
    try:
        d = json.loads(result.stdout)
        return d.get("asset", {}).get("value", "")
    except:
        return ""

# Check product-card.js for URL/history/pushState behavior
pc_js = get_asset("assets/product-card.js")
print("=== product-card.js ===")
print("File size: " + str(len(pc_js)) + " chars")

# Search for pagination-related patterns
patterns = {
    "pushState": re.findall(r'.{0,100}pushState.{0,100}', pc_js),
    "replaceState": re.findall(r'.{0,100}replaceState.{0,100}', pc_js),
    "?page=": re.findall(r'.{0,100}\?page=.{0,100}', pc_js),
    "page=": re.findall(r'.{0,100}[?&]page=.{0,100}', pc_js),
    "nextUrl": re.findall(r'.{0,100}(next|nextUrl|next_url|loadMore).{0,100}', pc_js, re.IGNORECASE),
    "infinite": re.findall(r'.{0,100}infinite.{0,100}', pc_js, re.IGNORECASE),
    "history": re.findall(r'.{0,100}history.{0,100}', pc_js, re.IGNORECASE),
    "pagevisit": re.findall(r'.{0,100}(pagevisit|visited).{0,100}', pc_js, re.IGNORECASE),
}

for name, matches in patterns.items():
    if matches:
        print("\n'" + name + "' patterns found: " + str(len(matches)))
        for m in matches[:3]:
            print("  " + m[:120])

# ============================================================
# DEEP DIVE: results-list component (in main-collection.liquid)
# ============================================================
print("\n=== RESULTS-LIST COMPONENT ANALYSIS ===")

main_coll = get_asset("sections/main-collection.liquid")
print("main-collection.liquid size: " + str(len(main_coll)) + " chars")

# Look for results-list JS logic
rl_patterns = {
    "results-list": re.findall(r'results-list.{0,500}', main_coll, re.DOTALL),
    "infinite": re.findall(r'.{0,100}infinite.{0,100}', main_coll, re.IGNORECASE),
    "?page=": re.findall(r'.{0,50}\?page=.{0,50}', main_coll),
    "paginate": re.findall(r'.{0,100}paginate.{0,100}', main_coll, re.IGNORECASE),
}

for name, matches in rl_patterns.items():
    if matches:
        print("\n'" + name + "' found: " + str(len(matches)))
        for m in matches[:5]:
            print("  " + m[:150])

# Check if there's a schema for infinite scroll in main-collection
schema_match = re.search(r'\{%\s+schema\s+%}.*?\{%\s+endschema\s+%\}', main_coll, re.DOTALL)
if schema_match:
    schema = schema_match.group()
    if "infinite" in schema.lower():
        print("\nInfinite scroll config in schema:")
        for line in schema.split("\n"):
            if "infinite" in line.lower():
                print("  " + line.strip()[:120])

# ============================================================
# DEEP DIVE: Check settings for infinite_scroll in sections
# ============================================================
print("\n=== INFINITE SCROLL SETTINGS IN SECTIONS ===")

sections_with_infinite = []

for key in ["sections/main-collection.liquid", "sections/main-blog.liquid", "sections/featured-blog-posts.liquid"]:
    content = get_asset(key)
    if "infinite" in content.lower():
        lines = [(i+1, line.strip()) for i, line in enumerate(content.split("\n")) if "infinite" in line.lower()]
        print("\n" + key + ":")
        for ln, line in lines:
            print("  Line " + str(ln) + ": " + line[:150])

# ============================================================
# HREFLANG + PAGE=N TEST
# ============================================================
print("\n=== HREFLANG + PAGE=N TEST ===")

headers = {"User-Agent": "Mozilla/5.0"}

r_p2 = requests.get("https://www.bastelschachtel.at/collections/all?page=2", headers=headers, timeout=15)
r_base = requests.get("https://www.bastelschachtel.at/collections/all", headers=headers, timeout=15)

# Check hreflang on base vs page 2
hreflang_base = re.findall(r'<link[^>]+rel=["\']alternate["\'][^>]+hreflang=["\']([^"\']+)', r_base.text, re.IGNORECASE)
hreflang_p2 = re.findall(r'<link[^>]+rel=["\']alternate["\'][^>]+hreflang=["\']([^"\']+)', r_p2.text, re.IGNORECASE)
canonical_base = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', r_base.text, re.IGNORECASE)
canonical_p2 = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', r_p2.text, re.IGNORECASE)

print("hreflang on base: " + str(hreflang_base))
print("hreflang on page 2: " + str(hreflang_p2))
print("Canonical on base: " + str(canonical_base.group(1) if canonical_base else "NOT FOUND"))
print("Canonical on page 2: " + str(canonical_p2.group(1) if canonical_p2 else "NOT FOUND"))

# Check JSON-LD inLanguage on page 2
jsonld_lang = re.findall(r'"inLanguage"\s*:\s*"([^"]+)"', r_p2.text)
print("inLanguage on page 2: " + str(jsonld_lang))

# ============================================================
# CRAWLER-ONLY PAGINATION DISCOVERY TEST
# ============================================================
print("\n=== CRAWLER-ONLY PAGINATION DISCOVERY TEST ===")

r_base2 = requests.get("https://www.bastelschachtel.at/collections/all", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
r_p2_full = requests.get("https://www.bastelschachtel.at/collections/all?page=2", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)

# Check for rel="next" / rel="prev"
next_tags = re.findall(r'<link[^>]+rel=["\']([^"\']+)["\'][^>]+href=["\']([^"\']+)', r_base2.text, re.IGNORECASE)
prev_tags = re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']([^"\']+)["\']', r_base2.text, re.IGNORECASE)

print("rel=next/prev tags (as attributes): " + str(len(next_tags)))
print("href + rel=next/prev tags (as attributes): " + str(len(prev_tags)))

# Check for noscript pagination
noscript_pagination = re.findall(r'<noscript[^>]*>.*?(?:paginate|pagination|<a[^>]+page=).*?</noscript>', r_base2.text, re.DOTALL | re.IGNORECASE)
print("noscript pagination blocks: " + str(len(noscript_pagination)))

# Check for <nav class="pagination">
nav_pagination = re.findall(r'<nav[^>]+pagination[^>]*>.*?</nav>', r_base2.text, re.DOTALL | re.IGNORECASE)
print("nav pagination blocks: " + str(len(nav_pagination)))

# Check for any anchor with page= in the base HTML
all_page_anchors = re.findall(r'<a[^>]+href=["\'][^"\']*\?page=[^"\']+["\']', r_base2.text, re.IGNORECASE)
print("Anchor tags with ?page= in base HTML: " + str(len(all_page_anchors)))
for a in all_page_anchors[:5]:
    print("  " + a[:120])

# Check if pagination exists in the raw base HTML at all
pagination_html = re.findall(r'.{0,30}(?:pagination|page-[0-9]+|Seite [0-9]).{0,30}', r_base2.text, re.IGNORECASE)
print("\nPagination signals in raw base HTML: " + str(len(pagination_html)))
