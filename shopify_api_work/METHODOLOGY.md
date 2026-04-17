# Shopify API Development Methodology

We will always follow this rigorous scientific method for all development work:

```
KNOW → HYPOTHESIZE → STRESS TEST → ADVERSARIAL REVIEW → PROVE → IMPLEMENT → VERIFY
    ↑                                                               ↓
    └───────────────────────────────── REJECT ──────────────────────┘
```

## 🎯 CORE PRINCIPLES

### 1. **Current State is Holy**
- Never assume, always verify
- Byte-for-byte live production snapshots are the only truth
- API-verified theme asset inventory required before any hypothesis

### 2. **Hypotheses are Falsifiable**
- Must define clear pass/fail criteria upfront
- "If we change X to Y, then Z will improve"
- No vague predictions allowed

### 3. **Adversarial Mindset Required**
- Actively try to break your own fixes
- Assume competitors will exploit any weakness
- AI crawlers will misinterpret edge cases

### 4. **Proof Before Production**
- No implementation without empirical evidence
- Before/after comparisons with timestamps
- Schema validator passes required

### 5. **Atomic Reversibility**
- One change at a time
- Always revertible within 5 minutes
- Backup snapshots remain untouched

### 6. **Write to Live, Verify Instantly**
- Direct implementation to production
- No staging delays
- Immediate verification post-implementation

## 🔬 THE 7-PHASE METHOD

### **Phase 1: KNOW — Comprehensive Current State**
**Goal:** Establish irrefutable baseline
- **Byte-for-byte** live production snapshots
- **API-verified** system state  
- **Cross-referenced** documentation
- **Quantified** issues (counts, not adjectives)

**Deliverable:** *Current State Dossier* — machine-verifiable truth table

### **Phase 2: HYPOTHESIZE — Falsifiable Fix Formulation**
**Goal:** Articulate testable predictions
- Format: "If we change X to Y, then Z will improve"
- Must include: Success metric, verification method, failure conditions
- Example: "If we change product endpoint to use bulk API, then response time will improve by 50%"

**Deliverable:** *Hypothesis Statement* with clear pass/fail criteria

### **Phase 3: STRESS TEST — Verification & Review**
**Goal:** Test hypothesis against edge cases
- **Cross-API** endpoint testing
- **High-load** scenario validation
- **Error condition** handling  
- **Pagination** and filtering verification
- **API validator** compliance checks

**Deliverable:** *Stress Test Report* — where hypothesis holds/breaks

### **Phase 4: ADVERSARIAL REVIEW — Attempt to Break**
**Goal:** Actively try to disprove the hypothesis
- **"What if" scenarios**: Malformed data, rate limiting, timeouts
- **Regression hunting**: Does fix break something else?
- **Security lens**: How would an attacker exploit this?
- **Failure simulation**: What happens when dependent services fail?

**Deliverable:** *Adversarial Findings* — weaknesses to address

### **Phase 5: PROVE — Empirical Validation**
**Goal:** Demonstrate hypothesis is true
- **Before/after metrics** with timestamps
- **API response** comparisons
- **Performance validator** passes
- **Zero regression** evidence

**Deliverable:** *Proof Package* — incontrovertible evidence

### **Phase 6: IMPLEMENT — Surgical Deployment**
**Goal:** Apply validated fix to production
- **Atomic change**: One hypothesis at a time
- **Direct write** to production systems
- **Backup snapshots** remain untouched as **revert point**
- **Commit checkpoint** after each successful implementation

**Safety Net:** If implementation fails, revert to backup snapshot

### **Phase 7: VERIFY — Post-Implementation Proof**
**Goal:** Confirm fix works in production
- **Immediate**: HTTP status, error checks (0 errors)
- **24-hour**: Performance metrics comparison
- **7-day**: System stability confirmation
- **30-day**: Business metric improvements

**Deliverable:** *Verification Certificate* — fix is live and working

## ⚠️ FAILURE HANDLING PROTOCOL

### **Hypothesis Rejection Path**
```
Stress Test Failure → Document why → Return to Phase 2 (reformulate)
Adversarial Break → Document vulnerability → Return to Phase 2 (strengthen)  
Proof Incomplete → Document missing evidence → Return to Phase 5 (gather more)
```

### **Implementation Rollback Protocol**
1. **Detect regression** (monitoring alerts)
2. **Immediately revert** to backup snapshot
3. **Document failure** in hypothesis log
4. **Return to Phase 1** with new current state

## 🧪 VALIDATION STACK

### **Tier 1: Instant Verification** (Post-implementation)
- ✅ HTTP 200 on all endpoints
- ✅ Zero console errors
- ✅ API validator passes
- ✅ Performance benchmarks met

### **Tier 2: Short-term Proof** (24-48 hours)
- 📊 Response time improvements
- 📊 Error rate reduction
- 📊 System stability metrics

### **Tier 3: Long-term Evidence** (7-30 days)
- 📈 Business metric improvements
- 📈 User satisfaction increases
- 📈 System reliability gains

## ⚖️ ENFORCEMENT

This methodology is the **LAW** for all Shopify API work. Any deviation must be:
1. Documented as a controlled experiment
2. Approved via adversarial review
3. Reverted if regression detected

> **Scientia est potentia.** Knowledge is power. Empirical evidence is truth. Adversarial rigor is survival.