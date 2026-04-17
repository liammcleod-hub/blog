import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment
store_url = os.getenv('SHOPIFY_SHOP_DOMAIN', 'bastelschachtel.myshopify.com')
access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
theme_id = os.getenv('SHOPIFY_THEME_ID', '196991385938')
api_version = os.getenv('SHOPIFY_API_VERSION', '2026-01')

print(f"Store: {store_url}")
print(f"Theme ID: {theme_id}")

# Headers for API requests
headers = {
    'X-Shopify-Access-Token': access_token,
    'Content-Type': 'application/json'
}

# Get theme information
try:
    url = f'https://{store_url}/admin/api/{api_version}/themes/{theme_id}.json'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        theme_data = response.json()
        print(f"Theme name: {theme_data['theme']['name']}")
        print(f"Theme role: {theme_data['theme']['role']}")
    else:
        print(f"Error getting theme info: {response.status_code}")
        print(response.text[:200])
except Exception as e:
    print(f"Error getting theme info: {e}")

# Try to get header-related files
header_files = [
    'sections/header.liquid',
    'snippets/header.liquid',
    'assets/theme.css',
    'assets/theme.scss',
    'sections/mobile-nav.liquid',
    'snippets/mobile-nav.liquid'
]

print("\nTrying to get header-related files...")

for filename in header_files:
    try:
        url = f'https://{store_url}/admin/api/{api_version}/themes/{theme_id}/assets.json?asset[key]={filename}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            asset_data = response.json()
            print(f"Found: {filename}")
            # Save the file content
            with open(f'temp_{filename.replace("/", "_")}', 'w', encoding='utf-8') as f:
                f.write(asset_data['asset']['value'])
        elif response.status_code == 404:
            print(f"Not found: {filename}")
        else:
            print(f"Error getting {filename}: {response.status_code}")
    except Exception as e:
        print(f"Error getting {filename}: {e}")