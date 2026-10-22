"""Command-line runner: form JSON → full strategy, without the web app.

    uv run python cli.py examples/example_form.json

Uses ANTHROPIC_API_KEY (environment or .env), or the key saved in the app's Settings.
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
CALLER_CWD = Path.cwd()
os.chdir(ROOT)  # templates/ and config.yaml are resolved from the project root
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from engine.form.parser import FormParser
from engine.llm.anthropic_client import AnthropicClient
from engine.llm.router import ModelRouter
from engine.pipeline.runner import DocumentPipeline
from engine.models.enums import ModelTier

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            LOG_DIR / f"{timestamp}.log",
            encoding="utf-8",
        ),
    ],
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config.yaml")

def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load and validate config.yaml. Exits on failure."""
    if not path.exists():
        logger.error(f"Config file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        logger.error(f"Invalid config format in {path}")
        sys.exit(1)
    return config


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <form_answers.json> [run_name]")
        print("       python cli.py examples/example_form.json example")
        sys.exit(1)

    form_path = CALLER_CWD / sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else "user"

    # ── Load config ──
    config = load_config()

    # ── Load form answers ──
    with open(form_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    parser = FormParser()
    parse_result = parser.parse(raw)

    if not parse_result.is_valid:
        logger.error("Form validation failed:")
        for err in parse_result.errors:
            logger.error(f"  {err.question_id}: {err.message}")
        sys.exit(1)

    if parse_result.warnings:
        for warn in parse_result.warnings:
            logger.warning(f"  {warn.question_id}: {warn.message}")

    # ── Initialize LLM client from config ──
    from app.settings import get_api_key
    api_key = get_api_key()
    if not api_key:
        logger.error("No API key: set ANTHROPIC_API_KEY or save one in the app's Settings")
        sys.exit(1)

    router = ModelRouter.from_config(config)
    logger.info(
        f"Models: max={router.models[ModelTier.MAX].model_name}, "
        f"heavy={router.models[ModelTier.HEAVY].model_name}, "
        f"medium={router.models[ModelTier.MEDIUM].model_name}, "
        f"light={router.models[ModelTier.LIGHT].model_name}"
    )

    client = AnthropicClient(
        api_key=api_key,
        router=router,
        retry_config=config.get("retry"),
    )

    # ── Run pipeline ──
    output_base = Path(config.get("output", {}).get("base_dir", "output"))
    pipeline = DocumentPipeline(client=client, output_base=output_base)
    result = pipeline.run(form=parse_result.answers, user_id=user_id)

    # ── Report ──
    print("\n" + "=" * 60)
    print(f"Pipeline {'SUCCEEDED' if result.all_succeeded else 'COMPLETED WITH ERRORS'}")
    print(f"Output: {result.output_dir}")
    print(f"Documents: {result.doc_count} | Assets: {result.asset_count}")
    print(f"Cost: ${result.total_cost_usd:.3f} | Time: {result.total_generation_time_s:.1f}s")
    print(f"LLM: {client.usage.summary()}")

    if result.fatal_error:
        print(f"\nStopped early: {result.fatal_error}")
    if result.failed_docs:
        print(f"\nFailed: {[d.value for d in result.failed_docs]}")

    if result.fatal_error or not result.all_succeeded:
        sys.exit(1)


if __name__ == "__main__":
    main()