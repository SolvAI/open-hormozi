"""All 49 intake form questions — single source of truth.

Each question defines its type, options, conditional visibility,
and which documents it feeds into.
"""

from __future__ import annotations

from engine.models.form import QuestionSchema, QuestionType


# ─── SECTION 1: WHO ARE YOU ─────────────────────────────────────

Q1 = QuestionSchema(
    id="Q1",
    section=1,
    text="What best describes your business?",
    type=QuestionType.DROPDOWN,
    options=[
        "Freelance / independent consultant",
        "Agency / studio (2-10 people)",
        "Coach / trainer / expert",
        "Local business (restaurant, salon, retail, practice…)",
        "Tradesperson / home services",
        "E-commerce / online shop",
        "SaaS / digital product",
        "Other (specify)",
    ],
    maps_to=["U1", "U2", "U3", "U5", "U6", "BM4", "CH4", "CH5", "CH6", "MT3"],
)

Q2 = QuestionSchema(
    id="Q2",
    section=1,
    text="What's your industry / vertical?",
    type=QuestionType.TEXT,
    maps_to=["U2", "U5", "CH1", "CH4", "CH5"],
)

Q3 = QuestionSchema(
    id="Q3",
    section=1,
    text="How long have you been operating?",
    type=QuestionType.DROPDOWN,
    options=[
        "Not yet launched",
        "< 6 months",
        "6-18 months",
        "1.5-3 years",
        "3-8 years",
        "8+ years",
    ],
    maps_to=["U1", "U5"],
)

Q4 = QuestionSchema(
    id="Q4",
    section=1,
    text="Are you solo or do you have a team?",
    type=QuestionType.RADIO,
    options=[
        "Solo — just me",
        "Me + 1-2 people (freelancers/part-time)",
        "Team of 3-10",
        "Team of 10+",
    ],
    maps_to=["U1", "MT3"],
)

Q5 = QuestionSchema(
    id="Q5",
    section=1,
    text="Where are your customers?",
    type=QuestionType.RADIO,
    options=[
        "Local (city / region)",
        "National",
        "International",
        "Mix of local + national/international",
    ],
    maps_to=["U1", "BM3", "CH1", "CH2", "CH5"],
)

Q6 = QuestionSchema(
    id="Q6",
    section=1,
    text="Do you have a physical location where customers come to you?",
    type=QuestionType.RADIO,
    options=[
        "Yes — it's central to my business",
        "Yes — but most business happens remotely",
        "No — fully remote/online",
    ],
    maps_to=["BM3", "BM4", "CH5"],
)

# ─── SECTION 2: WHAT YOU SELL ───────────────────────────────────

Q7 = QuestionSchema(
    id="Q7",
    section=2,
    text="Describe what you sell in 2-3 sentences. What does the client get?",
    type=QuestionType.TEXTAREA,
    min_length=50,
    maps_to=["U3", "U5", "BM1", "FC1", "FC3", "CH1"],
)

Q8 = QuestionSchema(
    id="Q8",
    section=2,
    text="Is your core offer a…",
    type=QuestionType.RADIO,
    options=[
        "Service (you do something for them)",
        "Physical product",
        "Digital product (course, SaaS, template…)",
        "Mix of service + product",
    ],
    maps_to=["U3", "U4", "U6", "BM7"],
)

Q9 = QuestionSchema(
    id="Q9",
    section=2,
    text="How do you currently price?",
    type=QuestionType.DROPDOWN,
    options=[
        "Hourly rate",
        "Daily rate",
        "Fixed project price",
        "Monthly retainer / subscription",
        "Per-unit product price",
        "Tiered packages",
        "I haven't formalized pricing yet",
        "Mix / depends",
    ],
    maps_to=["U4", "U5"],
)

Q10 = QuestionSchema(
    id="Q10",
    section=2,
    text="What's your average deal size / transaction value?",
    type=QuestionType.DROPDOWN,
    options=[
        "< $100",
        "$100-500",
        "$500-2,000",
        "$2,000-5,000",
        "$5,000-15,000",
        "$15,000-50,000",
        "$50,000+",
        "Don't know",
    ],
    maps_to=["U3", "U4", "U7", "BM1", "BM5", "FC3", "CH1"],
)

