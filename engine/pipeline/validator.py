"""Pre-generation validation: catch inconsistencies and red flags in form answers.

Runs after parsing, before (or alongside) the LLM strat prompt.
Produces ValidationFlag objects that feed into the diagnostic.
"""

from __future__ import annotations

from engine.models.diagnostic import ValidationFlag
from engine.models.form import FormAnswers
from engine.pipeline.trigger_engine import (
    _REVENUE_MIDPOINTS,
    _TARGET_MIDPOINTS,
    _DEAL_MIDPOINTS,
    _BUDGET_MIDPOINTS,
)


class FormValidator:
    """Run all validation rules against form answers."""

    def __init__(self, form: FormAnswers):
        self.form = form
        self._revenue = _REVENUE_MIDPOINTS.get(form.monthly_revenue, 0)
        self._target = _TARGET_MIDPOINTS.get(form.get("Q40", ""), 0)
        self._deal = _DEAL_MIDPOINTS.get(form.deal_size, 0)
        self._budget = _BUDGET_MIDPOINTS.get(form.get("Q44", ""), 0)

    def run_all(self) -> list[ValidationFlag]:
        flags: list[ValidationFlag] = []
        for check in [
            self._check_revenue_sanity,
            self._check_budget_vs_ambition,
            self._check_hard_no_vs_channel,
            self._check_proof_vs_guarantee,
            self._check_zero_resources,
            self._check_declining_no_proof,
            self._check_price_mismatch,
            self._check_local_but_international,
            self._check_revenue_concentration,
            self._check_margin_vs_scale,
        ]:
            result = check()
            if result:
                flags.append(result)
        return flags

    def _check_revenue_sanity(self) -> ValidationFlag | None:
        """Q10 × Q19 ≈ Q18 (±50%)."""
        q19_map = {"0": 0, "1-3": 2, "4-10": 7, "11-30": 20, "30-100": 65, "100+": 150}
        clients = q19_map.get(self.form.get("Q19", "0"), 0)

        if clients == 0 or self._deal == 0 or self._revenue == 0:
            return None

        implied = self._deal * clients
        ratio = implied / self._revenue if self._revenue > 0 else float("inf")

        if ratio > 3 or ratio < 0.3:
            return ValidationFlag(
                rule_name="revenue_sanity",
                severity="warning",
                message=(
                    f"Deal size (${self._deal}) × clients/mo ({clients}) = ${implied:,.0f} "
                    f"but reported revenue is ${self._revenue:,.0f}/mo. "
                    f"Ratio: {ratio:.1f}x. Numbers may be inconsistent."
                ),
                questions_involved=["Q10", "Q19", "Q18"],
                action="Flag in U1. Use reported revenue as baseline but note discrepancy.",
            )
        return None

    def _check_budget_vs_ambition(self) -> ValidationFlag | None:
        """Q44 = $0 AND Q40 = $50k+."""
        if self._budget == 0 and self._target >= 50000:
            return ValidationFlag(
                rule_name="budget_vs_ambition",
                severity="warning",
                message=(
                    f"Revenue target is ${self._target:,.0f}/mo but acquisition budget is $0. "
                    "This target requires investment."
                ),
                questions_involved=["Q40", "Q44"],
                action="U1: prescribe minimum viable budget. U7: show investment needed for target.",
            )
        return None

    def _check_hard_no_vs_channel(self) -> ValidationFlag | None:
        """Q48 conflicts with likely best channel."""
        nos = self.form.hard_nos
        nos_text = " ".join(nos).lower()
        conflicts = []

        if "ads" in nos_text or "spend money on ads" in nos_text:
            if self._budget >= 1500 and self.form.conversation_required:
                conflicts.append("Refuses ads but profile fits paid acquisition (SEA)")
            if self.form.is_local:
                conflicts.append("Refuses ads but local business benefits most from targeted social ads")

        if "content" in nos_text and "cold" in nos_text and "ads" in nos_text:
            conflicts.append("Refuses content, cold outreach, AND ads — very few channels remain")

        if not conflicts:
            return None

        return ValidationFlag(
            rule_name="hard_no_vs_channel",
            severity="warning",
            message=" | ".join(conflicts),
            questions_involved=["Q48"],
            action="Acknowledge constraint in U1, recommend next-best channel, note trade-off explicitly.",
        )

    def _check_proof_vs_guarantee(self) -> ValidationFlag | None:
        """Q32 = "none" → softer guarantee needed."""
        if self.form.proof_level == "None — starting from scratch":
            return ValidationFlag(
                rule_name="proof_vs_guarantee",
                severity="info",
                message="No proof exists. Guarantee in U3 should be conditional, not unconditional.",
                questions_involved=["Q32"],
                action="U3: recommend conditional guarantee with clear criteria. MT2: prioritize proof generation.",
            )
        return None

    def _check_zero_resources(self) -> ValidationFlag | None:
        """Q45 ≤ 2h AND Q44 ≤ $200."""
        hours = self.form.get("Q45", "")
        if hours in ("< 2 hours", "I want to spend ZERO — automate everything") and self._budget <= 200:
            return ValidationFlag(
                rule_name="zero_resources",
                severity="critical",
                message=(
                    f"Budget: ${self._budget}/mo. Time: {hours}/week. "
                    "System cannot produce results without either time or money input."
                ),
                questions_involved=["Q44", "Q45"],
                action=(
                    "U1: prescribe 'Step 1: free up budget or time before anything else.' "
                    "Stripped-down doc set. Focus on single highest-leverage action."
                ),
            )
        return None

    def _check_declining_no_proof(self) -> ValidationFlag | None:
        """Q21 = declining AND Q32 = weak/none."""
        trend = self.form.get("Q21", "")
        proof = self.form.proof_level

        if trend == "Declining" and proof in (
            "Weak — I have experience but nothing documented",
            "None — starting from scratch",
        ):
            return ValidationFlag(
                rule_name="declining_no_proof",
                severity="critical",
                message="Revenue declining with no documented proof. Survival mode.",
                questions_involved=["Q21", "Q32"],
                action=(
                    "U1: prioritize immediate revenue actions over system building. "
                    "MT2: urgent proof generation sprint. "
                    "Skip long-term plays (content, SEO). Focus on fastest path to next client."
                ),
            )
        return None

    def _check_price_mismatch(self) -> ValidationFlag | None:
        """Q10 < $500 AND Q13 = "always" (sales call for small deal)."""
        if self._deal < 500 and self.form.conversation_required:
            return ValidationFlag(
                rule_name="price_mismatch",
                severity="warning",
                message=(
                    f"Consultative sale (Q13) for deals under ${self._deal}. "
                    "A 30-min sales call + follow-up may cost more than the deal."
                ),
                questions_involved=["Q10", "Q13"],
                action="U4: recommend either raising prices to justify sales process, or moving to self-serve for small deals.",
            )
        return None

    def _check_local_but_international(self) -> ValidationFlag | None:
        """Q6 = physical location AND Q5 = international."""
        q6 = self.form.get("Q6", "")
        q5 = self.form.get("Q5", "")

        if "Yes" in q6 and q5 == "International":
            return ValidationFlag(
                rule_name="local_but_international",
                severity="info",
                message="Has physical location but targets international customers. Unusual combination.",
                questions_involved=["Q5", "Q6"],
                action="U1: clarify — location-based business with international ambition? Or location is incidental? Affects channel strategy.",
            )
        return None

    def _check_revenue_concentration(self) -> ValidationFlag | None:
        """Q20 > 50% from single client."""
        q20 = self.form.get("Q20", "")
        if q20 in ("100% (one client)", "50-80%"):
            return ValidationFlag(
                rule_name="revenue_concentration",
                severity="warning",
                message=f"Revenue concentration: {q20} from top client. High dependency risk.",
                questions_involved=["Q20"],
                action="U1: flag as urgency driver. U3: offer must address diversification. Acquisition is urgent regardless of other bottlenecks.",
            )
        return None

    def _check_margin_vs_scale(self) -> ValidationFlag | None:
        """Want to double revenue but margins < 20%."""
        q22 = self.form.get("Q22", "")
        multiplier = self._target / self._revenue if self._revenue > 0 else 0

        if q22 == "< 20%" and multiplier >= 1.5:
            return ValidationFlag(
                rule_name="margin_vs_scale",
                severity="warning",
                message=(
                    f"Target is {multiplier:.1f}x current revenue but margins are <20%. "
                    "Doubling volume at thin margins won't solve profitability."
                ),
                questions_involved=["Q18", "Q22", "Q40"],
                action=(
                    "U7: model improved-margin × moderate-volume vs current-margin × high-volume. "
                    "U4: restructure pricing for margin FIRST, then scale. "
                    "Prescription: fix margins before pouring into acquisition."
                ),
            )
        return None