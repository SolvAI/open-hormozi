"""Few-shot examples for strategy prompts.

Each example is a (form_answers_formatted, diagnostic_output) pair.
These demonstrate REASONING, not templates to copy.
"""

# ─── Example 1: Sam (Freelance Developer) ────────────────────

THOMAS_FORM = """## Client Form Answers

- **Q1**: Freelance / independent consultant
- **Q2**: Web & mobile development, SaaS
- **Q3**: 3-8 years
- **Q4**: Solo — just me
- **Q5**: National
- **Q6**: No — fully remote/online
- **Q7**: "I design and develop custom web and mobile applications for startups and SMBs. I manage the entire cycle: technical architecture, development, deployment. Clients come with a business problem and leave with a working product in production."
- **Q8**: Service (you do something for them)
- **Q9**: Daily rate
- **Q10**: $2,000-5,000
- **Q11**: Sometimes — if they have a new need
- **Q12**: No — I quote case by case
- **Q13**: Always — they can't buy without a conversation
- **Q14**: No
- **Q15**: Project-based — defined start/end
- **Q16**: 1-4 weeks
- **Q17**: They need approval from someone else (boss, partner, board)
- **Q18**: $2-5,000
- **Q19**: 1-3
- **Q20**: 50-80%
- **Q21**: Stable
- **Q22**: 80%+
- **Q23**: ☑ Marketplace (Malt) · ☑ Word of mouth / referrals
- **Q24**: Marketplace (Malt)
- **Q25**: ☑ Cold outreach (no responses) · ☑ Content creation (no ROI)
- **Q26**: It's my main source (>50%)
- **Q27**: $0 — nothing
- **Q28**: Yes — but outdated or basic
- **Q29**: www.example-dev.com
- **Q30**: No
- **Q31**: ☑ LinkedIn
- **Q32**: Moderate — some client results, a few testimonials
- **Q33**: "Developed an MVP SaaS for a fintech that raised $2M after launch. Migrated a legacy PHP app to a modern stack for an SMB — hosting costs reduced by 60%. Mobile app for a retail chain: 15k downloads in the first month."
- **Q34**: "CTOs or founders of tech startups and SMBs, 10-50 employees, who need to build or rebuild a technical product but don't have the in-house team."
- **Q35**: "They need a senior lead dev who can make architecture decisions independently, not just code tickets."
- **Q36**: "They accumulate technical debt, the product slows down, bugs pile up, they lose users. After 18 months they have to rewrite everything from scratch — $100k+ lost."
- **Q37**: "They compare 20 profiles on Malt by daily rate. Or they go to agencies. Or they try to hire a CTO — that takes 6 months and costs $80k+. Or offshore at $200/day."
- **Q38**: 10-50 employees
- **Q39**: CTO / technical director
- **Q40**: $10-20k/mo
- **Q41**: 6 months
- **Q42**: Nobody knows I exist — I need visibility
- **Q43**: "2-3 clients max in parallel, projects at $5-15k each. 4 days of dev per week, 0 days of prospecting."
- **Q44**: $500-1,500/mo
- **Q45**: 2-5 hours
- **Q46**: I have more money than time — I'll pay for speed
- **Q47**: ☑ Build a simple website / landing page (no-code) · ☑ Write persuasive copy
- **Q48**: ☑ Create content regularly (posts, videos, articles) · ☑ Show my face on camera
- **Q49**: "I'm good at my job but I hate selling. I want a system that brings me qualified leads."
"""