Q11 = QuestionSchema(
    id="Q11",
    section=2,
    text="Can the same customer buy from you more than once?",
    type=QuestionType.RADIO,
    options=[
        "Yes — regularly (weekly/monthly)",
        "Yes — occasionally (few times/year)",
        "Sometimes — if they have a new need",
        "Rarely — mostly one-time",
    ],
    maps_to=["BM5", "U7"],
)

Q12 = QuestionSchema(
    id="Q12",
    section=2,
    text="Do you already have a structured offer? (packages, tiers, clear pricing page)",
    type=QuestionType.RADIO,
    options=[
        "Yes — clear packages with prices",
        "Somewhat — I have a general structure but it's flexible",
        "No — I quote case by case",
        "No — I haven't formalized anything",
    ],
    maps_to=["U3", "U4"],
)

# ─── SECTION 3: HOW THE SALE WORKS ─────────────────────────────

Q13 = QuestionSchema(
    id="Q13",
    section=3,
    text="Does a customer typically need to talk to you (or your team) before buying?",
    type=QuestionType.RADIO,
    options=[
        "Always — they can't buy without a conversation",
        "Usually — most do, some buy directly",
        "Rarely — most buy without talking to me",
        "Never — fully self-serve",
    ],
    maps_to=["BM1", "BM7", "U6"],
)

Q14 = QuestionSchema(
    id="Q14",
    section=3,
    text="Is your service delivered by appointment or scheduled sessions?",
    type=QuestionType.RADIO,
    options=["Yes", "No", "N/A (product business)"],
    conditional_on={"Q8": ["Service (you do something for them)", "Mix of service + product"]},
    maps_to=["BM2"],
)

Q15 = QuestionSchema(
    id="Q15",
    section=3,
    text="Is the engagement typically ongoing (retainer, subscription, recurring) or one-off?",
    type=QuestionType.RADIO,
    options=[
        "Ongoing — months or years",
        "Project-based — defined start/end",
        "One-time transaction",
        "Mix",
    ],
    maps_to=["BM6", "U3", "U7"],
)

Q16 = QuestionSchema(
    id="Q16",
    section=3,
    text="How long does it take from first contact to purchase?",
    type=QuestionType.DROPDOWN,
    options=[
        "Immediate (same day)",
        "A few days",
        "1-4 weeks",
        "1-3 months",
        "3+ months",
        "Don't know",
    ],
    maps_to=["U6", "FC2", "FC3", "FC4", "FC5"],
)

Q17 = QuestionSchema(
    id="Q17",
    section=3,
    text="Who makes the buying decision?",
    type=QuestionType.RADIO,
    options=[
        "The person I talk to",
        "They need approval from someone else (boss, partner, board)",
        "Committee / multiple stakeholders",
        "Consumer — decides alone",
        "Don't know",
    ],
    conditional_on={"Q13": [
        "Always — they can't buy without a conversation",
        "Usually — most do, some buy directly",
    ]},
    maps_to=["BM1"],
)

# ─── SECTION 4: YOUR NUMBERS ───────────────────────────────────

Q18 = QuestionSchema(
    id="Q18",
    section=4,
    text="What's your current monthly revenue?",
    type=QuestionType.DROPDOWN,
    options=[
        "$0 (pre-revenue)",
        "$1-2,000",
        "$2-5,000",
        "$5-10,000",
        "$10-20,000",
        "$20-50,000",
        "$50,000+",
    ],
    maps_to=["U1", "U4", "U7"],
)

Q19 = QuestionSchema(
    id="Q19",
    section=4,
    text="How many active clients / customers per month?",
    type=QuestionType.DROPDOWN,
    options=["0", "1-3", "4-10", "11-30", "30-100", "100+"],
    maps_to=["U1", "U7"],
)

Q20 = QuestionSchema(
    id="Q20",
    section=4,
    text="What % of your revenue comes from your single biggest client?",
    type=QuestionType.DROPDOWN,
    options=[
        "100% (one client)",
        "50-80%",
        "30-50%",
        "< 30%",
        "Revenue is spread evenly",
        "N/A",
    ],
    conditional_on={"Q18": [
        "$1-2,000", "$2-5,000", "$5-10,000",
        "$10-20,000", "$20-50,000", "$50,000+",
    ]},
    required=False,
    maps_to=["U1", "U3"],
)

