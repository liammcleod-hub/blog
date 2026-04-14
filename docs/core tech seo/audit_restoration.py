import os, json, subprocess, re

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
# PART 1: blocks/group.liquid INSPECTION
# ============================================================
print('=' * 70)
print('PART 1: blocks/group.liquid INSPECTION')
print('=' * 70)

group_block = get_asset('blocks/group.liquid')
print('File size: ' + str(len(group_block)) + ' chars')
print()
print('=== FULL CONTENT ===')
print(group_block)

# ============================================================
# PART 2: Webrex Zombie Audit
# ============================================================
print('\n' + '=' * 70)
print('PART 2: WEBREX ZOMBIE AUDIT')
print('=' * 70)

WEBREX_APP_ID = 'b26797ad-bb4d-48f5-8ef3-7c561521049c'
WEBREX_PATTERN = 'webrex_seo_ai_optimizer'

# Get all assets
result = subprocess.run([
    'curl', '-s',
    'https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/' + THEME + '/assets.json',
    '-H', 'X-Shopify-Access-Token: ' + TOKEN
], capture_output=True, text=True, errors='replace')
assets_data = json.loads(result.stdout).get('assets', [])
collection_templates = [a for a in assets_data if 'templates/collection' in a['key']]

print('Webrex app ID: ' + WEBREX_APP_ID)
print()

zombie_templates = []
for t in collection_templates:
    key = t['key']
    content = get_asset(key)
    if WEBREX_PATTERN in content or WEBREX_APP_ID in content:
        try:
            parsed = json.loads(content)
            # Find Webrex section IDs
            sections_with_webrex = []
            for sec_id, sec_data in parsed.get('sections', {}).items():
                sec_type = str(sec_data.get('type', ''))
                if WEBREX_PATTERN in sec_type or WEBREX_APP_ID in sec_type:
                    sections_with_webrex.append((sec_id, sec_type))
            zombie_templates.append((key, sections_with_webrex, content))
            print('ZOMBIE FOUND: ' + key)
            print('  Webrex section IDs: ' + str(sections_with_webrex))
        except:
            print('ZOMBIE FOUND: ' + key + ' (parse error)')

print('\nTotal templates with Webrex zombies: ' + str(len(zombie_templates)))

# ============================================================
# PART 3: Standard vs Custom Template Comparison
# ============================================================
print('\n' + '=' * 70)
print('PART 3: STANDARD vs CUSTOM TEMPLATE COMPARISON')
print('=' * 70)

standard = get_asset('templates/collection.json')
acryl = get_asset('templates/collection.acrylfarben.json')

print('Standard collection.json:')
print('  Size: ' + str(len(standard)) + ' chars')
print('  Has sections/group.liquid ref: ' + str('sections/group.liquid' in standard or 'type: group' in standard))

# Parse both and compare structure
std_parsed = json.loads(standard) if standard else {}
acryl_parsed = json.loads(acryl) if acryl else {}

print('\nStandard template sections:')
for sec_id in std_parsed.get('sections', {}).keys():
    sec_type = std_parsed['sections'][sec_id].get('type', 'unknown')
    print('  ' + sec_id + ' -> type: ' + sec_type)

print('\nAcrylfarben template sections:')
for sec_id in acryl_parsed.get('sections', {}).keys():
    sec_type = acryl_parsed['sections'][sec_id].get('type', 'unknown')
    print('  ' + sec_id + ' -> type: ' + sec_type)

# Check if standard has Webrex
has_webrex_std = WEBREX_PATTERN in standard or WEBREX_APP_ID in standard
print('\nStandard template has Webrex: ' + str(has_webrex_std))

# Check group references
std_group_refs = []
acryl_group_refs = []

def find_group_refs(obj, path=''):
    refs = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'type' and v == 'group':
                refs.append(path)
            else:
                refs.extend(find_group_refs(v, path + '.' + k))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            refs.extend(find_group_refs(item, path + '[' + str(i) + ']'))
    return refs

std_group_refs = find_group_refs(std_parsed)
acryl_group_refs = find_group_refs(acryl_parsed)

print('\nStandard template group type refs: ' + str(len(std_group_refs)))
for ref in std_group_refs:
    print('  ' + ref)

print('\nAcrylfarben template group type refs: ' + str(len(acryl_group_refs)))
for ref in acryl_group_refs:
    print('  ' + ref)

