import os, json, subprocess

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

# Check all 20 collection templates for broken block references
result = subprocess.run([
    'curl', '-s',
    'https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/' + THEME + '/assets.json',
    '-H', 'X-Shopify-Access-Token: ' + TOKEN
], capture_output=True, text=True, errors='replace')
assets_data = json.loads(result.stdout).get('assets', [])

# All existing block files
blocks = [a['key'] for a in assets_data if a['key'].startswith('blocks/') and a['key'].endswith('.liquid')]
block_types = set()
for b in blocks:
    # Extract type name: blocks/group.liquid -> group
    name = b.replace('blocks/', '').replace('.liquid', '')
    block_types.add(name)

# Also check sections for block-rendering sections
sections = [a['key'] for a in assets_data if a['key'].startswith('sections/') and a['key'].endswith('.liquid')]
for s in sections:
    name = s.replace('sections/', '').replace('.liquid', '')
    block_types.add(name)

print('All valid block/section types: ' + str(len(block_types)))
print()

# Get all collection templates
collection_templates = [a['key'] for a in assets_data if 'templates/collection' in a['key']]

print('=== BLOCK REFERENCE VALIDATION ===')
broken_templates = []
for tpl in sorted(collection_templates):
    content = get_asset(tpl)
    if not content:
        continue
    try:
        parsed = json.loads(content)
    except:
        print('PARSE ERROR: ' + tpl)
        continue
    
    broken_refs = []
    for sec_id, sec_data in parsed.get('sections', {}).items():
        sec_type = sec_data.get('type', '')
        # Check section type
        if sec_type and sec_type not in block_types and not sec_type.startswith('@shopify/') and not sec_type.startswith('shopify://'):
            broken_refs.append(('SECTION', sec_id, sec_type))
        # Check blocks inside section
        for blk_id, blk_data in sec_data.get('blocks', {}).items():
            blk_type = blk_data.get('type', '')
            if blk_type and blk_type not in block_types and not blk_type.startswith('@shopify/') and not blk_type.startswith('shopify://'):
                broken_refs.append(('BLOCK', sec_id + '/' + blk_id, blk_type))
    
    if broken_refs:
        broken_templates.append((tpl, broken_refs))
        print('\nBROKEN: ' + tpl)
        for ref_type, path, ref_val in broken_refs:
            print('  [' + ref_type + '] ' + path + ' -> type: ' + ref_val)
    else:
        print('OK:     ' + tpl)

print('\n=== SUMMARY ===')
print('Broken templates: ' + str(len(broken_templates)) + ' of ' + str(len(collection_templates)))