Q21 = QuestionSchema(
    id="Q21",
    section=4,
    text="Revenue trend over the last 6 months?",
    type=QuestionType.RADIO,
    options=["Growing", "Stable", "Declining", "Irregular / unpredictable", "Too early to say"],
    conditional_on={"Q18": [
        "$1-2,000", "$2-5,000", "$5-10,000",
        "$10-20,000", "$20-50,000", "$50,000+",
    ]},
    required=False,
    maps_to=["U1"],
)

Q22 = QuestionSchema(
    id="Q22",
    section=4,
    text="What's your current profit margin (roughly)?",
    type=QuestionType.DROPDOWN,
    options=["< 20%", "20-40%", "40-60%", "60-80%", "80%+", "Don't know"],
    conditional_on={"Q18": [
        "$1-2,000", "$2-5,000", "$5-10,000",
        "$10-20,000", "$20-50,000", "$50,000+",
    ]},
    required=False,
    maps_to=["U4", "U7", "BM5"],
)

# ─── SECTION 5: HOW YOU GET CLIENTS TODAY ───────────────────────

Q23 = QuestionSchema(
    id="Q23",
    section=5,
    text="How do you currently get clients? (select all)",
    type=QuestionType.CHECKBOX,
    options=[
        "Word of mouth / referrals",
        "Marketplace (Malt, Upwork, Fiverr, Etsy…)",
        "My own website / inbound",
        "Social media (organic posts)",
        "Paid ads (Google, Meta, LinkedIn…)",
        "Cold outreach (email, DM, calls)",
        "Networking / events",
        "Partnerships / affiliates",
        "I don't have a system — it's random",
        "Other",
    ],
    maps_to=["U1", "CH6", "CH7"],
)

Q24 = QuestionSchema(
    id="Q24",
    section=5,
    text="Which single method brings the MOST revenue today?",
    type=QuestionType.DROPDOWN,
    options=[],  # dynamically filtered to Q23 selections at form level
    conditional_on={"Q23": "__multiple"},  # shown if Q23 has >1 selection
    required=False,
    maps_to=["U1", "CH6"],
)

Q25 = QuestionSchema(
    id="Q25",
    section=5,
    text="What have you tried that DIDN'T work? (select all)",
    type=QuestionType.CHECKBOX,
    options=[
        "Paid ads (wasted budget)",
        "Cold outreach (no responses)",
        "Content creation (no ROI)",
        "SEO (too slow)",
        "Networking (too time-consuming)",
        "Marketplace (race to bottom on price)",
        "Nothing — I haven't tried much yet",
        "Other (specify)",
    ],
    maps_to=["U1"],
)

Q26 = QuestionSchema(
    id="Q26",
    section=5,
    text="If you're on a marketplace, how dependent are you?",
    type=QuestionType.RADIO,
    options=[
        "It's my only source of clients",
        "It's my main source (>50%)",
        "It's one of several",
        "I'm not on any marketplace",
    ],
    conditional_on={"Q23": ["Marketplace (Malt, Upwork, Fiverr, Etsy…)"]},
    required=False,
    maps_to=["CH7"],
)

Q27 = QuestionSchema(
    id="Q27",
    section=5,
    text="Do you currently spend money on acquisition? If yes, how much/month?",
    type=QuestionType.DROPDOWN,
    options=[
        "$0 — nothing",
        "$1-200/mo",
        "$200-500/mo",
        "$500-1,500/mo",
        "$1,500-3,000/mo",
        "$3,000+/mo",
    ],
    maps_to=["U7"],
)

# ─── SECTION 6: WHAT YOU ALREADY HAVE ──────────────────────────

Q28 = QuestionSchema(
    id="Q28",
    section=6,
    text="Do you have a website?",
    type=QuestionType.RADIO,
    options=[
        "Yes — professional, up to date",
        "Yes — but outdated or basic",
        "No",
    ],
    maps_to=["FC1", "MT3"],
)

Q29 = QuestionSchema(
    id="Q29",
    section=6,
    text="Website URL (if applicable)",
    type=QuestionType.TEXT,
    required=False,
    conditional_on={"Q28": [
        "Yes — professional, up to date",
        "Yes — but outdated or basic",
    ]},
    maps_to=["U5", "FC1", "MT1"],
)

Q30 = QuestionSchema(
    id="Q30",
    section=6,
    text="Do you have an email list?",
    type=QuestionType.RADIO,
    options=["Yes — 500+", "Yes — under 500", "No"],
    maps_to=["FC2", "FC4"],
)

