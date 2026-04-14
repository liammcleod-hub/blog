import os, requests, re, json, subprocess

TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN', '')
if not TOKEN:
    raise SystemExit('Missing SHOPIFY_ACCESS_TOKEN (set it in your environment or .env)')
THEME = "196991385938"

# ============================================================
# PART 1: Paginate Tag Search Across All Liquid Files
# ============================================================
print("=== PART 1: PAGINATE TAG SEARCH ===")

# Get all liquid files
result = subprocess.run([
    "curl", "-s",
    "https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/196991385938/assets.json",
    "-H", "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
], capture_output=True, text=True, errors="replace")

try:
    assets_data = json.loads(result.stdout).get("assets", [])
    liquid_files = [a["key"] for a in assets_data if a["key"].endswith(".liquid")]
except:
    print("API call failed")
    liquid_files = []

print("Total liquid files: " + str(len(liquid_files)))

# Search for paginate tag in all liquid files
paginate_files = []
history_pushstate_js = []
intersection_observer_js = []

for key in liquid_files:
    result = subprocess.run([
        "curl", "-s",
        "https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/196991385938/assets.json?asset%5Bkey%5D=" + key,
        "-H", "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
    ], capture_output=True, text=True, errors="replace")
    try:
        d = json.loads(result.stdout)
        v = d.get("asset", {}).get("value", "")
        if "{% paginate" in v or "{%- paginate" in v:
            m = re.search(r'paginate\s+\w+\s+by\s+(\d+)', v)
            by_num = m.group(1) if m else "UNKNOWN"
            count = v.count("{% paginate")
            paginate_files.append((key, by_num, count))
        if "pushState" in v or "replaceState" in v:
            history_pushstate_js.append(key)
        if "IntersectionObserver" in v:
            intersection_observer_js.append(key)
    except:
        pass

print("\nFiles with {% paginate %} tag: " + str(len(paginate_files)))
for item in sorted(paginate_files):
    key, by_num, count = item
    print("  " + key + " | paginate by " + by_num + " | " + str(count) + " occurrence(s)")

# ============================================================
# PART 2: Infinite Scroll JS Detection
# ============================================================
print("\n=== PART 2: INFINITE SCROLL JS DETECTION ===")

js_files = [a["key"] for a in assets_data if a["key"].endswith(".js")]
print("Total JS files: " + str(len(js_files)))

infinite_scroll_files = []
scroll_files = []

for key in js_files:
    result = subprocess.run([
        "curl", "-s",
        "https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/196991385938/assets.json?asset%5Bkey%5D=" + key,
        "-H", "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
    ], capture_output=True, text=True, errors="replace")
    try:
        d = json.loads(result.stdout)
        v = d.get("asset", {}).get("value", "")
        v_lower = v.lower()
        if "infinite" in v_lower and ("scroll" in v_lower or "IntersectionObserver" in v):
            infinite_scroll_files.append(key)
        if "infinite" in v_lower and ".js" in key:
            scroll_files.append(key)
    except:
        pass

print("\nJS files mentioning 'infinite': " + str(len(scroll_files)))
for f in scroll_files:
    print("  " + f)

print("\nJS files with 'infinite' + 'IntersectionObserver': " + str(len(infinite_scroll_files)))
for f in infinite_scroll_files:
    print("  " + f)

print("\nJS files with 'pushState' or 'replaceState': " + str(len(history_pushstate_js)))
for f in history_pushstate_js:
    print("  " + f)

print("\nJS files with 'IntersectionObserver': " + str(len(intersection_observer_js)))
for f in intersection_observer_js:
    print("  " + f)

# ============================================================
# PART 3: Collection Template Types
# ============================================================
print("\n=== PART 3: COLLECTION TEMPLATE TYPES ===")

template_files = [k for k in liquid_files if "template" in k and "collection" in k]
print("Collection-related template files:")
for k in sorted(template_files):
    print("  " + k)

section_files = [k for k in liquid_files if "section" in k and "collection" in k]
print("\nCollection-related section files:")
for k in sorted(section_files):
    print("  " + k)

# ============================================================
# PART 4: meta-tags.liquid description block analysis
# ============================================================
print("\n=== PART 4: META-TAG GUARD VERIFICATION ===")

result = subprocess.run([
    "curl", "-s",
    "https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/196991385938/assets.json?asset%5Bkey%5D=snippets/meta-tags.liquid",
    "-H", "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
], capture_output=True, text=True, errors="replace")

try:
    d = json.loads(result.stdout)
    v = d.get("asset", {}).get("value", "")
    
    # Find the description block
    desc_match = re.search(r'\{%\s*if\s+page_description\s*%\}.*?\{%\s*endif\s*%\}', v, re.DOTALL)
    title_match = re.search(r'<title>.*?</title>', v, re.DOTALL)
    
    print("Current meta-tags.liquid description block:")
    if desc_match:
        print(desc_match.group())
    print("\nCurrent meta-tags.liquid title block:")
    if title_match:
        print(title_match.group())
        
    # Check current_page usage
    current_page_uses = [(i+1, line.strip()) for i, line in enumerate(v.split("\n")) if "current_page" in line]
    print("\ncurrent_page uses in meta-tags.liquid:")
    for ln, line in current_page_uses:
        print("  Line " + str(ln) + ": " + line[:120])
        
except Exception as e:
    print("Error: " + str(e))
