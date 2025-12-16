# backend/services/clean_preview.py

import logging
import os
from services.ai_client import call_gemini

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "clean_preview.txt")


def _safe_extract_preview(response: dict, original_code: str):
    """
    Extract usable preview code from ANY Gemini response shape.
    This function NEVER throws.
    """

    if not isinstance(response, dict):
        return original_code, "AI returned invalid response format."

    # Ideal response
    if isinstance(response.get("preview_code"), str):
        return response["preview_code"], response.get("explanation", "")

    # Old key name
    if isinstance(response.get("refactored_code"), str):
        return response["refactored_code"], response.get("notes", "")

    # Raw text (LLM ignored JSON rules)
    raw_text = response.get("raw_text")
    if isinstance(raw_text, str) and raw_text.strip():
        return raw_text.strip(), "Extracted from AI raw output."

    # Nothing usable
    return original_code, "AI preview unavailable. Showing original code."


def run_clean_preview(code, issues):
    """
    AI Clean Code Preview (ADVISORY ONLY).
    This function NEVER crashes.
    """

    try:
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            template = f.read()

        issues_text = "\n".join(
            f"- {i.get('type')}: {i.get('message')}"
            for i in (issues or [])
        )

        prompt = (
            template
            .replace("{{CODE}}", code)
            .replace("{{ISSUES}}", issues_text)
        )

        response = call_gemini(prompt)

        preview_code, explanation = _safe_extract_preview(response, code)

        return {
            "preview_code": preview_code,
            "explanation": explanation
        }

    except Exception as e:
        logger.exception("AI clean preview hard failure")
        return {
            "preview_code": code,
            "explanation": "AI preview failed completely. Showing original code."
        }
