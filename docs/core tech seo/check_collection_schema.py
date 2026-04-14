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

# Check schema on collection page 2 - get actual block content
headers = {'User-Agent': 'Mozilla/5.0'}
r2 = requests.get('https://www.bastelschachtel.at/collections/all?page=2', headers=headers, timeout=15)
jsonld_match = re.search(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', r2.text, re.DOTALL)
if jsonld_match:
    block = jsonld_match.group(1)
    print('Block 1 content:')
    print(block[:2000])
    
# Check main-collection.liquid - infinite vs paginate logic
print('\n=== main-collection.liquid INFINITE vs PAGINATE LOGIC ===')
mc = get_asset('sections/main-collection.liquid')
lines = mc.split('\n')
for i, line in enumerate(lines):
    if 'infinite' in line.lower() or ('paginate' in line.lower() and 'section' not in line.lower()):
        print('Line ' + str(i+1) + ': ' + line.strip()[:150])

# Check if there is JS that loads more pages (fetch based)
rl_js = get_asset('assets/results-list.aio.min.js')
print('\n=== results-list.aio.min.js FULL CONTENT ===')
print(rl_js[:2000])

# Check for settings enable_infinite_scroll across sections
print('\n=== infinite_scroll setting across sections ===')
sections = ['sections/main-collection.liquid', 'sections/featured-blog-posts.liquid', 'sections/main-blog.liquid']
for s in sections:
    content = get_asset(s)
    if 'infinite_scroll' in content:
        print('File: ' + s)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'infinite_scroll' in line.lower():
                print('  Line ' + str(i+1) + ': ' + line.strip()[:150])
