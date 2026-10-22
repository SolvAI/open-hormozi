"""Strat Prompt 2: JSON extraction from diagnostic output.

Takes the prose diagnostic from strat_prompt_1 and extracts
structured booleans + enums for pipeline consumption.

Uses a lighter model (Haiku/Sonnet) since this is extraction, not reasoning.
"""

import json
from engine.models.enums import DocID, EmailSequence

# Build the expected JSON shape dynamically from enums
_DOC_KEYS = {d.value: "boolean" for d in DocID}
_SEQ_KEYS = [s.value for s in EmailSequence]

SYSTEM_PROMPT = f"""You extract structured data from a business diagnostic report.

Given a diagnostic report, return a JSON object with this EXACT structure:

```json
{{
  "meta": {{
    "maturity": "STARTER | GROWING | ESTABLISHED | PIVOT",
    "bottleneck": "visibility | lead_generation | conversion | pricing | retention | wrong_clients",
    "resource": "money_rich | time_rich | balanced | constrained",
    "ambition": "lifestyle | growth | aggressive | survival"
  }},
  "triggered_docs": {{
    {', '.join(f'"{k}": true/false' for k in _DOC_KEYS)}
  }},
  "channels": {{
    "scores": {{
      "CH1": integer 0-100,
      "CH2": integer 0-100,
      "CH3": integer 0-100,
      "CH4": integer 0-100,
      "CH5": integer 0-100,
      "CH6": integer 0-100,
      "CH7": integer 0-100
    }},
    "primary": "CH1 | CH2 | CH3 | CH4 | CH5 | CH6 | CH7",
    "secondary": "CH1 | ... | CH7 | null"
  }},
  "fc4_sequences": [
    // Only include sequences that are triggered. Possible values:
    // {json.dumps(_SEQ_KEYS)}
  ],
  "validation_flags": [
    {{
      "rule_name": "string",
      "severity": "info | warning | critical",
      "message": "string",
      "questions_involved": ["Q1", "Q2"],
      "action": "string"
    }}
  ],
  "content_angles": ["string", "string", ...],
  "priority_order": ["U1", "U4", "U3", ...]
}}
```

Rules:

U1 through U9 are ALWAYS true in triggered_docs.
Extract values exactly as stated in the diagnostic. Do not re-analyze or change decisions.
If the diagnostic says a doc is triggered, set it to true. If excluded, false.
For channel scores, extract the numeric scores from the scoring table.
For fc4_sequences, only include ones explicitly mentioned as triggered.
priority_order should list ONLY triggered docs in the order specified.
Return ONLY valid JSON. No explanation, no markdown fences. """

def build_extractor_user_prompt(diagnostic_text: str) -> str: 
    """Build the user prompt for strat prompt 2.""" 
    return f"""Extract the structured data from this diagnostic report:
    {diagnostic_text}
    Return the JSON object. No explanation."""

