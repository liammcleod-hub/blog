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

# Check product-card.js replaceState context
pc_js = get_asset('assets/product-card.js')
lines = pc_js.split('\n')

for i, line in enumerate(lines):
    if 'replaceState' in line:
        print('=== replaceState context ===')
        print('Line ' + str(i+1) + ': ' + line.strip())
        start = max(0, i-15)
        end = min(len(lines), i+15)
        for j in range(start, end):
            marker = '>>> ' if j == i else '    '
            print(marker + str(j+1) + ': ' + lines[j].strip()[:200])
        print('')

# Check results-list.aio.min.js
rl_js = get_asset('assets/results-list.aio.min.js')
print('=== results-list.aio.min.js ===')
print('File size: ' + str(len(rl_js)) + ' chars')
print('Contains pushState: ' + str('pushState' in rl_js))
print('Contains replaceState: ' + str('replaceState' in rl_js))
print('Contains history: ' + str('history' in rl_js))
print('Contains navigate: ' + str('navigate' in rl_js))

# Check live nav pagination
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://www.bastelschachtel.at/collections/all', headers=headers, timeout=15)

nav_match = re.search(r'<nav[^>]*pagination[^>]*>(.*?)</nav>', r.text, re.DOTALL | re.IGNORECASE)
if nav_match:
    print('\n=== PAGINATION NAV FOUND ===')
    print('Length: ' + str(len(nav_match.group())) + ' chars')
    # Find all page= links
    page_links = re.findall(r'href="([^"]*page=[^"]+)"', nav_match.group())
    print('Links in nav: ' + str(len(page_links)))
    for lnk in page_links[:10]:
        print('  ' + lnk)
else:
    print('\nPAGINATION NAV NOT FOUND in base HTML')

# All anchors with page=
all_page_anchors = re.findall(r'<a[^>]+href="([^"]*page=[^"]+)"', r.text, re.IGNORECASE)
print('\nAll anchor hrefs with page= in HTML: ' + str(len(all_page_anchors)))
seen = set()
for a in all_page_anchors:
    if a not in seen:
        seen.add(a)
        print('  ' + a[:150])

# JSON-LD on page 2
print('\n=== SCHEMA ON PAGE 2 ===')
r2 = requests.get('https://www.bastelschachtel.at/collections/all?page=2', headers=headers, timeout=15)
jsonld_blocks = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', r2.text, re.DOTALL)
print('JSON-LD blocks on /collections/all?page=2: ' + str(len(jsonld_blocks)))
for i, block in enumerate(jsonld_blocks):
    try:
        d = json.loads(block.strip())
        t = d.get('@type', 'unknown')
        print('  Block ' + str(i+1) + ': @type=' + str(t))
    except:
        print('  Block ' + str(i+1) + ': parse failed (' + str(len(block)) + ' chars)')

# Same for base
jsonld_base = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', r.text, re.DOTALL)
print('JSON-LD blocks on base: ' + str(len(jsonld_base)))
for i, block in enumerate(jsonld_base):
    try:
        d = json.loads(block.strip())
        t = d.get('@type', 'unknown')
        print('  Block ' + str(i+1) + ': @type=' + str(t))
    except:
        print('  Block ' + str(i+1) + ': parse failed')
