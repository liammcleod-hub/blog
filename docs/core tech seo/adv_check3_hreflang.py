import os, requests, re

# ADV CHECK 3: Hreflang collision - check live HTML for competing hreflang signals
print("=== HREFLANG COLLISION TEST ===")

headers = {"User-Agent": "Mozilla/5.0"}

# Fetch live homepage HTML and look for ALL language-related signals
r = requests.get("https://www.bastelschachtel.at/", headers=headers, timeout=15)
html = r.text

print(f"Homepage HTML size: {len(html)} bytes")

# Find all hreflang tags
hreflang_tags = re.findall(r'<link[^>]+rel=["\']alternate["\'][^>]*>', html, re.IGNORECASE)
print(f"\nhreflang tags found: {len(hreflang_tags)}")
for tag in hreflang_tags:
    print(f"  {tag}")

# Find html tag lang
html_tag = re.search(r'<html([^>]*)>', html)
print(f"\n<html> tag: {html_tag.group() if html_tag else 'NOT FOUND'}")

# Look for content_for_header (Shopify Markets injects here)
cfh_match = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
if cfh_match:
    head_content = cfh_match.group(1)
    # Look for anything that could be injected by Shopify Markets
    markets_signals = re.findall(r'(?:hreflang|locale|x-default|lang)[^<]{0,200}', head_content, re.IGNORECASE)
    print(f"\nPotential Markets/Shopify language injections in <head>:")
    for sig in markets_signals[:10]:
        print(f"  {sig[:150]}")

# Check for any JSON-LD inLanguage
jsonld_inlanguage = re.findall(r'"inLanguage"\s*:\s*"([^"]+)"', html)
print(f"\nJSON-LD inLanguage values: {jsonld_inlanguage}")

# Check theme.liquid for "markets" keyword  
print("\n--- Checking theme.liquid for 'markets' keyword ---")
import subprocess, json
result = subprocess.run([
    "curl", "-s",
    "https://bastelschachtel.myshopify.com/admin/api/2024-01/themes/196991385938/assets.json?asset%5Bkey%5D=layout/theme.liquid",
    "-H", "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
], capture_output=True, text=True)
try:
    d = json.loads(result.stdout)
    v = d.get("asset", {}).get("value", "")
    print(f"'markets' found in theme.liquid: {'markets' in v.lower()}")
    print(f"'market' found: {'market' in v.lower()}")
    print(f"'locale' found: {'locale' in v.lower()}")
    if "market" in v.lower():
        for i, line in enumerate(v.split("\n"), 1):
            if "market" in line.lower():
                print(f"  Line {i}: {line.strip()[:120]}")
except Exception as e:
    print(f"Error: {e}")

# Also check content_for_header content type
print("\n--- Checking content_for_header injection type ---")
cfh_section = re.search(r'content_for_header[^>]*>', html)
if cfh_section:
    print(f"content_for_header tag: {cfh_section.group()[:200]}")
else:
    print("content_for_header not found as a visible tag (it's typically processed server-side)")

print("\n=== KEY FINDING ===")
print("If Shopify Markets is active, it injects hreflang via content_for_header.")
print("content_for_header is processed server-side - it won't show in raw HTML inspection.")
print("We CANNOT confirm whether Shopify Markets is active without Admin API access.")
print()
print("WORST CASE:")
print("  If Markets is active AND we inject our own hreflang,")
print("  we create DUPLICATE HREFLANG CONFLICT.")
print("  Google may ignore both signals or pick the wrong one.")
print()
print("RECOMMENDATION:")
print("  Before injecting hreflang, check Shopify Admin â†’ Settings â†’ Markets")
print("  OR inspect via browser DevTools Network tab for 'content_for_header' response")
print("  which contains Markets-injected hreflang tags.")
