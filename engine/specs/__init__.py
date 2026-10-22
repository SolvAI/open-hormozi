"""Central registry of all 31 document specifications.

This is the single entry point — nothing else imports spec files directly.
"""

from __future__ import annotations

from engine.models.enums import DocID
from engine.models.registry import DocSpec

# ─── Tier 1: Universal (9 docs) ─────────────────────────────────
from engine.specs.u1_diagnostic_report import U1_SPEC
from engine.specs.u2_avatar_icp import U2_SPEC
from engine.specs.u3_grand_slam_offer import U3_SPEC
from engine.specs.u4_pricing_packaging import U4_SPEC
from engine.specs.u5_positioning_messaging import U5_SPEC
from engine.specs.u6_funnel_blueprint import U6_SPEC
from engine.specs.u7_financial_model import U7_SPEC
from engine.specs.u8_kpi_tracking import U8_SPEC
from engine.specs.u9_launch_roadmap import U9_SPEC

# ─── Tier 2: Business Model (7 docs) ────────────────────────────
from engine.specs.bm1_sales_playbook import BM1_SPEC
from engine.specs.bm2_booking_flow import BM2_SPEC
from engine.specs.bm3_local_visibility import BM3_SPEC
from engine.specs.bm4_onsite_experience import BM4_SPEC
from engine.specs.bm5_retention_loyalty import BM5_SPEC
from engine.specs.bm6_client_operations import BM6_SPEC
from engine.specs.bm7_online_purchase import BM7_SPEC

# ─── Tier 3: Channel (7 docs) ───────────────────────────────────
from engine.specs.ch1_sea_strategy import CH1_SPEC
from engine.specs.ch2_social_ads import CH2_SPEC
from engine.specs.ch3_cold_outbound import CH3_SPEC
from engine.specs.ch4_organic_content import CH4_SPEC
from engine.specs.ch5_local_seo import CH5_SPEC
from engine.specs.ch6_referral_partnership import CH6_SPEC
from engine.specs.ch7_marketplace import CH7_SPEC

# ─── Tier 4: Funnel Components (5 docs) ─────────────────────────
from engine.specs.fc1_landing_page import FC1_SPEC
from engine.specs.fc2_lead_magnet import FC2_SPEC
from engine.specs.fc3_webinar_vsl import FC3_SPEC
from engine.specs.fc4_email_sequences import FC4_SPEC
from engine.specs.fc5_retargeting import FC5_SPEC

# ─── Tier 5: Maturity (3 docs) ──────────────────────────────────
from engine.specs.mt1_proof_kit import MT1_SPEC
from engine.specs.mt2_proof_generation import MT2_SPEC
from engine.specs.mt3_tech_stack import MT3_SPEC


# ─── Master Registry ────────────────────────────────────────────

ALL_SPECS: dict[DocID, DocSpec] = {}

for _spec in [
    # Tier 1 — Universal
    U1_SPEC, U2_SPEC, U3_SPEC, U4_SPEC, U5_SPEC,
    U6_SPEC, U7_SPEC, U8_SPEC, U9_SPEC,
    # Tier 2 — Business Model
    BM1_SPEC, BM2_SPEC, BM3_SPEC, BM4_SPEC,
    BM5_SPEC, BM6_SPEC, BM7_SPEC,
    # Tier 3 — Channel
    CH1_SPEC, CH2_SPEC, CH3_SPEC, CH4_SPEC,
    CH5_SPEC, CH6_SPEC, CH7_SPEC,
    # Tier 4 — Funnel Components
    FC1_SPEC, FC2_SPEC, FC3_SPEC, FC4_SPEC, FC5_SPEC,
    # Tier 5 — Maturity
    MT1_SPEC, MT2_SPEC, MT3_SPEC,
]:
    ALL_SPECS[_spec.id] = _spec

assert len(ALL_SPECS) == 31, f"Expected 31 specs, got {len(ALL_SPECS)}"


def get_spec(doc_id: DocID) -> DocSpec:
    """Get a document spec by ID. Raises KeyError if not found."""
    if doc_id not in ALL_SPECS:
        raise KeyError(
            f"No spec registered for {doc_id.value}. "
            f"Available: {sorted(d.value for d in ALL_SPECS)}"
        )
    return ALL_SPECS[doc_id]


def has_spec(doc_id: DocID) -> bool:
    """Check if a spec exists."""
    return doc_id in ALL_SPECS