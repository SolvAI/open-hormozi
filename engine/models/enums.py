from enum import Enum


# ─── Output Formats ───────────────────────────────────────────────

class Format(str, Enum):
    DOC = "doc"
    XLS = "xls"
    HTML = "html"
    PNG = "png"
    MERMAID = "mermaid"
    PDF = "pdf"
    CHART = "chart"
    SLIDES = "slides"


# ─── Generation Methods ──────────────────────────────────────────

class GenerationMethod(str, Enum):
    LLM = "llm"                       # Pure LLM generation
    TEMPLATE_FILL = "template_fill"   # LLM produces JSON, injected into static template
    LLM_THEN_RENDER = "llm_then_render"  # LLM produces content, rendered via HTML→PNG/PDF
    STATIC = "static"                 # No LLM — return static asset as-is


# ─── Document Tiers ──────────────────────────────────────────────

class Tier(str, Enum):
    UNIVERSAL = "universal"
    BUSINESS_MODEL = "business_model"
    CHANNEL = "channel"
    FUNNEL = "funnel"
    MATURITY = "maturity"


# ─── Meta-Variable: Maturity ─────────────────────────────────────

class Maturity(str, Enum):
    STARTER = "STARTER"           # Pre-revenue or early, weak proof
    GROWING = "GROWING"           # $2-10k/mo, some traction
    ESTABLISHED = "ESTABLISHED"   # $10k+/mo, strong proof, years in
    PIVOT = "PIVOT"               # Experienced professional, new business


# ─── Meta-Variable: Bottleneck ───────────────────────────────────

class Bottleneck(str, Enum):
    VISIBILITY = "visibility"
    LEAD_GENERATION = "lead_generation"
    CONVERSION = "conversion"
    PRICING = "pricing"
    RETENTION = "retention"
    WRONG_CLIENTS = "wrong_clients"


# ─── Meta-Variable: Resource Profile ────────────────────────────

class ResourceProfile(str, Enum):
    MONEY_RICH = "money_rich"       # High budget, low time
    TIME_RICH = "time_rich"         # Low budget, high time
    BALANCED = "balanced"           # Some of each
    CONSTRAINED = "constrained"     # Neither


# ─── Meta-Variable: Ambition Profile ────────────────────────────

class AmbitionProfile(str, Enum):
    LIFESTYLE = "lifestyle"         # Optimize for margin + freedom
    GROWTH = "growth"               # Systematic 2-5x scaling
    AGGRESSIVE = "aggressive"       # 5x+ or compressed timeline
    SURVIVAL = "survival"           # Declining, needs next client NOW


# ─── Channels ────────────────────────────────────────────────────

class Channel(str, Enum):
    CH1_SEA = "CH1"
    CH2_SOCIAL_ADS = "CH2"
    CH3_COLD_OUTBOUND = "CH3"
    CH4_ORGANIC_CONTENT = "CH4"
    CH5_LOCAL_SEO = "CH5"
    CH6_REFERRAL = "CH6"
    CH7_MARKETPLACE = "CH7"


# ─── Document IDs ────────────────────────────────────────────────

class DocID(str, Enum):
    # Tier 1 — Universal
    U1 = "U1"
    U2 = "U2"
    U3 = "U3"
    U4 = "U4"
    U5 = "U5"
    U6 = "U6"
    U7 = "U7"
    U8 = "U8"
    U9 = "U9"
    # Tier 2 — Business Model
    BM1 = "BM1"
    BM2 = "BM2"
    BM3 = "BM3"
    BM4 = "BM4"
    BM5 = "BM5"
    BM6 = "BM6"
    BM7 = "BM7"
    # Tier 3 — Channel
    CH1 = "CH1"
    CH2 = "CH2"
    CH3 = "CH3"
    CH4 = "CH4"
    CH5 = "CH5"
    CH6 = "CH6"
    CH7 = "CH7"
    # Tier 4 — Funnel
    FC1 = "FC1"
    FC2 = "FC2"
    FC3 = "FC3"
    FC4 = "FC4"
    FC5 = "FC5"
    # Tier 5 — Maturity
    MT1 = "MT1"
    MT2 = "MT2"
    MT3 = "MT3"

    @property
    def tier(self) -> Tier:
        prefix = self.value[0]
        if self.value.startswith("U"):
            return Tier.UNIVERSAL
        if self.value.startswith("BM"):
            return Tier.BUSINESS_MODEL
        if self.value.startswith("CH"):
            return Tier.CHANNEL
        if self.value.startswith("FC"):
            return Tier.FUNNEL
        if self.value.startswith("MT"):
            return Tier.MATURITY
        raise ValueError(f"Unknown tier for {self.value}")

    @property
    def is_universal(self) -> bool:
        return self.tier == Tier.UNIVERSAL


# ─── FC4 Email Sub-Sequences ────────────────────────────────────

class EmailSequence(str, Enum):
    QUALIFIED_CONFIRMATION = "qualified_confirmation"
    NOT_QUALIFIED_LEAD_MAGNET = "not_qualified_lead_magnet"
    NO_SHOW_RECOVERY = "no_show_recovery"
    POST_CALL_SOLD = "post_call_sold"
    POST_CALL_NOT_SOLD = "post_call_not_sold"
    LONG_TERM_NURTURE = "long_term_nurture"
    POST_PURCHASE_WELCOME = "post_purchase_welcome"
    ABANDONED_CART = "abandoned_cart"
    RE_ENGAGEMENT_LAPSED = "re_engagement_lapsed"
    REVIEW_REQUEST = "review_request"
    REFERRAL_ASK = "referral_ask"


# ─── LLM Model Tiers ────────────────────────────────────────────

class ModelTier(str, Enum):
    MAX = "max"
    HEAVY = "heavy"     # Opus — strat, complex docs (U3, BM1, FC1, FC3)
    MEDIUM = "medium"   # Sonnet — most doc generation
    LIGHT = "light"     # Haiku — extraction, summaries, simple fills
