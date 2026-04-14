---
uid: voice_guidelines
tags:
  - brand-voice
  - bastelschachtel
  - reference
created: 2026-04-14
type: document
---

# Bastelschachtel — Voice Guidelines

## Quick Navigation

| Category | Files |
|----------|-------|
| **Core Brand Voice** | [[BASTELSCHACHTEL-BRAND-VOICE]] · [[brand_guidelines]] · [[tone_doc]] · [[forbidden_phrases]] |
| **Live Examples** | [[bastelschachtel-soul-first]] · [[example_subject]] |
| **Context** | [[product-marketing-context]] · [[marketing-handbook]] |

---

## Core Identity

Bastelschachtel is a family-run craft supply business in Wattens, Tirol. Five people. Hand-packed orders. A physical shop that smells like paper and glue. The voice is never corporate, never optimized, never performative.

The single test for every sentence:
> "Does this sound like a letter from a creative friend — or like a marketing campaign?"

If it sounds like marketing, rewrite it.

---

## The Voice in One Paragraph

Warm. Personal. Curious. A little unhurried. Like someone who genuinely loves what they do and assumes you will too, once you see it. Not selling — sharing. Not convincing — inviting. The reader should feel like she's being written to by someone who thought of her specifically, not someone who wrote to 8,000 people at once.

---

## Structural Voice Principles

### 1. Customer-centric, always
Never write from inside business goals. Always write from inside the customer's creative life.
- ✅ "Was wirst du diesen Frühling erschaffen?"
- ❌ "Q4 ist für uns die umsatzstärkste Zeit"

> See [[forbidden_phrases]] for the complete list of business interiority language to never use.

### 2. Personal, not performative
Informal "du" throughout. "Wir/uns" for the team, never "ich/mir" for an individual. Warm without being fake. Close without being creepy.

> See [[tone_doc]] for the calibrations on intimacy dimension.

### 3. Prose poetry structure
Each phrase earns its own breath. Line breaks are rhythm, not decoration. Sentences are short. Paragraphs are short. White space is part of the voice.

### 4. Permission, not pressure
She already wants to create. The brand's job is to open the door — not push her through it. Assume desire, remove barriers.

> See [[marketing-handbook]] Part 2, Section 2 for how this plays out in real customer service and abandoned cart emails.

### 5. Seasonal grounding
Seasons are not marketing hooks. They're real creative moments. Write about autumn because autumn is genuinely happening, not because it's Q4.

### 6. Implicit selling
The product exists inside the story, not as the headline. If done correctly, she discovers the shop the way you discover a recipe at a dinner party — through enthusiasm, not a pitch.

> See [[bastelschachtel-soul-first]] for real examples of implicit selling in action.

---

## Prose Poetry Format Rules

Each email reads as a series of short breath-units, not paragraphs. Format:

```
Eine neue Lieferung ist eingetroffen.

Rocailles in 60 Farben —
von tiefem Marineblau bis zu diesem bestimmten Grün,
das man nur im Frühling richtig benennen kann.

Wir haben sie gerade ausgepackt.
Noch nicht mal sortiert.
```

Rules:
- One idea per line, maximum two
- Line breaks signal pause, not list items
- No bullet points in newsletter text
- No bold headers within the letter section
- Rhythm > completeness

> See [[tone_doc]] for how prose poetry tone varies by email type.

---

## Sender Identity

Always from: **Bastelschachtel** or **das Bastelschachtel-Team**
Never from a named individual unless it is a genuinely personal story and the name is real.

Signature variants:
- Standard: "Herzliche Grüße aus Tirol, / Dein Team von der Bastelschachtel"
- Seasonal: "Kreative Frühlingsgrüße aus Wattens, / Dein Bastelschachtel-Team"
- Personal (rare): "Mit kreativen Grüßen aus der Werkstatt, / [Name] und das Bastelschachtel-Team"

> See [[BASTELSCHACHTEL-BRAND-VOICE]] Quick Reference for the complete signature guide.

---

## Tone Spectrum by Email Type

| Type | Tone | Energy |
|------|------|--------|
| Monthly Newsletter | Reflective, warm, literary | Slow, sit-down |
| New Arrivals | Excited but calm | Light, "hey, look at this" |
| Seasonal Kickoff | Anticipatory, inviting | Building warmth |
| Sale / Offers | Direct but never aggressive | Clear, no pressure |
| Customer Story | Grateful, moved | Quiet, sincere |

> See [[example_subject]] for subject line examples for each email type.
> See [[bastelschachtel-soul-first]] for real emails showing each type in practice.

---

## Voice Check (Run Before Every Send)

- [ ] Does this sound like a letter from a creative friend?
- [ ] Would she feel invited or pressured?
- [ ] Is there any manufactured urgency?
- [ ] Does it give permission rather than create guilt?
- [ ] Is it in warm, personal "du" form?
- [ ] Is the product secondary to the creative possibility?
- [ ] Would she want to sit down and read this?

> See [[BASTELSCHACHTEL-BRAND-VOICE]] Section 7 for the full Voice Check with 8 questions.

---

## See Also

### Inside This Folder

| Document | Description |
|----------|-------------|
| [[BASTELSCHACHTEL-BRAND-VOICE]] | Framework output with voice profile |
| [[brand_guidelines]] | Company identity and values |
| [[tone_doc]] | Emotional register and tone dimensions |
| [[forbidden_phrases]] | Never-use language and structural rules |
| [[example_subject]] | Email subject line examples |
| [[bastelschachtel-soul-first]] | Raw real emails (the source) |
| [[marketing-handbook]] | Assistant handbook with brand immersion |
| [[product-marketing-context]] | Product/audience bible |

### Outside This Folder

| Document | Path | Description |
|----------|------|-------------|
| Email Brand Voice Guide | [[docs/reference/email-brand-voice]] | Email-specific voice guide |
| SEO Brand Voice | [[docs/seo/brand-voice]] | SEO-specific voice document |
| VOC Split Bank | [[docs/customer-reviews/voc-split-bank]] | Amazon vs owned channel voice |
| Master Business Context | [[docs/strategy/master-business-context]] | Full strategy context |

---

*Date: 2026-04-14*



python3 -c "
import json, os
path = os.path.expanduser('~/.pi/agent/auth.json')
with open(path, 'r') as f:
	data = json.load(f)
data['openrouter'] = {'type': 'api_key', 'key': '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'}
with open(path, 'w') as f:
	json.dump(data, f, indent=2)
print('✓ Added OpenRouter to auth.json')
"