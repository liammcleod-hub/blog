# Operation Ironclad — Strategic Overview

**Date:** 2026-04-14 | **Status:** Read-Only Audit Complete | **Phase:** Ready for Implementation

---

## 🎯 The End Goal: DACH Domination via AEO/GEO

**Operation Ironclad** is a comprehensive campaign to make **bastelschachtel.at** the **#1 craft supplies retailer in the DACH region** through superior technical implementation aligned with the **AEO/GEO Framework**.

### What is AEO/GEO?
- **AEO (Answer Engine Optimization)**: Winning the answer box via FAQ schema, Q&A structure
- **GEO (Generative Engine Optimization)**: Being named in AI-generated responses via entity signals and schema authority
- **Identity Graph**: All entities linked with `@id` references forming a machine-readable knowledge graph

### The FORTRESS Architecture
This is our implementation of the AEO/GEO framework:
- **One Organization** (`#organization`) with Austrian legal credentials (GmbH, VAT ID)
- **All pages reference this Organization** as publisher, provider, parentOrganization
- **Zero duplicate schemas** — competing schemas suppressed
- **Transactional Bridge** — product offers link back to the main Organization

---

## 🏗️ Current State: FORTRESS Deployed with Critical Leaks

### ✅ **What's Working (FORTRESS Core)**
- Homepage: 1 JSON-LD @graph (ArtSupplyStore + LocalBusiness + WebSite)
- @id spine consistency across all entities
- AVADA schema suppression working
- FAQPage with 7 Q&As
- Transactional Bridge to products
- Canonical hygiene (1 per page)

### 🔴 **Critical Leaks (Discovering During Verification)**

| Leak | AEO/GEO Impact | Priority |
|------|---------------|----------|
| **Bastelbedarf page bleeding broken schema** | ❌ Violates "unambiguous identity" principle | 🔴 CRITICAL |
| **HowTo schema NOT rendering on DIY pages** | ❌ Breaks #2 highest-impact schema type | 🔴 CRITICAL |
| **Collection pages missing H1 tags** | ⚠️ Weakens topic signaling for AI | 🟡 HIGH |
| **AVADA 404 scripts injecting via Shopify Admin** | ⚠️ Signals poor site hygiene | 🟡 HIGH |
| **Schema gap: no `shippingDetails`/`MerchantReturnPolicy`** | ❌ Missing DACH trust signals | 🟢 MEDIUM |

---

## 🔄 The Full Campaign Phases

### **Phase 1: Forensic Audit** → ✅ DONE
- Live API handshake, theme ID confirmation
- Deep recursive scan of all templates
- Zombie hunt: 14 infected templates found (10 collections + 4 products)
- Pagination Trap confirmed live

### **Phase 2: "Going Wide" Lateral Scan** → ✅ DONE
- Checked 4 vectors: content bloat, asset rot, merchant identity, parameter explosion
- Found: 9 orphaned AVADA snippets, 2 AVADA 404 scripts, missing DACH schema nodes
- Report saved: `2026-04-14-operation-ironclad-lateral-extension-report.md`

### **Phase 3: Implementation (Clean Sweep + Fortress Expansion)** → 🟡 PENDING
**Objective:** Fix all leaks, complete the FORTRESS architecture
**Methodology:** Governed by [[OPERATION-IRONCLAD-SCIENTIFIC-METHODOLOGY]]

**Sub-phases:**
1. **Phase 3A (Critical):** Restore unambiguous identity + enable HowTo rich results
2. **Phase 3B (High):** Strengthen topic signaling + clean technical foundation  
3. **Phase 3C (Medium):** Maximize FAQ coverage + DACH trust signals
4. **Phase 3D (Framework):** Full AEO/GEO framework alignment

### **Phase 4: Verification & GSC Import** → 🔮 FUTURE
- Byte-for-byte verification of all fixes
- Google Search Console performance monitoring
- AI citation tracking

---

## 🛠️ Implementation Resources

| Document | Purpose |
|----------|---------|
| **`2026-04-14-operation-ironclad-verification-findings-sorted.md`** | Prioritized action plan with AEO/GEO alignment |
| **`2026-04-14-operation-clean-sweep-handoff.md`** | Step-by-step instructions for Phase 3 |
| **`2026-04-14-operation-ironclad-lateral-extension-report.md`** | Full lateral scan findings |
| **`2026-04-13-aeo-geo-framework.md`** | Strategic blueprint for AEO/GEO implementation |
| **`2026-04-13-schema-master-status.md`** | Current live schema state |

---

## 📈 Success Metrics (Post-Implementation)

### **Technical Perfection**
- Zero duplicate meta descriptions (Pagination Trap eliminated)
- Zero Webrex zombies in any template  
- Zero AVADA 404 scripts
- 100% schema coverage (Organization, LocalBusiness, WebSite, FAQPage, HowTo, Product with shipping/returns)
- Perfect hreflang for DACH markets (when scope granted)
- Clean canonicals (1 per page, filter parameters stripped)
- All collection pages with proper H1 hierarchy

### **AEO/GEO Excellence**
- **Unambiguous identity**: One stable Organization entity with durable @id
- **Extractable evidence**: Visible content matches structured data 100%
- **Entity graph**: All schema types linked via @id references
- **DACH trust signals**: Austrian legal credentials, German-language content, regional qualifiers
- **E-E-A-T signals**: Experience (DIY content), Expertise (Pentart products), Authoritativeness (reviews), Trustworthiness (GDPR compliance)

---

## 🚀 Ready for Implementation

**Current status:** Read-only audit complete. All leaks documented. Prioritized action plan created. 

**Next step:** Await authorization to exit read-only mode and begin Phase 3 implementation.

**Estimated impact:** When Operation Ironclad is complete, bastelschachtel.at will be a **Fortress** — technically perfect, schema-rich, and positioned to dominate German-language craft search for years.

---

## 📜 GOVERNING METHODOLOGY

All Phase 3+ implementation is governed by the **Scientific Methodology (LAW)**:

```
KNOW → HYPOTHESIZE → STRESS TEST → ADVERSARIAL REVIEW → PROVE → IMPLEMENT → VERIFY
```

**Reference:** [[OPERATION-IRONCLAD-SCIENTIFIC-METHODOLOGY]] for full protocol.

---

> **Key Insight:** This isn't just about fixing bugs. It's about building an **impenetrable technical foundation** that makes bastelschachtel.at the **authoritative source** AI engines will cite when answering craft-related queries in the DACH region.