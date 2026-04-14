import os, requests, re, json, subprocess

TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN', '')
if not TOKEN:
    raise SystemExit('Missing SHOPIFY_ACCESS_TOKEN (set it in your environment or .env)')
THEME = '196991385938'

def get_asset(key):
    result = subprocess.run([
        'curl', '-s',
        'https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/' + THEME + '/assets.json?asset%5Bkey%5D=' + key,
        '-H', 'X-Shopify-Access-Token: ' + TOKEN
    ], capture_output=True, text=True, errors='replace')
    try:
        d = json.loads(result.stdout)
        return d.get('asset', {}).get('value', '')
    except:
        return ''

# ============================================================
# PART 1: product-card.js history.replaceState FULL CONTEXT
# ============================================================
print('=== product-card.js: history.replaceState CONTEXT ===')

pc_js = get_asset('assets/product-card.js')
lines = pc_js.split('\n')

for i, line in enumerate(lines):
    if 'replaceState' in line:
        print('Line ' + str(i+1) + ': ' + line.strip())
        start = max(0, i-10)
        end = min(len(lines), i+10)
        print('\n  Context:')
        for j in range(start, end):
            marker = '>>> ' if j == i else '    '
            print(marker + str(j+1) + ': ' + lines[j].strip()[:200])
        print('')

# ============================================================
# PART 2: Pagination nav HTML inspection (live)
# ============================================================
print('\n=== PAGINATION NAV HTML INSPECTION ===')

headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)'}
r = requests.get('https://www.bastelschachtel.at/collections/all', headers=headers, timeout=15)

nav_match = re.search(r'<nav[^>]*pagination[^>]*>(.*?)</nav>', r.text, re.DOTALL | re.IGNORECASE)
if nav_match:
    nav_content = nav_match.group()
    print('nav class=pagination found, length: ' + str(len(nav_content)))
    nav_links = re.findall(r'href=[\"\\']([^\"\\']+)[\"\\']\\]', nav_content)
    print('Links: ' + str(nav_links)[:200])

# All ?page= anchors
all_page_anchors = re.findall(r'href=[\"\\'][^\"\\']*\bpage=\b[^\"\\']*[\"\\']', r.text, re.IGNORECASE)
print('\nAll ?page= anchors: ' + str(len(all_page_anchors)))
seen = set()
for a in all_page_anchors:
    if a not in seen:
        seen.add(a)
        print('  ' + a[:150])

# ============================================================
# PART 3: main-collection.liquid paginate block
# ============================================================
print('\n=== main-collection.liquid PAGINATE TAG DEEP DIVE ===')

mc = get_asset('sections/main-collection.liquid')
lines_mc = mc.split('\n')
for i, line in enumerate(lines_mc):
    if 'paginate' in line.lower():
        start = max(0, i-3)
        end = min(len(lines_mc), i+12)
        print('Paginate reference at line ' + str(i+1) + ':')
        for j in range(start, end):
            print('  ' + str(j+1) + ': ' + lines_mc[j].strip()[:150])
        print('')

# ============================================================
# PART 4: Schema on collection page 2
# ============================================================
print('\n=== SCHEMA ON COLLECTION PAGE 2 ===')

r_p2 = requests.get('https://www.bastelschachtel.at/collections/all?page=2', headers=headers, timeout=15)
jsonld_blocks = re.findall(r'<script[^>]+type=[\"\\']application/ld\\+json[\"\\'\\'][^>]*>(.*?)</script>', r_p2.text, re.DOTALL)
print('JSON-LD blocks on page 2: ' + str(len(jsonld_blocks)))
for i, block in enumerate(jsonld_blocks):
    try:
        d = json.loads(block.strip())
        block_type = d.get('@type', 'unknown')
        if '@graph' in d:
            block_type = d['@graph'][0].get('@type', 'unknown') if d['@graph'] else 'empty-graph'
        print('  Block ' + str(i+1) + ': @type=' + str(block_type))
    except:
        print('  Block ' + str(i+1) + ': JSON parse failed')

# Also check if the schema is different on page 2
r_base2 = requests.get('https://www.bastelschachtel.at/collections/all', headers=headers, timeout=15)
jsonld_base = re.findall(r'<script[^>]+type=[\"\\']application/ld\\+json[\"\\'\\'][^>]*>(.*?)</script>', r_base2.text, re.DOTALL)
print('\nJSON-LD blocks on base page: ' + str(len(jsonld_base)))
for i, block in enumerate(jsonld_base):
    try:
        d = json.loads(block.strip())
        block_type = d.get('@type', 'unknown')
        if '@graph' in d:
            block_type = d['@graph'][0].get('@type', 'unknown') if d['@graph'] else 'empty-graph'
        print('  Block ' + str(i+1) + ': @type=' + str(block_type))
    except:
        print('  Block ' + str(i+1) + ': JSON parse failed')

# ============================================================
# PART 5: results-list.aio.min.js - check for history API
# ============================================================
print('\n=== results-list.aio.min.js - URL/history handling ===')

rl_js = get_asset('assets/results-list.aio.min.js')
print('File size: ' + str(len(rl_js)) + ' chars')

# Search for URL/history patterns
for pat in ['pushState', 'replaceState', 'page=', 'infinite', 'IntersectionObserver', 'history', 'navigate']:
    matches = re.findall('.{0,80}' + pat + '.{0,80}', rl_js, re.IGNORECASE)
    if matches:
        print('Pattern ' + repr(pat) + ': ' + str(len(matches)) + ' found')
        for m in matches[:2]:
            print('  ' + m[:150])
