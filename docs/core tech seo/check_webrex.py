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

# Get schulbedarf template - has Webrex
schul = get_asset('templates/collection.schulbedarf.json')
parsed = json.loads(schul)

print('SCHULBEDARF template sections:')
for sec_id, sec_data in parsed.get('sections', {}).items():
    sec_type = str(sec_data.get('type', ''))
    block_count = len(sec_data.get('blocks', {}))
    if 'webrex' in sec_type or 'b26797ad' in sec_type:
        print('  ZOMBIE: ' + sec_id + ' -> type: ' + sec_type)
    else:
        print('  VALID:  ' + sec_id + ' -> type: ' + sec_type)

# Get winter template - has Webrex
winter = get_asset('templates/collection.winter.json')
parsed_w = json.loads(winter)
print('\nWINTER template sections:')
for sec_id, sec_data in parsed_w.get('sections', {}).items():
    sec_type = str(sec_data.get('type', ''))
    if 'webrex' in sec_type or 'b26797ad' in sec_type:
        print('  ZOMBIE: ' + sec_id + ' -> type: ' + sec_type)
    else:
        print('  VALID:  ' + sec_id + ' -> type: ' + sec_type)