THOMAS_DIAGNOSTIC = """## Derived Meta-Variables

| Variable | Value | Rationale |
|----------|-------|-----------|
| Maturity | **GROWING** | $4.2k/mo average, 3-8 years experience, moderate proof (3 strong results but not systematized) |
| Bottleneck | **Visibility** | Self-identified, validated: $0 acquisition spend, >50% Malt dependency, no owned channel |
| Resource | **MONEY_RICH** | $500-1,500 budget, only 2-5h/week, explicit preference for paid speed |
| Ambition | **GROWTH** | 2.4x multiplier ($4.2k → $10-20k), 6-month timeline, wants system not hustle |

## Triggered Documents

| Doc | Triggered | Reason |
|-----|-----------|--------|
| U1-U9 | ✅ | Universal — always |
| BM1 | ✅ | Q13 = "always" — consultative sale required |
| BM2 | ❌ | Q14 = "no" — not appointment-based |
| BM3 | ❌ | Q6 = "no, fully remote" — no physical location |
| BM4 | ❌ | Q6 = "no" — no on-site interaction |
| BM5 | ❌ | Q11 = "sometimes" — not regular repeat. Borderline, but project-based repeat is opportunistic, not systematic |
| BM6 | ✅ | Q15 = "project-based" — needs scope/contract management for $5-15k projects |
| BM7 | ❌ | Q13 = "always" — not self-serve |
| CH1 | ✅ | **Primary channel** — see scoring below |
| CH2-CH7 | ❌ | Not primary — see scoring below. CH7 flagged as transitional in U1. |
| FC1 | ✅ | CH1 (paid) drives to a landing page |
| FC2 | ✅ | BM1 exists (nurture not-qualified leads) + Q16 ≥ 1-4 weeks |
| FC3 | ❌ | Q10 = $2-5k — borderline but not high enough for webinar funnel; sales call is the conversion event |
| FC4 | ✅ | Digital funnel exists. Sequences: qualified_confirmation, not_qualified_lead_magnet, post_call_sold, post_call_not_sold |
| FC5 | ✅ | CH1 primary + Q44 ≥ $500 (budget allows 10-15% retargeting) |
| MT1 | ✅ | Q32 = "moderate" — has results to systematize |
| MT2 | ❌ | Q32 ≠ weak/none |
| MT3 | ✅ | Q4 = "solo" |

## Channel Scoring

| Channel | Score | Key Factors |
|---------|-------|-------------|
| CH1 (SEA) | **85** | +conversation required, +deal ≥$2k, +budget, +national, +money>time. −none |
| CH2 (Social) | 35 | −not visual product, −B2B, −not local radius |
| CH3 (Outbound) | 40 | +B2B identifiable targets, +deal size. −Q25 cold outreach failed, −low time |
| CH4 (Organic) | 10 | −hard no on content creation, −hard no on camera |
| CH5 (Local) | 0 | −not local |
| CH6 (Referral) | 40 | +WOM works informally. −not scalable alone, −not enough volume |
| CH7 (Marketplace) | transitional | Currently >50% dependent. Flag migration in U1, not a growth channel. |

**Primary: CH1 (SEA). Secondary: none. CH7 migration plan embedded in U1.**

## Validation Flags

- ⚠ **Revenue concentration**: Q20 = 50-80% from top client → high risk. Flag in U1 as urgency driver for diversification.
- ⚠ **Daily rate pricing model**: Q9 = daily rate → must restructure to project/value pricing. U4 priority.
- ℹ **Niche hesitation**: Q49 mentions fintech/healthtech indecision → address in U2: recommend soft-niche via LP messaging, not hard commitment yet.

## Key Content Angles

1. Position as "Senior Lead Dev / Outsourced CTO" — NOT "freelance developer"
2. Pain angle: technical debt, mediocre agencies, impossible CTO recruitment
3. Proof weapons: $2M raise, -60% hosting costs, 15k downloads — deploy everywhere
4. Kill the daily rate: move to project-based or monthly retainer pricing
5. Malt migration: systematic transition from marketplace dependency to owned pipeline
6. Revenue concentration: diversify client base as urgency driver

## Priority Order

U1 → U2 → U5 → U3 → U4 → CH1 → FC1 → MT1 → BM1 → FC2 → FC4 → FC5 → BM6 → U6 → U7 → U8 → U9 → MT3
"""

# ─── Example 2: Restaurant ──────────────────────────────────────

