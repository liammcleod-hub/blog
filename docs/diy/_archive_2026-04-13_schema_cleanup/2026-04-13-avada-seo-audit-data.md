# AVADA SEO Suite Full Audit Data

Date: 2026-04-13
Source: AVADA SEO Suite Dashboard

---

## Raw AVADA Output

```json
{
  "seo_audit_agent": {
    "products": [
      { "name": "Pentart Antikpaste 20ml", "handle": "/pentart-antikpaste-20ml", "score": "37 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Pigment fix 100ml", "handle": "/pentart-pigmentfix-100ml", "score": "37 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Metall Pigment 8g - gold", "handle": "/pentart-metall-pigment-gold", "score": "42 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Metall Pigment 8g - silber", "handle": "/pentart-metall-pigment-8g-silber", "score": "42 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Antikpaste Metallic Set", "handle": "/pentart-antikpaste-metallic-set", "score": "39 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Metallic-Pasten Bundle", "handle": "/metallic-master-set", "score": "38 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Rosteffekt Pulver", "handle": "/pentart-rosteffekt-set-pulver", "score": "44 (Arm)", "status": "Kritisch" },
      { "name": "Pentart Antik-Effekt Gel", "handle": "/pentart-antik-effekt-gel", "score": "36 (Arm)", "status": "Kritisch" }
    ],
    "collections": [
      { "name": "Haftgrundierung / Bonding Primer", "score": "43 (Arm)", "status": "Kritisch" },
      { "name": "Grundierung & Vorbereitung", "score": "39 (Arm)", "status": "Kritisch" },
      { "name": "All Products", "score": "36 (Arm)", "status": "Kritisch" }
    ],
    "pages": [
      { "title": "Katalog Ostern 2026 bis 2027", "score": "20 (Arm)", "status": "Kritisch" },
      { "title": "Bastelbedarf", "score": "40 (Arm)", "status": "Kritisch" },
      { "title": "Glasätzung", "score": "20 (Arm)", "status": "Kritisch" }
    ]
  },
  "speed_performance": {
    "score": 30,
    "rating": "Arm",
    "loading_speed": "8.6 s",
    "total_blocking_time": "2,820 ms"
  },
  "seo_checklist": {
    "overall_score": 55,
    "unsolved_tasks": 8,
    "critical_problems": 7,
    "content_issues": [
      "Bild alt: 1 Seite fehlt",
      "Inhalt der After-List-Sammlung fehlt",
      "Strukturierte Daten zu Bewertungen fehlen"
    ]
  },
  "instant_indexing": {
    "google_api_key": "Missing/JSON upload required",
    "bing_api_key": "Missing"
  },
  "local_business": {
    "opening_hours": {
      "Monday": "09:00 - 18:00",
      "Tuesday": "09:00 - 18:00",
      "Wednesday": "09:00 - 18:00",
      "Thursday": "09:00 - 18:00",
      "Friday": "09:00 - 18:00",
      "Saturday": "09:00 - 12:00",
      "Sunday": "Closed"
    }
  },
  "broken_link_manager": {
    "unresolved_404": 378,
    "resolved_404": 8321
  }
}
```

---

## Key Findings

### 🚨 SEO Score: 55/100 (Medium) — 7 Critical Problems

1. Strukturierte Daten zu Bewertungen fehlen (Review schema missing)
2. 378 broken links
3. Speed optimization never done (8.6s load time!)
4. Image alt missing on 1 page
5. After-list collection content missing

### 🚨 Speed: 30/100 (Poor)
- Loading: 8.6 seconds
- Blocking: 2.8 seconds
- AVADA acceleration mode: Not optimized

### 🚨 Indexing: API Keys Missing
- Google API key: ❌ Missing
- Bing API key: ❌ Missing

### ⚠️ Local Business: Wrong Hours Configured
- AVADA has: Mon-Fri 9-18, Sat 9-12
- Actual: Di-Fr 9-12 & 14-18, Sa 9-12

---

## Related Documents
- [[2026-04-13-store-wide-schema-audit]] — Full schema audit
- [[2026-04-13-store-wide-schema-adversarial-review]] — Strategic review
