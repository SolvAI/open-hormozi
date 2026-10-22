"""Deterministic trigger logic: form answers → document triggers + channel scores.

This runs BEFORE the LLM strat prompt as a mechanical baseline.
The LLM can override with judgment (edge cases), but disagreements are flagged.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.models.enums import (
    AmbitionProfile,
    Bottleneck,
    Channel,
    DocID,
    Maturity,
    ResourceProfile,
)
from engine.models.form import FormAnswers
from engine.models.diagnostic import MetaVariables, ChannelScore, ChannelScores


# ─── Revenue midpoint estimates for calculations ────────────────

_REVENUE_MIDPOINTS = {
    "$0 (pre-revenue)": 0,
    "$1-2,000": 1500,
    "$2-5,000": 3500,
    "$5-10,000": 7500,
    "$10-20,000": 15000,
    "$20-50,000": 35000,
    "$50,000+": 75000,
}

_TARGET_MIDPOINTS = {
    "$2-5k/mo": 3500,
    "$5-10k/mo": 7500,
    "$10-20k/mo": 15000,
    "$20-50k/mo": 35000,
    "$50-100k/mo": 75000,
    "$100k+/mo": 150000,
}

_DEAL_MIDPOINTS = {
    "< $100": 50,
    "$100-500": 300,
    "$500-2,000": 1250,
    "$2,000-5,000": 3500,
    "$5,000-15,000": 10000,
    "$15,000-50,000": 32500,
    "$50,000+": 75000,
    "Don't know": 0,
}

_BUDGET_MIDPOINTS = {
    "$0 — bootstrapping": 0,
    "$100-500/mo": 300,
    "$500-1,500/mo": 1000,
    "$1,500-3,000/mo": 2250,
    "$3,000-5,000/mo": 4000,
    "$5,000+/mo": 7500,
    "I'll invest whatever works (ROI-driven)": 3000,
}

_OPERATING_YEARS = {
    "Not yet launched": 0,
    "< 6 months": 0.25,
    "6-18 months": 1,
    "1.5-3 years": 2.25,
    "3-8 years": 5,
    "8+ years": 10,
}


class TriggerEngine:
    """Derive meta-variables, document triggers, and channel scores from form answers."""

    def __init__(self, form: FormAnswers):
        self.form = form
        self._revenue = _REVENUE_MIDPOINTS.get(form.monthly_revenue, 0)
        self._target = _TARGET_MIDPOINTS.get(form.get("Q40", ""), 0)
        self._deal = _DEAL_MIDPOINTS.get(form.deal_size, 0)
        self._budget = _BUDGET_MIDPOINTS.get(form.get("Q44", ""), 0)
        self._years = _OPERATING_YEARS.get(form.get("Q3", ""), 0)

    # ─── Meta-Variables ──────────────────────────────────────

    def derive_maturity(self) -> tuple[Maturity, str]:
        q18 = self._revenue
        q3 = self._years
        q32 = self.form.proof_level

        is_weak_proof = q32 in (
            "Weak — I have experience but nothing documented",
            "None — starting from scratch",
        )
        is_strong_proof = q32 in (
            "Strong — portfolio, testimonials, case studies, media/speaking",
            "Moderate — some client results, a few testimonials",
        )

        # Pivot: experienced person, new business
        if q18 == 0 and q3 >= 8:
            return Maturity.PIVOT, (
                f"Pre-revenue but {self.form.get('Q3')} operating experience. "
                "Experienced professional starting a new venture."
            )

        # Starter
        if q18 <= 1500 and q3 <= 1 and is_weak_proof:
            return Maturity.STARTER, (
                f"Revenue ${q18}/mo, operating {self.form.get('Q3')}, "
                f"proof level: {q32}. Early stage."
            )

        # Established
        if q18 >= 10000 and q3 >= 3 and is_strong_proof:
            return Maturity.ESTABLISHED, (
                f"Revenue ${q18}/mo, operating {self.form.get('Q3')}, "
                f"proof level: {q32}. Established business."
            )

        # Growing (default middle)
        return Maturity.GROWING, (
            f"Revenue ${q18}/mo, operating {self.form.get('Q3')}, "
            f"proof level: {q32}. Growing business with traction."
        )

    def derive_bottleneck(self) -> tuple[Bottleneck, str]:
        q42 = self.form.bottleneck_answer

        mapping = {
            "Nobody knows I exist — I need visibility": Bottleneck.VISIBILITY,
            "People know me but don't reach out — I need lead generation": Bottleneck.LEAD_GENERATION,
            "I get leads but can't close them — I need conversion help": Bottleneck.CONVERSION,
            "I close but my prices are too low — I need pricing/packaging help": Bottleneck.PRICING,
            "I get clients but they leave or don't come back — I need retention": Bottleneck.RETENTION,
            "I have too much work but the wrong kind — I need better positioning": Bottleneck.WRONG_CLIENTS,
        }

        if q42 in mapping:
            return mapping[q42], f"Self-identified: '{q42}'"

        # "I honestly don't know" → derive from numbers
        clients = self.form.get("Q19", "0")
        client_count_low = clients in ("0", "1-3")

        if client_count_low and self._revenue <= 5000:
            return Bottleneck.VISIBILITY, (
                "Self-reported 'don't know'. Derived from low client count + low revenue → visibility."
            )
        if not client_count_low and self._revenue <= 5000:
            return Bottleneck.PRICING, (
                "Self-reported 'don't know'. Derived from decent client count but low revenue → pricing."
            )
        trend = self.form.get("Q21", "")
        if trend == "Declining":
            return Bottleneck.RETENTION, (
                "Self-reported 'don't know'. Revenue declining → retention or market shift."
            )

        return Bottleneck.VISIBILITY, "Self-reported 'don't know'. Defaulting to visibility."

    def derive_resource(self) -> tuple[ResourceProfile, str]:
        budget = self._budget
        hours = self.form.get("Q45", "")
        pref = self.form.get("Q46", "")

        hours_low = hours in ("< 2 hours", "2-5 hours", "I want to spend ZERO — automate everything")
        hours_high = hours in ("10-20 hours", "5-10 hours")
        money_pref = pref in ("I have more money than time — I'll pay for speed",
                              "I want to buy a system — don't make me build slowly")
        time_pref = pref == "I have more time than money — I'll do the work"

        if budget >= 1500 and hours_low and money_pref:
            return ResourceProfile.MONEY_RICH, (
                f"Budget ${budget}/mo, {hours}/week, preference: '{pref}'"
            )

        if budget <= 500 and hours_high and time_pref:
            return ResourceProfile.TIME_RICH, (
                f"Budget ${budget}/mo, {hours}/week, preference: '{pref}'"
            )

        if budget <= 200 and hours in ("< 2 hours",):
            return ResourceProfile.CONSTRAINED, (
                f"Budget ${budget}/mo, {hours}/week. Neither time nor money available."
            )

        return ResourceProfile.BALANCED, (
            f"Budget ${budget}/mo, {hours}/week, preference: '{pref}'"
        )

    def derive_ambition(self) -> tuple[AmbitionProfile, str]:
        current = self._revenue
        target = self._target
        timeline = self.form.get("Q41", "")
        trend = self.form.get("Q21", "")
        q43 = self.form.get("Q43", "")
        q42 = self.form.bottleneck_answer

        multiplier = target / current if current > 0 else float("inf")

        # Survival
        if trend == "Declining" and timeline == "3 months":
            return AmbitionProfile.SURVIVAL, (
                f"Revenue declining, 3-month timeline, bottleneck: '{q42}'. Urgent."
            )

        # Lifestyle
        lifestyle_signals = any(
            w in (q43 or "").lower()
            for w in ["freedom", "few clients", "select", "choose",
                      "calm", "balance"]
        )
        if target <= 10000 and lifestyle_signals:
            return AmbitionProfile.LIFESTYLE, (
                f"Target ${target}/mo, lifestyle signals in Q43. Optimize for margin + freedom."
            )

        # Aggressive
        if multiplier > 5 or (target >= 50000 and timeline in ("3 months", "6 months")):
            return AmbitionProfile.AGGRESSIVE, (
                f"{multiplier:.1f}x multiplier (${current} → ${target}), timeline: {timeline}"
            )

        # Growth (default)
        return AmbitionProfile.GROWTH, (
            f"{multiplier:.1f}x multiplier (${current} → ${target}), timeline: {timeline}"
        )

    def derive_meta_variables(self) -> MetaVariables:
        mat, mat_r = self.derive_maturity()
        bot, bot_r = self.derive_bottleneck()
        res, res_r = self.derive_resource()
        amb, amb_r = self.derive_ambition()
        return MetaVariables(
            maturity=mat, maturity_rationale=mat_r,
            bottleneck=bot, bottleneck_rationale=bot_r,
            resource=res, resource_rationale=res_r,
            ambition=amb, ambition_rationale=amb_r,
        )

    # ─── Document Triggers ───────────────────────────────────

    def derive_triggers(self) -> dict[DocID, bool]:
        f = self.form
        triggers: dict[DocID, bool] = {}

        # Tier 1 — always
        for uid in (DocID.U1, DocID.U2, DocID.U3, DocID.U4, DocID.U5,
                     DocID.U6, DocID.U7, DocID.U8, DocID.U9):
            triggers[uid] = True

        # Tier 2 — Business Model
        triggers[DocID.BM1] = f.conversation_required
        triggers[DocID.BM2] = f.is_appointment_based
        triggers[DocID.BM3] = f.has_physical_location
        triggers[DocID.BM4] = f.get("Q6") == "Yes — it's central to my business"
        triggers[DocID.BM5] = f.has_repeat_purchase
        triggers[DocID.BM6] = f.is_ongoing_service
        triggers[DocID.BM7] = f.is_self_serve

        # Tier 3 — Channel (determined by scoring)
        channel_scores = self.score_channels()
        primary = channel_scores.primary
        secondary = channel_scores.secondary

        for ch_doc in (DocID.CH1, DocID.CH2, DocID.CH3, DocID.CH4,
                       DocID.CH5, DocID.CH6, DocID.CH7):
            ch_enum = Channel(ch_doc.value)
            triggers[ch_doc] = (ch_enum == primary) or (ch_enum == secondary)

        # Tier 4 — Funnel Components
        is_paid_channel = primary in (Channel.CH1_SEA, Channel.CH2_SOCIAL_ADS)
        is_outbound = primary == Channel.CH3_COLD_OUTBOUND
        has_no_website = f.get("Q28") == "No"

        triggers[DocID.FC1] = is_paid_channel or is_outbound or has_no_website
        triggers[DocID.FC2] = (
            triggers[DocID.BM1]
            or f.get("Q30", "") in ("Yes — 500+", "Yes — under 500")
            or f.get("Q16", "") in ("1-4 weeks", "1-3 months", "3+ months")
        )
        triggers[DocID.FC3] = (
            self._deal >= 2000
            and f.get("Q16", "") in ("1-4 weeks", "1-3 months", "3+ months")
            and primary != Channel.CH3_COLD_OUTBOUND
        )
        # FC4: almost always triggered if any digital funnel exists
        triggers[DocID.FC4] = any([
            triggers[DocID.BM1], triggers[DocID.BM2],
            triggers[DocID.BM5], triggers[DocID.BM7],
            triggers[DocID.FC1], triggers[DocID.FC2],
        ])
        triggers[DocID.FC5] = is_paid_channel and self._budget >= 1500

        # Tier 5 — Maturity
        proof = f.proof_level
        triggers[DocID.MT1] = proof in (
            "Strong — portfolio, testimonials, case studies, media/speaking",
            "Moderate — some client results, a few testimonials",
        )
        triggers[DocID.MT2] = proof in (
            "Weak — I have experience but nothing documented",
            "None — starting from scratch",
        )
        triggers[DocID.MT3] = f.team_size in ("Solo — just me", "Me + 1-2 people (freelancers/part-time)")

        return triggers

    # ─── Channel Scoring ─────────────────────────────────────

    def score_channels(self) -> ChannelScores:
        scores = [
            self._score_ch1(),
            self._score_ch2(),
            self._score_ch3(),
            self._score_ch4(),
            self._score_ch5(),
            self._score_ch6(),
            self._score_ch7(),
        ]

        ranked = sorted(scores, key=lambda s: s.score, reverse=True)
        primary = ranked[0].channel
        secondary = None

        # If top 2 within 10 points, flag secondary
        if len(ranked) > 1 and ranked[1].score > 0 and (ranked[0].score - ranked[1].score) <= 10:
            secondary = ranked[1].channel

        # CH7 is always transitional — if it's "primary", pair with next best
        if primary == Channel.CH7_MARKETPLACE:
            secondary = ranked[1].channel if len(ranked) > 1 else None

        return ChannelScores(scores=scores, primary=primary, secondary=secondary)

    def _hard_no(self, *keywords: str) -> bool:
        nos = self.form.hard_nos
        return any(k in " ".join(nos).lower() for k in keywords)

    def _score_ch1(self) -> ChannelScore:
        """SEA (Google Ads)."""
        score = 0
        pos, neg = [], []

        if self._hard_no("ads", "spend money on ads"):
            return ChannelScore(Channel.CH1_SEA, 0, [], ["Hard no on ads"], hard_no=True)

        if self.form.conversation_required:
            score += 20; pos.append("Conversation required → high-intent search")
        if self._deal >= 2000:
            score += 20; pos.append(f"Deal size ${self._deal} justifies CPC")
        if self._budget >= 1500:
            score += 20; pos.append(f"Budget ${self._budget}/mo sufficient")
        if self.form.get("Q5") in ("National", "International"):
            score += 15; pos.append("National/international reach")
        if self.form.get("Q46") in ("I have more money than time — I'll pay for speed",
                                     "I want to buy a system — don't make me build slowly"):
            score += 10; pos.append("Prefers paid speed")

        if self._deal < 500:
            score -= 30; neg.append(f"Deal size ${self._deal} too low for CPC ROI")

        return ChannelScore(Channel.CH1_SEA, max(score, 0), pos, neg)

    def _score_ch2(self) -> ChannelScore:
        """Social Ads (Meta/Instagram/LinkedIn/TikTok)."""
        score = 0
        pos, neg = [], []

        if self._hard_no("ads", "spend money on ads"):
            return ChannelScore(Channel.CH2_SOCIAL_ADS, 0, [], ["Hard no on ads"], hard_no=True)

        q8 = self.form.get("Q8", "")
        if q8 in ("Physical product", "Mix of service + product"):
            score += 20; pos.append("Visual/product business")
        if self.form.is_local or self.form.get("Q5") == "National":
            score += 20; pos.append("Local radius or national B2C targeting")
        if self._budget >= 500:
            score += 20; pos.append(f"Budget ${self._budget}/mo sufficient")
        if self.form.get("Q46") in ("I have more money than time — I'll pay for speed",
                                     "I want to buy a system — don't make me build slowly"):
            score += 15; pos.append("Prefers paid speed")

        socials = self.form.get("Q31", [])
        if isinstance(socials, list) and any(s in socials for s in ("Instagram", "Facebook")):
            score += 10; pos.append("Instagram/Facebook presence exists")

        return ChannelScore(Channel.CH2_SOCIAL_ADS, max(score, 0), pos, neg)

    def _score_ch3(self) -> ChannelScore:
        """Cold Outbound."""
        score = 0
        pos, neg = [], []

        if self._hard_no("cold call", "cold dm"):
            return ChannelScore(Channel.CH3_COLD_OUTBOUND, 0, [], ["Hard no on cold outreach"], hard_no=True)

        if self.form.conversation_required:
            score += 20; pos.append("Conversation-based sale")
        if self._deal >= 2000:
            score += 20; pos.append(f"Deal size ${self._deal} justifies outreach effort")

        q38 = self.form.get("Q38", "")
        if q38 not in ("N/A (B2C)", "Doesn't matter", ""):
            score += 15; pos.append(f"Identifiable target companies: {q38}")
        q39 = self.form.get("Q39", "")
        if q39 not in ("N/A", "Don't know", ""):
            score += 15; pos.append(f"Identifiable buyer role: {q39}")

        if self._budget < 1500:
            score += 10; pos.append("Budget too low for ads → outbound is viable alternative")

        hours = self.form.get("Q45", "")
        if hours in ("5-10 hours", "10-20 hours"):
            score += 10; pos.append(f"Has time to execute: {hours}/week")

        return ChannelScore(Channel.CH3_COLD_OUTBOUND, max(score, 0), pos, neg)

    def _score_ch4(self) -> ChannelScore:
        """Organic Content."""
        score = 0
        pos, neg = [], []

        if self._hard_no("content regularly", "create content"):
            return ChannelScore(Channel.CH4_ORGANIC_CONTENT, 0, [], ["Hard no on content creation"], hard_no=True)

        hours = self.form.get("Q45", "")
        if hours in ("5-10 hours", "10-20 hours"):
            score += 20; pos.append(f"Has time: {hours}/week")

        proof = self.form.proof_level
        if proof in ("Strong — portfolio, testimonials, case studies, media/speaking",
                     "Moderate — some client results, a few testimonials"):
            score += 15; pos.append("Has expertise to share (proof exists)")

        q16 = self.form.get("Q16", "")
        if q16 in ("1-4 weeks", "1-3 months", "3+ months"):
            score += 15; pos.append("Long buying cycle → content nurtures")

        if self.form.get("Q46") == "I have more time than money — I'll do the work":
            score += 15; pos.append("Prefers time over money")

        if self._hard_no("show my face", "camera"):
            score -= 30; neg.append("Won't show face → limits video formats")

        return ChannelScore(Channel.CH4_ORGANIC_CONTENT, max(score, 0), pos, neg)

    def _score_ch5(self) -> ChannelScore:
        """Local SEO & Maps."""
        score = 0
        pos, neg = [], []

        q6 = self.form.get("Q6", "")
        if q6 == "Yes — it's central to my business":
            score += 30; pos.append("Physical location is central to business")
        elif q6 == "Yes — but most business happens remotely":
            score += 10; pos.append("Has physical location (secondary)")

        if self.form.is_local:
            score += 25; pos.append("Local customer base")

        q1 = self.form.business_type
        if q1 in ("Local business (restaurant, salon, retail, practice…)",
                   "Tradesperson / home services"):
            score += 20; pos.append(f"Business type: {q1}")

        if score > 0:
            score += 10; pos.append("Long-term compounding value")

        return ChannelScore(Channel.CH5_LOCAL_SEO, max(score, 0), pos, neg)

    def _score_ch6(self) -> ChannelScore:
        """Referral & Partnerships."""
        score = 0
        pos, neg = [], []

        methods = self.form.current_methods
        if "Word of mouth / referrals" in methods:
            score += 25; pos.append("WOM already a current source")
        if self.form.get("Q24") == "Word of mouth / referrals":
            score += 20; pos.append("WOM is primary revenue source → systematize")
        if self.form.has_repeat_purchase:
            score += 15; pos.append("Repeat customers can refer")
        if self._budget <= 500:
            score += 10; pos.append("Low budget → free channel is attractive")

        return ChannelScore(Channel.CH6_REFERRAL, max(score, 0), pos, neg)

    def _score_ch7(self) -> ChannelScore:
        """Marketplace (transitional)."""
        pos, neg = [], []

        methods = self.form.current_methods
        q26 = self.form.get("Q26", "")

        is_marketplace = "Marketplace (Malt, Upwork, Fiverr, Etsy…)" in methods
        is_dependent = q26 in ("It's my only source of clients", "It's my main source (>50%)")

        if is_marketplace and is_dependent:
            pos.append(f"Currently on marketplace, dependency: {q26}")
            neg.append("Transitional only — always paired with migration channel")
            return ChannelScore(Channel.CH7_MARKETPLACE, 1, pos, neg)

        return ChannelScore(Channel.CH7_MARKETPLACE, 0, [], ["Not on marketplace or not dependent"])