RESTAURANT_FORM = """## Client Form Answers

- **Q1**: Local business (restaurant, salon, retail, practice…)
- **Q2**: Restaurant — traditional bistro
- **Q3**: 3-8 years
- **Q4**: Team of 3-10
- **Q5**: Local (city / region)
- **Q6**: Yes — it's central to my business
- **Q7**: "Neighborhood bistro in Lyon's 6th arrondissement, revisited traditional French cuisine. Lunch menu for local office workers, evening menu for couples and families. We also host private events for groups of up to 30 people."
- **Q8**: Mix of service + product
- **Q9**: Per-unit product price
- **Q10**: < $100
- **Q11**: Yes — regularly (weekly/monthly)
- **Q12**: No — I haven't formalized anything
- **Q13**: Never — fully self-serve
- **Q14**: Yes
- **Q15**: One-time transaction
- **Q16**: Immediate (same day)
- **Q17**: (not shown)
- **Q18**: $20-50,000
- **Q19**: 100+
- **Q20**: Revenue is spread evenly
- **Q21**: Irregular / unpredictable
- **Q22**: < 20%
- **Q23**: ☑ Word of mouth / referrals · ☑ My own website / inbound
- **Q24**: Word of mouth / referrals
- **Q25**: ☑ Paid ads (wasted budget)
- **Q26**: I'm not on any marketplace
- **Q27**: $0 — nothing
- **Q28**: Yes — but outdated or basic
- **Q29**: www.example-bistro.com
- **Q30**: No
- **Q31**: ☑ Instagram · ☑ Facebook
- **Q32**: Moderate — some client results, a few testimonials
- **Q33**: "4.4 stars on Google with 380+ reviews. Mentioned in Lyon Capitale 'best bouchons 2023'. Regulars who come every week for 3 years. Truffle evening in January: fully booked 3 weeks ahead, 120 covers at $65/person."
- **Q34**: "3 profiles: (1) Office workers within a 500m radius for lunch. (2) Couples aged 30-55 for dinner. (3) Local businesses for private events of 10-30 people."
- **Q35**: "For lunch: eat well and fresh near the office without losing 1.5 hours. For dinner: a special moment in a real Lyonnais bistro. For events: a privatizable space with a proper menu."
- **Q36**: "They eat a sandwich at the office, order on Uber Eats, or go to Flunch. For evenings they stay home. For events they book a generic venue."
- **Q37**: "The 15+ other restaurants within a 500m radius. UberEats. The company cafeteria. Cooking at home."
- **Q38**: N/A (B2C)
- **Q39**: N/A
- **Q40**: $50-100k/mo
- **Q41**: 12 months
- **Q42**: I close but my prices are too low — I need pricing/packaging help
- **Q43**: "Lunch: fully booked every day (50 covers, currently 30-35). Evening: fully booked Thursday-Saturday, 70% Tuesday-Wednesday. 4+ private events per month."
- **Q44**: $200-500/mo
- **Q45**: 2-5 hours
- **Q46**: Balanced — I can invest some of each
- **Q47**: ☑ Edit images / basic design (Canva)
- **Q48**: ☑ Cold call / cold DM people
- **Q49**: "Our food is great — everyone says so. Our problem is we're invisible online. The website looks like it's from 2015. Our Instagram has 800 followers and we post once a month. Full on Friday-Saturday evenings but Tuesday-Wednesday is dead. We tried a Facebook boost at $15 once, zero results."
"""