Q31 = QuestionSchema(
    id="Q31",
    section=6,
    text="Do you have social media presence? (select active ones)",
    type=QuestionType.CHECKBOX,
    options=[
        "LinkedIn",
        "Instagram",
        "Facebook",
        "YouTube",
        "TikTok",
        "Twitter/X",
        "None active",
    ],
    maps_to=["CH4", "FC5"],
)

Q32 = QuestionSchema(
    id="Q32",
    section=6,
    text="How would you rate your existing proof and credibility?",
    type=QuestionType.RADIO,
    options=[
        "Strong — portfolio, testimonials, case studies, media/speaking",
        "Moderate — some client results, a few testimonials",
        "Weak — I have experience but nothing documented",
        "None — starting from scratch",
    ],
    maps_to=["U3", "MT1", "MT2", "FC1", "BM1"],
)

Q33 = QuestionSchema(
    id="Q33",
    section=6,
    text="Can you list 2-3 concrete results you've achieved for clients? (even informal)",
    type=QuestionType.TEXTAREA,
    required=False,
    conditional_on={"Q32": [
        "Strong — portfolio, testimonials, case studies, media/speaking",
        "Moderate — some client results, a few testimonials",
        "Weak — I have experience but nothing documented",
    ]},
    maps_to=["MT1", "FC1", "BM1"],
)

# ─── SECTION 7: WHO YOU WANT TO REACH ──────────────────────────

Q34 = QuestionSchema(
    id="Q34",
    section=7,
    text="Describe your ideal client/customer in a few sentences. Who are they? What's their situation?",
    type=QuestionType.TEXTAREA,
    min_length=80,
    maps_to=["U2", "U5", "BM1", "FC1", "CH1", "CH2", "CH3"],
)

Q35 = QuestionSchema(
    id="Q35",
    section=7,
    text="What's the #1 problem you solve for them?",
    type=QuestionType.TEXTAREA,
    maps_to=["U2", "U3", "U5", "FC1", "FC3", "CH1"],
)

Q36 = QuestionSchema(
    id="Q36",
    section=7,
    text="What happens if they DON'T solve this problem? (consequences of inaction)",
    type=QuestionType.TEXTAREA,
    maps_to=["U5", "BM1", "FC1", "FC3", "BM5"],
)

Q37 = QuestionSchema(
    id="Q37",
    section=7,
    text="What do they currently do instead of hiring/buying from you?",
    type=QuestionType.TEXTAREA,
    maps_to=["U2", "U3", "U5", "BM1"],
)

Q38 = QuestionSchema(
    id="Q38",
    section=7,
    text="If B2B: what size companies are you targeting?",
    type=QuestionType.DROPDOWN,
    options=[
        "1-10 employees",
        "10-50",
        "50-200",
        "200-1000",
        "1000+",
        "Doesn't matter",
        "N/A (B2C)",
    ],
    required=False,
    maps_to=["U2", "CH1", "CH3"],
)

Q39 = QuestionSchema(
    id="Q39",
    section=7,
    text="If B2B: what's the buyer's role?",
    type=QuestionType.DROPDOWN,
    options=[
        "CEO / founder",
        "CTO / technical director",
        "COO / operations",
        "CMO / marketing",
        "HR director",
        "Procurement",
        "End user (not decision maker)",
        "Don't know",
        "N/A",
    ],
    required=False,
    maps_to=["U2", "CH1", "CH3", "BM1"],
)

# ─── SECTION 8: WHERE YOU WANT TO GO ───────────────────────────

Q40 = QuestionSchema(
    id="Q40",
    section=8,
    text="What's your monthly revenue target?",
    type=QuestionType.DROPDOWN,
    options=[
        "$2-5k/mo",
        "$5-10k/mo",
        "$10-20k/mo",
        "$20-50k/mo",
        "$50-100k/mo",
        "$100k+/mo",
    ],
    maps_to=["U4", "U7", "U9"],
)

Q41 = QuestionSchema(
    id="Q41",
    section=8,
    text="By when?",
    type=QuestionType.DROPDOWN,
    options=[
        "3 months",
        "6 months",
        "12 months",
        "18-24 months",
        "No rush — I want sustainable growth",
    ],
    maps_to=["U9"],
)

