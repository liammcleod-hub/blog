# Bastelschachtel Store-Wide Schema: Adversarial Review

Date: 2026-04-13
Parent: [[2026-04-13-store-wide-schema-audit]]

---

# Adversarial Review: Schema Audit Strategy

## Challenge 1: Is Schema Markup Even The Right Priority?

**The assumption:** "We need structured data for SEO."

**The challenge:**
- For a niche craft supplies store in Austria, **ranking for "Bastelbedarf"** is not won by schema — it's won by product coverage, category pages, and DIY content clusters.
- Google's crawlers read your HTML just fine. Schema is a **confidence signal**, not a ranking factor.
- The real question: **What does Bastelschachtel rank for today?** If it's product keywords, schema won't help. If it's DIY/how-to searches, HowTo schema matters — but only if you have the content.

**Counter-question:** What search queries do you actually want to rank for?

---

## Challenge 2: FAQPage — Are These The Right Questions?

**The assumption:** "We should add FAQ schema for our 7 shipping/payment FAQs."

**The challenge:**
- Your current 7 FAQs are **transactional** (shipping, payment, returns) — not the questions people search before buying.
- People searching "Bastelbedarf kaufen Österreich" don't have these FAQs — they have **informational** questions:
  - "Welcher Bastelbedarf für Anfänger?"
  - "Pentart vs Marabu Farben Unterschied"
  - "Wie startet man mit Korbflechten?"
- The 3 FAQs on "Bastelbedarf" page are **better** — but you want to put them on /faq instead? That's backwards.

**Counter-question:** What questions are your competitors answering that you're not?

---

## Challenge 3: LocalBusiness — Do You Even Need It?

**The assumption:** "We need LocalBusiness schema with hours and address."

**The challenge:**
- You're an **e-commerce store** shipping from Austria. LocalBusiness is for businesses people visit in person.
- If you're targeting Austrian customers who want "Bastelbedarf in der Nähe" — then yes.
- But if your customer is "Martha, 45, from Graz who found you on Google" — she doesn't care about your Wattens address. She cares about shipping time and reviews.
- LocalBusiness schema can actually **hurt** if Google thinks you're a physical store and users bounce because they expected to pick up.

**Counter-question:** What % of your traffic/search intent is local vs. national/e-commerce?

### Updated Assessment After New Data

✅ **You DO have a walk-in store** (Bastel-Kreativ GmbH, Swarovskistraße 3, 6112 Wattens)
✅ **Google Business Profile exists** with 5.0 rating, 27 reviews
✅ **Social profiles linked**: YouTube, Instagram, Facebook, Pinterest

**This changes things:** LocalBusiness schema is now **HIGH priority** — especially for "Bastelschachtel Wattens" local searches. You have the assets to make it work.

---

## Challenge 4: The DIY Content Strategy — Is This The Real Play?

**The assumption:** "We should add HowTo schema to DIY pages."

**The challenge:**
- **You already have DIY metaobjects** — but no schema. That's a 1% problem.
- The **bigger** problem: Are DIY pages actually getting traffic? Are they optimized for the right keywords?
- HowTo schema requires **perfect implementation** — Google is strict. If steps are missing or malformed, it shows nothing in SERPs.
- Is the effort worth it vs. just writing better meta descriptions?

**Counter-question:** Which DIY pages currently rank? What's their CTR? What's the actual traffic opportunity?

---

## Challenge 5: Implementation Method — Wrong Tool?

**The assumption:** "We'll add schema to theme.liquid."

**The challenge:**
- You're on **Horizon/Maerz 2026** theme. These are modern Shopify themes with sections.
- Adding schema to theme.liquid means it appears on **every page** — which breaks FAQPage rules.
- Better approach: Use **Shopify's built-in schema system** or a **dedicated SEO app** (Schema Pro, RankMath, Yoast) that handles validation automatically.
- Manual JSON-LD in theme files = maintenance nightmare and easy to break.

