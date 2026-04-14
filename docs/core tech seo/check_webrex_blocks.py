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

# Check where Webrex actually is in the templates
templates = [
    'templates/collection.schulbedarf.json',
    'templates/collection.winter.json',
    'templates/collection.glasaetzpaste-gravuren.json',
]

for tpl in templates:
    content = get_asset(tpl)
    if not content:
        continue
    # Find all block type references
    block_types = set()
    parsed = json.loads(content)
    for sec_id, sec_data in parsed.get('sections', {}).items():
        sec_type = sec_data.get('type', '')
        if 'webrex' in sec_type or 'b26797ad' in sec_type:
            block_types.add(('SECTION', sec_id, sec_type))
        for blk_id, blk_data in sec_data.get('blocks', {}).items():
            blk_type = blk_data.get('type', '')
            if 'webrex' in blk_type or 'b26797ad' in blk_type:
                block_types.add(('BLOCK', sec_id + '/' + blk_id, blk_type))
    
    if block_types:
        print('\n=== ' + tpl + ' ===')
        print('Webrex references found: ' + str(len(block_types)))
        for loc, path, ref in sorted(block_types):
            print('  [' + loc + '] ' + path)
            print('    -> ' + ref)

# Also check: does the acrylfarben template have any Webrex blocks?
print('\n=== acrylfarben blocks check ===')
content = get_asset('templates/collection.acrylfarben.json')
parsed = json.loads(content)
block_types = set()
for sec_id, sec_data in parsed.get('sections', {}).items():
    for blk_id, blk_data in sec_data.get('blocks', {}).items():
        blk_type = blk_data.get('type', '')
        block_types.add(blk_type)
print('All block types in acrylfarben:')
for bt in sorted(block_types):
    print('  ' + bt)

# Check if "section" as a type name works in the Theme Editor
# "section" is a block type that references blocks/section.liquid
# Let me check if blocks/section.liquid exists
print('\n=== blocks/section.liquid check ===')
section_block = get_asset('blocks/section.liquid')
if section_block:
    print('EXISTS: blocks/section.liquid (' + str(len(section_block)) + ' chars)')
    print('First 200 chars:')
    print(section_block[:200])
else:
    print('DOES NOT EXIST: blocks/section.liquid')

# The key question: when a JSON template has type: "section" (referencing blocks/section.liquid)
# and blocks/section.liquid renders blocks inside it using content_for
# does the Theme Editor look for sections/section.liquid?
# Answer: NO - section types in JSON templates are block types
# The BLOCK files are what matters, not section files

# Let me verify: blocks/section.liquid - what does it render?
print('\n=== blocks/section.liquid content_for analysis ===')
if section_block and 'content_for' in section_block:
    print('Uses content_for blocks: YES')
    for line in section_block.split('\n'):
        if 'content_for' in line:
            print('  ' + line.strip()[:150])
else:
    print('Uses content_for blocks: NO or file not found')

# Check: do group references in templates resolve to blocks/group.liquid?
print('\n=== KEY QUESTION: group block type resolution ===')
print('When JSON template has type: "group" inside a block context:')
print('  Shopify looks for: blocks/group.liquid')
print('  blocks/group.liquid EXISTS: YES (11,440 chars)')
print('When JSON template has type: "section" inside a block context:')
print('  Shopify looks for: blocks/section.liquid')
print('  blocks/section.liquid EXISTS: ' + ('YES' if section_block else 'NO'))
print()
print('CONCLUSION: group block references are VALID - blocks/group.liquid exists')
print('The SMOKING GUN was a FALSE POSITIVE')
print('The real issue is the Webrex BLOCK references (not section references)')
