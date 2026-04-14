import requests, re

# ADV CHECK 4: Noindex /search collision - check for ?q= search landing pages
print("=== NOINDEX /SEARCH COLLISION TEST ===")

headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the DIY HowTo pages and check for ?q= links
diy_pages = [
    "https://www.bastelschachtel.at/pages/diy-experience/handykette",
    "https://www.bastelschachtel.at/pages/diy-experience/batik-tshirt",
]

for url in diy_pages:
    r = requests.get(url, headers=headers, timeout=15)
    # Find any search parameter links
    search_links = re.findall(r'href=["\']([^"\']*\?q=[^"\']+)["\']', r.text)
    search_links_abs = re.findall(r'href=["\'](https://www\.bastelschachtel\.at/search[^"\']+)["\']', r.text)
    print(f"\n{url}")
    print(f"  ?q= search links: {len(search_links)}")
    for link in search_links[:5]:
        print(f"    {link}")
    print(f"  /search absolute links: {len(search_links_abs)}")
    for link in search_links_abs[:5]:
        print(f"    {link}")

# Also check the homepage for search links
r_home = requests.get("https://www.bastelschachtel.at/", headers=headers, timeout=15)
home_search_links = re.findall(r'href=["\']([^"\']*\?q=[^"\']+)["\']', r_home.text)
home_search_abs = re.findall(r'href=["\'](https://www\.bastelschachtel\.at/search[^"\']+)["\']', r_home.text)
print(f"\nHomepage ?q= links: {len(home_search_links)}")
for link in home_search_links[:5]:
    print(f"  {link}")
print(f"Homepage /search absolute links: {len(home_search_abs)}")
for link in home_search_abs[:5]:
    print(f"  {link}")

# Check the search results section template more carefully
# Does the /search page have any value beyond user queries?
print("\n--- Analyzing /search page value ---")

# Fetch the actual /search page
r_search = requests.get("https://www.bastelschachtel.at/search", headers=headers, timeout=15)
# Check if there are any meta tags that suggest it's a "landing page"
has_title = re.search(r'<title>([^<]+)</title>', r_search.text)
has_meta_desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^\"\']+)', r_search.text, re.IGNORECASE)
robots = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^\"\']+)', r_search.text, re.IGNORECASE)
canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^\"\']+)', r_search.text, re.IGNORECASE)

print(f"Search page status: {r_search.status_code}")
print(f"Title: {has_title.group(1) if has_title else 'NOT FOUND'}")
print(f"Meta description: {has_meta_desc.group(1)[:80] if has_meta_desc else 'NOT FOUND'}")
print(f"Robots meta: {robots.group(1) if robots else 'NONE (no robots meta)'}")
print(f"Canonical: {canonical.group(1) if canonical else 'NOT FOUND'}")

# KEY: Does the search page have a static title that suggests it's a "page"?
# If /search page has a unique, valuable title like "Bastelschachtel Shop-Suche",
# it might be getting organic traffic and shouldn't be noindexed.
print("\n=== KEY FINDING ===")
print("If /search page has organic traffic (searching for 'Bastelschachtel Produkte'),")
print("noindexing it would remove that page from search results.")
print()
print("HOW TO VERIFY:")
print("  1. Check GSC for /search page performance")
print("  2. If /search has impressions/clicks, do NOT noindex it")
print("  3. If /search has 0 impressions, noindex is safe")
print()
print("ADDITIONAL CONCERN:")
print("  If the site uses internal search links (?q=) as navigation,")
print("  those URLs would also be noindexed, killing internal link equity")
print("  flowing through search parameter URLs.")