**Counter-question:** Are you already paying for an SEO app that handles this? If not, why not?

---

## Challenge 6: The "Bastelbedarf" Page — What Is This?

**The assumption:** "Schema exists on Bastelbedarf page, we should clean it up."

**The challenge:**
- This page has **WebPage + FAQPage + BreadcrumbList + Organization** all in one page. That's a red flag.
- It looks like a **content dump** or a category landing page with FAQs slapped on.
- If this is supposed to rank for "Bastelbedarf kaufen", does it actually convert? What's the bounce rate?
- The broken template variables (`{{ shop.name }}` not rendering) suggest **this page isn't working as intended at all**.

**Counter-question:** Is this page worth fixing, or should it be restructured entirely?

---

## Current Search Presence Data

### Google Search Result (bastelschachtel)

```json
{
  "title": "Bastelbedarf kaufen | Bastelschachtel - Kreativshop Österreich",
  "displayed_url": "https://www.bastelschachtel.at/",
  "snippet": "Bastelbedarf aus Österreich: Pentart, Reispapier, Korbflechten, Bastelsets und kreative Spezialprodukte. 4,88☆, persönliche Beratung und Versand ab 70€ ...",
  "sitelinks": [
    "Textilien und Wolle",
    "All Products",
    "Kontakt",
    "Verkäufer:in Job in Wattens",
    "Collections"
  ]
}
```

### Google Business Profile (GMB)

```json
{
  "name": "Bastelschachtel der Online Kreativshop",
  "type": "Corporate office",
  "rating": 5.0,
  "review_count": 27,
  "address": "Swarovskistraße 3, 6112 Wattens",
  "phone": "+43 664 4564271",
  "profiles": {
    "youtube": "https://www.youtube.com/channel/UCv8kayedKQE_SwS9wVFnASg",
    "instagram": "https://www.instagram.com/bastelschachtel_onlineshop/",
    "facebook": "https://www.facebook.com/bastelschachtel",
    "pinterest": "https://at.pinterest.com/bastelschachtel/"
  },
  "description": "Online Bastelgeschäft aus Wattens mit Bastelmaterial für Bastelfeen und kreative Köpfe"
}
```

### MOZ Metrics
- Domain Authority: **16/100** (low — room to grow)
- Referring Domains: **296**
- Referring Links: **2.64K**
- Spam Score: **2%** (good)

---

## Revised Priority Assessment

### HIGH Impact (do first):

1. **LocalBusiness schema** — You have GMB, walk-in store, social profiles. This is now HIGH.
2. **Organization schema** — Link to GMB, include social `sameAs` links from GMB profile.
3. **Product schema** — You're probably missing this entirely. Product JSON-LD shows stars, price, availability.
4. **Fix Bastelbedarf page** — Broken template vars = broken schema. Fix or delete.

### MEDIUM Impact (if resources allow):

5. **HowTo schema** — Only if DIY pages get real traffic. Test first.
6. **Proper FAQPage** — Only if /faq page ranks or is linked from nav.

### LOW Impact (probably skip):

7. **WebSite schema** — Mostly cosmetic for Sitelinks (already have them).
8. **General FAQPage** — Transactional FAQs don't help informational searches.

---

## Questions to Challenge Your Strategy:

1. What does Google Search Console say your **top queries** are?
2. What does your **traffic by page type** look like? (Products, categories, blog, DIY, homepage)
3. Are you using an **SEO app** that might already handle schema?
4. What's the **bounce rate** on DIY pages?
5. Who is your **actual customer** — Austrian local or European online shopper?

---

## Next Steps

- [ ] Check SEO app (AVADA SEO Suite installed?)
- [ ] Get GSC data for top queries
- [ ] Review DIY page traffic
- [ ] Reassess FAQ strategy — transactional vs informational

---

## Related Documents

- [[2026-04-13-store-wide-schema-audit]] — Full audit with current state
