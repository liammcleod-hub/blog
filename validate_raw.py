#!/usr/bin/env python3
"""Internal Validator Protocol — Raw Evidence Report"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests, re, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def find_ld_blocks(html):
    pattern = re.compile(
        '<script[^>]*type\\s*=\\s*["\']application/ld\\+json["\'][^>]*>(.*?)</script>',
        re.DOTALL | re.IGNORECASE
    )
    return pattern.findall(html)

print("=" * 70)
print("  INTERNAL VALIDATOR PROTOCOL — RAW EVIDENCE REPORT")
print("=" * 70)

# SECTION 1: RAW HOMEPAGE JSON-LD EXTRACT
print("\n" + "=" * 70)
print("  SECTION 1 — HOMEPAGE: Raw JSON-LD Extract")
print("=" * 70)

r_home = requests.get("https://www.bastelschachtel.at/", headers=HEADERS, timeout=30)
print("HTTP Status: %d" % r_home.status_code)
print("HTML Size: %d bytes (%.2f MB)" % (len(r_home.text), len(r_home.text)/1024/1024))

home_blocks = find_ld_blocks(r_home.text)
print("JSON-LD blocks found: %d" % len(home_blocks))

for i, raw in enumerate(home_blocks):
    raw = raw.strip()
    print("\n" + ("-" * 60))
    print("  BLOCK %d — %d characters" % (i+1, len(raw)))
    print("-" * 60)
    try:
        parsed = json.loads(raw)
        etypes = [e.get('@type', '?') for e in parsed.get('@graph', [])]
        print("  @type: %s" % parsed.get('@type', 'none'))
        print("  @graph entities: %s" % etypes)
        print("\n  FULL RAW JSON OUTPUT:")
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print("  PARSE ERROR: %s" % e)
        print("  Raw: %s" % repr(raw[:300]))

# SECTION 2: RAW FAQ PAGE JSON-LD EXTRACT
print("\n" + "=" * 70)
print("  SECTION 2 — FAQ PAGE: Raw JSON-LD Extract")
print("=" * 70)

r_faq = requests.get("https://www.bastelschachtel.at/pages/faq-haufig-fragen", headers=HEADERS, timeout=30)
print("HTTP Status: %d" % r_faq.status_code)
print("HTML Size: %d bytes" % len(r_faq.text))

faq_blocks = find_ld_blocks(r_faq.text)
print("JSON-LD blocks found: %d" % len(faq_blocks))

for i, raw in enumerate(faq_blocks):
    raw = raw.strip()
    print("\n" + ("-" * 60))
    print("  BLOCK %d — %d characters" % (i+1, len(raw)))
    print("-" * 60)
    try:
        parsed = json.loads(raw)
        print("  @type: %s" % parsed.get('@type', 'none'))
        if '@graph' in parsed:
            for e in parsed['@graph']:
                print("  @graph entity: %s @id=%s" % (e.get('@type','?'), e.get('@id','NO ID')[:60]))
        elif parsed.get('@type') == 'FAQPage':
            qs = parsed.get('mainEntity', [])
            print("  FAQPage mainEntity questions: %d" % len(qs))
        print("\n  FULL RAW JSON OUTPUT:")
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError as e:
        print("  PARSE ERROR: %s" % e)
        print("  Raw: %s" % repr(raw[:300]))

# SECTION 3: GHOST AUDIT
print("\n" + "=" * 70)
print("  SECTION 3 — GHOST AUDIT: Full HTML Scan")
print("=" * 70)

for page_name, url in [
    ("HOMEPAGE", "https://www.bastelschachtel.at/"),
    ("FAQ PAGE", "https://www.bastelschachtel.at/pages/faq-haufig-fragen"),
]:
    print("\n  --- %s ---" % page_name)
    r = requests.get(url, headers=HEADERS, timeout=30)
    print("  HTML size: %d bytes" % len(r.text))

    all_blocks = find_ld_blocks(r.text)
    print("  Total JSON-LD blocks: %d" % len(all_blocks))

    for j, raw in enumerate(all_blocks):
        try:
            parsed = json.loads(raw.strip())
            etype = parsed.get('@type', 'none')
            graph_types = [e.get('@type','?') for e in parsed.get('@graph', [])]
            print("    Block %d: @type=%s, @graph=%s" % (j+1, etype, graph_types))
        except:
            print("    Block %d: PARSE ERROR" % (j+1))

    # "Organization" type in HTML
    org_matches = list(re.finditer(r'"@type"\s*:\s*"Organization"', r.text))
    print("  '\"@type\": \"Organization\"' in HTML: %d" % len(org_matches))
    for m in org_matches[:3]:
        ctx_start = max(0, m.start()-50)
        snippet = r.text[ctx_start:m.end()+50].replace('\n',' ')
        print("    ...%s..." % snippet[:100])

    # AVADA in JSON-LD blocks
    avada_in_ld = 0
    for raw in all_blocks:
        if 'avada' in raw.lower() or 'AVADA' in raw:
            avada_in_ld += 1
    print("  AVADA INSIDE JSON-LD blocks: %d" % avada_in_ld)

    # Categorize AVADA in HTML
    avada_all = list(re.finditer(r'.{0,40}[Aa][Vv][Aa][Dd][Aa].{0,40}', r.text))
    print("  AVADA in full HTML: %d occurrences" % len(avada_all))
    in_jsonld = 0
    firebase_ct = 0
    other_ct = 0
    for m in avada_all:
        start_pos = m.start()
        preceding = r.text[max(0, start_pos-200):start_pos].lower()
        if 'application/ld+json' in preceding or 'ld+json' in preceding:
            in_jsonld += 1
        elif 'firebasestorage' in m.group(0).lower() or 'avada-joy' in m.group(0).lower():
            firebase_ct += 1
        else:
            other_ct += 1
    print("    in JSON-LD script tags: %d" % in_jsonld)
    print("    in Firebase storage URLs: %d" % firebase_ct)
    print("    elsewhere (other): %d" % other_ct)

# SECTION 4: ID INTEGRITY CHECK
print("\n" + "=" * 70)
print("  SECTION 4 — ID INTEGRITY CHECK")
print("=" * 70)

for block in home_blocks:
    try:
        parsed = json.loads(block.strip())
        if '@graph' in parsed:
            graph = parsed['@graph']
            ids = {}
            for e in graph:
                t = e.get('@type', '?')
                eid = e.get('@id', '')
                ids[t] = eid

            org_id       = ids.get('ArtSupplyStore', 'MISSING')
            local_id     = ids.get('LocalBusiness', 'MISSING')
            web_id       = ids.get('WebSite', 'MISSING')
            local_parent = next((e.get('parentOrganization',{}).get('@id','') for e in graph if e.get('@type')=='LocalBusiness'), 'MISSING')
            web_pub      = next((e.get('publisher',{}).get('@id','') for e in graph if e.get('@type')=='WebSite'), 'MISSING')

            print("\n  Organization (ArtSupplyStore) @id:")
            print("    '%s'" % org_id)
            print("\n  LocalBusiness @id:")
            print("    '%s'" % local_id)
            print("\n  LocalBusiness parentOrganization @id:")
            print("    '%s'" % local_parent)
            print("\n  WebSite @id:")
            print("    '%s'" % web_id)
            print("\n  WebSite publisher @id:")
            print("    '%s'" % web_pub)

            print("\n  Integrity checks:")
            chk1 = (org_id == local_parent)
            chk2 = (org_id == web_pub)
            chk3 = all(u.startswith('https://') for u in [org_id, local_id, web_id])
            chk4 = not any('//#' in u for u in [org_id, local_id, web_id])
            print("    Org == Local.parentOrganization : %s %s" % (chk1, chr(9989) if chk1 else chr(10060)+' BREACH'))
            print("    Org == WebSite.publisher        : %s %s" % (chk2, chr(9989) if chk2 else chr(10060)+' BREACH'))
            print("    All @ids start with https://    : %s %s" % (chk3, chr(9989) if chk3 else chr(10060)))
            print("    No //# double-slash             : %s %s" % (chk4, chr(9989) if chk4 else chr(10060)))
    except Exception as e:
        print("  Error: %s" % e)

# SECTION 5: TRANSACTIONAL BRIDGE
print("\n" + "=" * 70)
print("  SECTION 5 — TRANSACTIONAL BRIDGE: Exact acceptedAnswer.text")
print("=" * 70)

for block in faq_blocks:
    try:
        parsed = json.loads(block.strip())
        if parsed.get('@type') == 'FAQPage':
            for q in parsed.get('mainEntity', []):
                name = q.get('name', '')
                text = q.get('acceptedAnswer', {}).get('text', '')
                if any(kw in name.lower() or kw in text.lower() for kw in ['lager', 'glas', 'glasaetz']):
                    print("\n  Question: %s" % name)
                    print("\n  acceptedAnswer.text (raw Python repr):")
                    print("  %s" % repr(text))
                    hrefs = re.findall(r'href="([^"]+)"', text)
                    if hrefs:
                        print("\n  href URLs found:")
                        for h in hrefs:
                            print("    %s" % h)
                            if 'glasaetzungspaste' in h:
                                print("      -> CORRECT: non-pentart- handle " + chr(9989))
                            elif 'pentart' in h:
                                print("      -> WRONG: pentart- prefix " + chr(10060) + " BREACH")
    except Exception as e:
        print("  Error: %s" % e)

# SECTION 6: CANONICAL TAG
print("\n" + "=" * 70)
print("  SECTION 6 — CANONICAL TAG: Exact <link rel=canonical>")
print("=" * 70)

for page_name, url in [
    ("HOMEPAGE", "https://www.bastelschachtel.at/"),
    ("FAQ PAGE", "https://www.bastelschachtel.at/pages/faq-haufig-fragen"),
]:
    r = requests.get(url, headers=HEADERS, timeout=30)
    m = re.search(r'<link[^>]+\bhref=["\']([^"\']+)["\'][^>]+\brel=["\']canonical["\']', r.text, re.IGNORECASE)
    if not m:
        m = re.search(r'<link[^>]+\brel=["\']canonical["\'][^>]+\bhref=["\']([^"\']+)["\']', r.text, re.IGNORECASE)
    if m:
        tag_start = max(0, m.start()-20)
        tag_end = m.end() + 5
        snippet = r.text[tag_start:tag_end].replace('\n',' ').strip()
        print("\n  %s canonical:" % page_name)
        print("  Tag: %s" % snippet)
        print("  URL: %s" % m.group(1))
    else:
        print("\n  %s: NOT FOUND" % page_name)

print("\n" + "=" * 70)
print("  END OF EVIDENCE REPORT")
print("=" * 70)