Q42 = QuestionSchema(
    id="Q42",
    section=8,
    text="What's your PRIMARY bottleneck right now?",
    type=QuestionType.RADIO,
    options=[
        "Nobody knows I exist — I need visibility",
        "People know me but don't reach out — I need lead generation",
        "I get leads but can't close them — I need conversion help",
        "I close but my prices are too low — I need pricing/packaging help",
        "I get clients but they leave or don't come back — I need retention",
        "I have too much work but the wrong kind — I need better positioning",
        "I honestly don't know",
    ],
    maps_to=["U1"],
)

Q43 = QuestionSchema(
    id="Q43",
    section=8,
    text="What does your ideal week look like in 12 months? (how many clients, what type of work, how many hours)",
    type=QuestionType.TEXTAREA,
    maps_to=["U3", "U4"],
)

# ─── SECTION 9: YOUR RESOURCES ─────────────────────────────────

Q44 = QuestionSchema(
    id="Q44",
    section=9,
    text="How much can you invest monthly in acquisition (ads, tools, freelancer help)?",
    type=QuestionType.DROPDOWN,
    options=[
        "$0 — bootstrapping",
        "$1-200/mo",
        "$200-500/mo",
        "$500-1,500/mo",
        "$1,500-3,000/mo",
        "$3,000-5,000/mo",
        "$5,000+/mo",
        "I'll invest whatever works (ROI-driven)",
    ],
    maps_to=["U7", "CH1", "CH2", "FC5", "MT3"],
)

Q45 = QuestionSchema(
    id="Q45",
    section=9,
    text="How many hours/week can you dedicate to marketing & sales? (not client delivery)",
    type=QuestionType.DROPDOWN,
    options=[
        "< 2 hours",
        "2-5 hours",
        "5-10 hours",
        "10-20 hours",
        "I want to spend ZERO — automate everything",
    ],
    maps_to=["U9", "MT3"],
)

Q46 = QuestionSchema(
    id="Q46",
    section=9,
    text="Time vs money — where do you sit?",
    type=QuestionType.RADIO,
    options=[
        "I have more time than money — I'll do the work",
        "Balanced — I can invest some of each",
        "I have more money than time — I'll pay for speed",
        "I want to buy a system — don't make me build slowly",
    ],
    maps_to=["U9", "MT3"],
)

Q47 = QuestionSchema(
    id="Q47",
    section=9,
    text="Technical comfort — can you… (select all that apply)",
    type=QuestionType.CHECKBOX,
    options=[
        "Build a simple website / landing page (no-code)",
        "Set up and manage Google Ads",
        "Set up email automation (Zapier, Mailchimp…)",
        "Edit images / basic design (Canva)",
        "Write persuasive copy",
        "None of the above — I need help with everything",
    ],
    maps_to=["MT3", "U9"],
)

# ─── SECTION 10: HARD NOS & CONTEXT ────────────────────────────

Q48 = QuestionSchema(
    id="Q48",
    section=10,
    text="Is there anything you absolutely REFUSE to do? (select all)",
    type=QuestionType.CHECKBOX,
    options=[
        "Create content regularly (posts, videos, articles)",
        "Show my face on camera",
        "Cold call / cold DM people",
        "Spend money on ads",
        "Lower my prices",
        "Offer free consultations",
        "Use social media at all",
        "Nothing — I'm open to everything",
    ],
    maps_to=["U1"],
)

Q49 = QuestionSchema(
    id="Q49",
    section=10,
    text="Is there anything else about your situation that we should know?",
    type=QuestionType.TEXTAREA,
    required=False,
    maps_to=["U1"],
)


# ─── Master registry ────────────────────────────────────────────

QUESTIONS: dict[str, QuestionSchema] = {
    q.id: q
    for q in [
        Q1, Q2, Q3, Q4, Q5, Q6,
        Q7, Q8, Q9, Q10, Q11, Q12,
        Q13, Q14, Q15, Q16, Q17,
        Q18, Q19, Q20, Q21, Q22,
        Q23, Q24, Q25, Q26, Q27,
        Q28, Q29, Q30, Q31, Q32, Q33,
        Q34, Q35, Q36, Q37, Q38, Q39,
        Q40, Q41, Q42, Q43,
        Q44, Q45, Q46, Q47,
        Q48, Q49,
    ]
}

QUESTIONS_BY_SECTION: dict[int, list[QuestionSchema]] = {}
for q in QUESTIONS.values():
    QUESTIONS_BY_SECTION.setdefault(q.section, []).append(q)


def get_question(question_id: str) -> QuestionSchema:
    """Get a question by ID. Raises KeyError if not found."""
    return QUESTIONS[question_id]