import json, subprocess, re, os

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

def get_asset_meta(key):
    result = subprocess.run([
        'curl', '-s',
        'https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/' + THEME + '/assets.json?asset%5Bkey%5D=' + key,
        '-H', 'X-Shopify-Access-Token: ' + TOKEN
    ], capture_output=True, text=True, errors='replace')
    try:
        d = json.loads(result.stdout)
        return d.get('asset', {})
    except:
        return {}

# ============================================================
# PART 1: JSON SYNTAX FORENSIC â€” All collection templates
# ============================================================
print('=' * 70)
print('PART 1: JSON SYNTAX FORENSIC')
print('=' * 70)

# Get all collection templates
result = subprocess.run([
    'curl', '-s',
    'https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/' + THEME + '/assets.json',
    '-H', 'X-Shopify-Access-Token: ' + TOKEN
], capture_output=True, text=True, errors='replace')
assets_data = json.loads(result.stdout).get('assets', [])

collection_templates = [a for a in assets_data if 'templates/collection' in a['key']]
print('Collection templates found: ' + str(len(collection_templates)))
for t in sorted(collection_templates, key=lambda x: x['key']):
    print('  ' + t['key'])

# Validate each one
print('\n--- JSON Validation Results ---')
broken_templates = []
for t in collection_templates:
    key = t['key']
    content = get_asset(key)
    if not content:
        print('EMPTY: ' + key)
        broken_templates.append((key, 'EMPTY'))
        continue
    try:
        parsed = json.loads(content)
        print('VALID: ' + key + ' (' + str(len(content)) + ' bytes)')
    except json.JSONDecodeError as e:
        print('BROKEN: ' + key + ' â€” ' + str(e))
        broken_templates.append((key, str(e)))
        # Show the problematic area
        lines = content.split('\n')
        error_line = e.lineno - 1 if e.lineno else 0
        start = max(0, error_line - 3)
        end = min(len(lines), error_line + 3)
        print('  Error context:')
        for i in range(start, end):
            marker = '>>> ' if i == error_line else '    '
            print('  ' + marker + 'Line ' + str(i+1) + ': ' + lines[i][:120])

# ============================================================
# PART 2: SECTION DEPENDENCY CHECK
# ============================================================
print('\n' + '=' * 70)
print('PART 2: SECTION DEPENDENCY CHECK')
print('=' * 70)

# Get all section files
sections = [a['key'] for a in assets_data if a['key'].startswith('sections/') and a['key'].endswith('.liquid')]
existing_sections = set(sections)
print('Total section files: ' + str(len(sections)))

# For each broken/custom template, extract referenced sections
for t in collection_templates:
    key = t['key']
    content = get_asset(key)
    if not content:
        continue
    try:
        parsed = json.loads(content)
        # Find all section references
        section_refs = []
        def find_sections(obj, path=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == 'type' and isinstance(v, str) and 'section' not in v:
                        section_refs.append(v)
                    elif k == 'type' and v.startswith('@shopify/'):
                        pass  # skip @shopify sections
                    else:
                        find_sections(v, path + '.' + k)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_sections(item, path + '[' + str(i) + ']')
        find_sections(parsed)
        
        if section_refs:
            print('\n' + key + ' references:')
            for ref in section_refs:
                ref_file = 'sections/' + ref + '.liquid'
                exists = ref_file in existing_sections
                status = 'EXISTS' if exists else 'MISSING'
                print('  ' + status + ': ' + ref_file)
                if not exists:
                    # Check if similar file exists
                    similar = [s for s in sections if ref.replace('-alt','').replace('-v2','').replace('-custom','') in s]
                    if similar:
                        print('    Similar: ' + str(similar))
    except:
        pass

# ============================================================
# PART 3: STANDARD vs CUSTOM LOGIC LEAK
# ============================================================
print('\n' + '=' * 70)
print('PART 3: STANDARD vs CUSTOM LOGIC LEAK')
print('=' * 70)

# Get collection.json (standard)
standard = get_asset('templates/collection.json')
custom_templates = [(t['key'], get_asset(t['key'])) for t in collection_templates if t['key'] != 'templates/collection.json']

print('\nStandard template (collection.json) structure:')
try:
    std_parsed = json.loads(standard)
    print('  ' + json.dumps(std_parsed, indent=2)[:500])
except:
    print('  PARSE ERROR')

# Compare with custom templates
for key, content in custom_templates:
    print('\n--- ' + key + ' ---')
    try:
        cust_parsed = json.loads(content)
        print('  ' + json.dumps(cust_parsed, indent=2)[:500])
    except:
        print('  PARSE ERROR')

# Check if standard has any custom variables or logic
print('\n--- Checking for global variable dependencies ---')
meta_tags = get_asset('snippets/meta-tags.liquid')
print('meta-tags.liquid uses:')
for var in ['current_page', 'page_description', 'collection.description', 'canonical_url']:
    found = var in meta_tags
    print('  ' + var + ': ' + str(found))

# ============================================================
# PART 4: PAGINATION CONFLICT CHECK
# ============================================================
print('\n' + '=' * 70)
print('PART 4: PAGINATION CONFLICT CHECK')
print('=' * 70)

# For each template, check for hardcoded pagination settings
for t in collection_templates:
    key = t['key']
    content = get_asset(key)
    if not content:
        continue
    try:
        parsed = json.loads(content)
        # Look for paginate, limit, products_per_page in schema
        json_str = json.dumps(parsed)
        if any(x in json_str.lower() for x in ['paginate', 'products_per_page', 'limit']):
            print('\n' + key + ' has pagination settings:')
            print('  ' + json_str[:300])
    except:
        pass

# ============================================================
# PART 5: THEME EDITOR SCHEMA AUDIT
# ============================================================
print('\n' + '=' * 70)
print('PART 5: THEME EDITOR SCHEMA AUDIT')
print('=' * 70)

# Check settings_data.json
settings = get_asset('config/settings_data.json')
if settings:
    print('settings_data.json size: ' + str(len(settings)) + ' bytes')
    try:
        parsed_settings = json.loads(settings)
        # Check for template overrides
        if 'theme_settings' in parsed_settings:
            print('theme_settings keys: ' + str(len(parsed_settings['theme_settings'])))
        # Check sections
        if 'sections' in parsed_settings:
            print('sections in settings_data.json: ' + str(len(parsed_settings['sections'])))
            # Check for orphaned section references
            for section_id, section_data in list(parsed_settings['sections'].items())[:20]:
                section_type = section_data.get('type', 'unknown')
                ref_file = 'sections/' + section_type + '.liquid'
                exists = ref_file in existing_sections
                status = 'OK' if exists else 'ORPHANED'
                if status == 'ORPHANED':
                    print('  ORPHANED: ID=' + str(section_id) + ', type=' + section_type)
    except json.JSONDecodeError as e:
        print('settings_data.json JSON ERROR: ' + str(e))
else:
    print('settings_data.json: NOT FOUND or EMPTY')