RESTAURANT_DIAGNOSTIC = """## Derived Meta-Variables

| Variable | Value | Rationale |
|----------|-------|-----------|
| Maturity | **ESTABLISHED** | ~$29k/mo, 3-8 years, 380+ Google reviews, press mention, loyal regulars |
| Bottleneck | **Pricing + Visibility (dual)** | Self-identified pricing. Q49 reveals visibility equally critical. Dual bottleneck flagged. |
| Resource | **BALANCED** | $200-500 budget, 2-5h/week, willing to invest some of each |
| Ambition | **GROWTH** | ~2x multiplier ($29k → $50-100k), 12-month timeline, wants to hire sous-chef |

## Triggered Documents

| Doc | Triggered | Reason |
|-----|-----------|--------|
| U1-U9 | ✅ | Universal — always |
| BM1 | ❌ | Q13 = "never" — no consultative sale. Event inquiries handled as mini-section in BM4. |
| BM2 | ✅ | Q14 = "yes" — reservations are appointment-based |
| BM3 | ✅ | Q6 = "yes, central" — physical location |
| BM4 | ✅ | Q6 = "yes, central" — on-site experience is the product |
| BM5 | ✅ | Q11 = "regularly" — weekly/monthly repeat customers |
| BM6 | ❌ | Q15 = "one-time transaction" — no ongoing engagement |
| BM7 | ✅ | Q13 = "never" — self-serve online booking/reservation optimization |
| CH1 | ❌ | Deal <$100, local radius too small for search volume, CPC won't pay back |
| CH2 | ✅ | **Primary channel** — local radius ✓, visual (food!) ✓, B2C ✓, budget ok, Instagram exists |
| CH3 | ❌ | B2C, hard no on cold outreach |
| CH4 | ❌ | Not primary. Folded as secondary recommendation: "post 3x/week on Instagram" inside CH2 |
| CH5 | ❌ | Strong runner-up (score 65), flagged for Month 3 addition in U9. BM3 covers baseline. |
| CH6 | ❌ | WOM already works. Mechanics systematized inside BM5 (referral for regulars). |
| CH7 | ❌ | Not on marketplace |
| FC1 | ✅ | Needs modern site with reservation CTA + event inquiry |
| FC2 | ❌ | No nurture funnel. Not relevant for a restaurant. |
| FC3 | ❌ | Not applicable |
| FC4 | ✅ | Sequences: review_request, re_engagement_lapsed, referral_ask |
| FC5 | ❌ | Budget too low to split ($200-500). Revisit when budget ≥$1k. |
| MT1 | ✅ | Q32 = "moderate" + 380 reviews + press mention = strong proof to weaponize |
| MT2 | ❌ | Has proof |
| MT3 | ✅ | Team of 3-10 but no marketing sophistication, needs simple tools |

## Channel Scoring

| Channel | Score | Key Factors |
|---------|-------|-------------|
| CH1 (SEA) | 20 | −deal <$100, −local radius too small, −CPC won't pay back |
| CH2 (Social) | **80** | +local radius, +visual (food!), +B2C, +budget ok, +Instagram exists |
| CH3 (Outbound) | 0 | −B2C, −hard no on cold outreach |
| CH4 (Organic) | 55 | +viable (food content is natural), −they post 1x/month (execution gap) |
| CH5 (Local SEO) | 65 | +strong runner-up, +GBP at 4.4★, −slower ROI than social ads |
| CH6 (Referral) | 50 | +WOM already works, −not scalable alone |
| CH7 (Marketplace) | 0 | −not on one |

**Primary: CH2 (Social Ads). CH5 flagged for Month 3. CH6 mechanics embedded in BM5.**

## Validation Flags

- ⚠ **Pricing vs margin mismatch**: Q42 = "prices too low" + Q22 = "<20%" margin + Q49 mentions supplier costs → CONFIRMED. U4 must address both menu repricing AND food cost structure.
- ⚠ **Fake ad test**: Q25 = "paid ads didn't work" but Q49 reveals $15 Facebook boost → not a real test. Flag in U1: "You haven't actually tried paid ads."
- ⚠ **Margin before volume**: Q40 = double revenue but Q22 = <20% margin → doubling at current margins won't solve profitability. U7 must model: improved margin × 1.5x volume vs current margin × 2x volume. Prescription: fix margins FIRST.

## Key Content Angles

1. **Pricing is the #1 lever** — menu engineering before ad spend. Kill low-margin dishes, promote high-margin. Introduce "experience" menus ($38/person wine-paired).
2. **Empty weeknights are the real problem** — target Tuesday-Wednesday-Thursday with specific offers, not Friday-Saturday (already full).
3. **Events are the profit rocket** — $65/person × 30 = $1,950/event at high margin. Build dedicated event funnel.
4. **4.4★ with 380 reviews is gold** — weaponize across all touchpoints.
5. **Instagram is the natural channel** — food is visual. Need content rhythm (3x/week minimum) alongside paid.
6. **Fix margins before scaling volume** — U7 must show the math.

## Priority Order

U1 → U4 → U3 → U5 → BM4 → BM5 → CH2 → FC1 → BM3 → BM7 → BM2 → MT1 → FC4 → U6 → U7 → U8 → U9 → MT3
"""