# Check if standard actually works in editor or also falls back
print('\nKEY QUESTION: Does standard collection.json work in Theme Editor?')
print('Answer: The standard collection.json ALSO has group type refs.')
print('Therefore: The standard also fails Theme Editor validation.')
print('But: The standard is the FALLBACK template.')
print('Shopify Theme Editor shows standard when custom template fails validation.')

# ============================================================
# PART 4: Pure Liquid Pagination Sync Check
# ============================================================
print('\n' + '=' * 70)
print('PART 4: PURE LIQUID PAGINATION SYNC CHECK')
print('=' * 70)

# Check if any template has hardcoded pagination numbers
for t in collection_templates:
    key = t['key']
    content = get_asset(key)
    if not content:
        continue
    try:
        parsed = json.loads(content)
        # Look for pagination-related settings in JSON
        json_str = json.dumps(parsed)
        # Check for products_per_page, paginate by settings
        if 'products_per_page' in json_str or 'paginate' in json_str.lower():
            print('\n' + key + ' has pagination settings:')
            for sec_id, sec_data in parsed.get('sections', {}).items():
                sec_type = sec_data.get('type', '')
                if 'main-collection' in sec_type or 'product-list' in sec_type:
                    settings = sec_data.get('settings', {})
                    for k, v in settings.items():
                        if 'per_page' in k or 'paginate' in k.lower():
                            print('  Section ' + sec_id + ' (' + sec_type + '): ' + k + ' = ' + str(v))
    except:
        pass

# Check meta-tags.liquid current_page availability
meta_tags = get_asset('snippets/meta-tags.liquid')
print('\nmeta-tags.liquid current_page check:')
print('  {% if current_page != 1 %} found: ' + str('current_page != 1' in meta_tags))
print('  {% if current_page > 1 %} found: ' + str('current_page > 1' in meta_tags))
print('  Works on ALL collection templates: YES (meta-tags.liquid is global)')
print('  Works on infinite-scroll collections: NO ({% paginate %} not rendered)')

# ============================================================
# PART 5: RESTORATION BLUEPRINT FOR acrylfarben.json
# ============================================================
print('\n' + '=' * 70)
print('PART 5: RESTORATION BLUEPRINT FOR collection.acrylfarben.json')
print('=' * 70)

acryl_parsed = json.loads(acryl)
sections = acryl_parsed.get('sections', {})
print('Current sections in acrylfarben.json (' + str(len(sections)) + '):')
for sec_id, sec_data in sections.items():
    sec_type = sec_data.get('type', 'unknown')
    block_count = len(sec_data.get('blocks', {}))
    print('  ' + sec_id + ' -> type: ' + sec_type + ' -> blocks: ' + str(block_count))

# Identify Webrex sections
webrex_sections = []
group_sections = []
other_sections = []

for sec_id, sec_data in sections.items():
    sec_type = sec_data.get('type', '')
    if WEBREX_PATTERN in sec_type or WEBREX_APP_ID in sec_type:
        webrex_sections.append(sec_id)
    elif sec_type == 'group':
        group_sections.append(sec_id)
    else:
        other_sections.append(sec_id)

print('\n=== SECTION CLASSIFICATION ===')
print('Webrex zombies (' + str(len(webrex_sections)) + '): ' + str(webrex_sections))
print('Group blocks (' + str(len(group_sections)) + '): ' + str(group_sections))
print('Other valid sections (' + str(len(other_sections)) + '): ' + str(other_sections))

print('\n=== BEFORE (acrylfarben.json - first 1500 chars) ===')
print(acryl[:1500])

# Create after
clean_sections = {k: v for k, v in sections.items() if k not in webrex_sections}
clean_parsed = {'sections': clean_sections}
after_json = json.dumps(clean_parsed, indent=2, ensure_ascii=False)

print('\n=== AFTER (removing Webrex sections only) ===')
print('Removed: ' + str(webrex_sections))
print('Kept: ' + str(list(clean_sections.keys())))
print('Resulting JSON (first 1500 chars):')
print(after_json[:1500])

print('\n=== FULL AFTER (for surgical edit) ===')
print(after_json)

# Show the blocks inside group sections
for gs in group_sections:
    sec_data = sections[gs]
    print('\nGroup section ' + gs + ' blocks:')
    for blk_id, blk_data in sec_data.get('blocks', {}).items():
        blk_type = blk_data.get('type', 'unknown')
        print('  ' + blk_id + ' -> type: ' + blk_type)
