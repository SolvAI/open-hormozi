from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from engine.models.enums import DocID, Format, ModelTier


@dataclass
class ModelConfig:
    """Configuration for one model tier."""

    model_name: str
    max_tokens: int
    thinking: Optional[dict] = None  # e.g. {"type": "adaptive", "display": "summarized"}
    effort: Optional[str] = None     # low | medium | high | xhigh | max


@dataclass
class ModelRouter:
    """Maps task types to Claude model names.

    Routing logic:
      MAX    (Opus+thinking) → strat diagnostic, hardest reasoning
      HEAVY  (Opus)          → complex docs (U3, BM1, FC1, FC3)
      MEDIUM (Sonnet)        → most document generation
      LIGHT  (Haiku)         → JSON extraction, summaries
    """

    models: dict[ModelTier, ModelConfig] = field(default_factory=dict)

    @classmethod
    def from_config(cls, config: dict) -> ModelRouter:
        """Build router from a parsed config.yaml dict. Required — no fallback defaults."""
        models_cfg = config.get("models")
        tokens_cfg = config.get("max_tokens")
        thinking_cfg = config.get("thinking", {})
        effort_cfg = config.get("effort", {})

        if not all([models_cfg, tokens_cfg]):
            missing = [
                k for k, v in {
                    "models": models_cfg,
                    "max_tokens": tokens_cfg,
                }.items()
                if not v
            ]
            raise ValueError(f"config.yaml missing required sections: {missing}")

        tier_map = {
            ModelTier.MAX: "max",
            ModelTier.HEAVY: "heavy",
            ModelTier.MEDIUM: "medium",
            ModelTier.LIGHT: "light",
        }

        built = {}
        for tier, key in tier_map.items():
            if key not in models_cfg:
                raise ValueError(f"config.yaml models.{key} is required")
            built[tier] = ModelConfig(
                model_name=models_cfg[key],
                max_tokens=tokens_cfg.get(key, 16384),
                thinking=thinking_cfg.get(key),  # None for tiers without thinking
                effort=effort_cfg.get(key),      # None for tiers without effort
            )

        return cls(models=built)

    def get_config(self, tier: ModelTier) -> ModelConfig:
        config = self.models.get(tier)
        if not config:
            raise ValueError(f"No model configured for tier: {tier}")
        return config

    def resolve(
        self,
        doc_id: Optional[DocID] = None,
        format: Optional[Format] = None,
        tier_override: Optional[ModelTier] = None,
        task: Optional[str] = None,
    ) -> ModelConfig:
        """Resolve the right model for a given generation task.

        Priority:
          1. Explicit tier_override (MAX or HEAVY treated as intentional)
          2. Task-based routing (strat → MAX, extraction → LIGHT)
          3. Doc-based (complex docs → HEAVY)
          4. Default → MEDIUM
        """

        # 1. Explicit override
        if tier_override and tier_override in (ModelTier.MAX, ModelTier.HEAVY):
            return self.get_config(tier_override)

        # 2. Task-based
        if task:
            task_tiers = {
                "strat_diagnostic": ModelTier.MAX,
                "strat_extraction": ModelTier.HEAVY,
                "summary": ModelTier.LIGHT,
            }
            if task in task_tiers:
                return self.get_config(task_tiers[task])

        # 3. Doc-based — complex docs get heavier models
        heavy_docs = {
            DocID.U3,   # Grand Slam Offer
            DocID.U6,   # Funnel Blueprint
            DocID.BM1,  # Sales Playbook
            DocID.FC1,  # Landing Page
            DocID.FC3,  # Webinar Script
        }
        if doc_id in heavy_docs:
            return self.get_config(ModelTier.HEAVY)

        # 4. Default
        return self.get_config(ModelTier.MEDIUM)