import os, requests, re, json, subprocess

TOKEN = os.environ.get('SHOPIFY_ACCESS_TOKEN', '')
if not TOKEN:
    raise SystemExit('Missing SHOPIFY_ACCESS_TOKEN (set it in your environment or .env)')
THEME = "196991385938"
BASE_URL = "https://www.bastelschachtel.at"

# ============================================================
# PART 1: Static vs Dynamic Head Audit
# ============================================================
print("=== PART 1: STATIC VS DYNAMIC HEAD AUDIT ===")

headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}

# Test 1a: Base collection meta tags
url_base = f"{BASE_URL}/collections/all"
r_base = requests.get(url_base, headers=headers, timeout=20)
desc_base = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', r_base.text, re.IGNORECASE)
title_base = re.search(r'<title[^>]*>([^<]+)</title>', r_base.text)
canon_base = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', r_base.text, re.IGNORECASE)
print(f"Base (/collections/all):")
print(f"  Title: {title_base.group(1).strip() if title_base else 'NOT FOUND'}")
print(f"  Description: {desc_base.group(1)[:80] if desc_base else 'NOT FOUND'}...")
print(f"  Canonical: {canon_base.group(1) if canon_base else 'NOT FOUND'}")

# Test 1b: Page 2 meta tags (server-side)
url_p2 = f"{BASE_URL}/collections/all?page=2"
r_p2 = requests.get(url_p2, headers=headers, timeout=20)
desc_p2 = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', r_p2.text, re.IGNORECASE)
title_p2 = re.search(r'<title[^>]*>([^<]+)</title>', r_p2.text)
canon_p2 = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', r_p2.text, re.IGNORECASE)
print(f"\nPage 2 (/collections/all?page=2):")
print(f"  Title: {title_p2.group(1).strip() if title_p2 else 'NOT FOUND'}")
print(f"  Description: {desc_p2.group(1)[:80] if desc_p2 else 'NOT FOUND'}...")
print(f"  Canonical: {canon_p2.group(1) if canon_p2 else 'NOT FOUND'}")

# Test 1c: Same for a smaller collection
url_small = f"{BASE_URL}/collections/glasatzen"
r_small = requests.get(url_small, headers=headers, timeout=20)
desc_small = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', r_small.text, re.IGNORECASE)
title_small = re.search(r'<title[^>]*>([^<]+)</title>', r_small.text)
print(f"\nSmall collection (/collections/glasatzen):")
print(f"  Title: {title_small.group(1).strip() if title_small else 'NOT FOUND'}")
print(f"  Description: {desc_small.group(1)[:80] if desc_small else 'NOT FOUND'}...")

url_small_p2 = f"{BASE_URL}/collections/glasatzen?page=2"
r_small_p2 = requests.get(url_small_p2, headers=headers, timeout=20)
desc_small_p2 = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', r_small_p2.text, re.IGNORECASE)
title_small_p2 = re.search(r'<title[^>]*>([^<]+)</title>', r_small_p2.text)
print(f"\nSmall collection Page 2 (/collections/glasatzen?page=2):")
print(f"  Title: {title_small_p2.group(1).strip() if title_small_p2 else 'NOT FOUND'}")
print(f"  Description: {desc_small_p2.group(1)[:80] if desc_small_p2 else 'NOT FOUND'}...")

print("\n=== KEY FINDING: TITLE vs DESCRIPTION DIVERGENCE ===")
print(f"All title_base: '{title_base.group(1).strip() if title_base else 'N/A'}'")
print(f"All title_p2:   '{title_p2.group(1).strip() if title_p2 else 'N/A'}'")
print(f"Title different? {title_base.group(1).strip() != title_p2.group(1).strip() if title_base and title_p2 else 'N/A'}")
print(f"All desc_base:   '{desc_base.group(1)[:80] if desc_base else 'N/A'}'")
print(f"All desc_p2:     '{desc_p2.group(1)[:80] if desc_p2 else 'N/A'}'")
print(f"Description different? {desc_base.group(1) != desc_p2.group(1) if desc_base and desc_p2 else 'N/A'}")

print("\n=== PAGE 2 vs PAGE 1 HTML SIZE COMPARISON ===")
print(f"Base /collections/all HTML: {len(r_base.text):,} bytes")
print(f"Page 2 /collections/all HTML: {len(r_p2.text):,} bytes")
print(f"Size ratio (p2/base): {len(r_p2.text)/len(r_base.text):.2f}x")
print(f"\nBase /collections/glasatzen HTML: {len(r_small.text):,} bytes")
print(f"Page 2 glasatzen HTML: {len(r_small_p2.text):,} bytes")
