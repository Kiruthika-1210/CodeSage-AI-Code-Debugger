import logging
import os
from services.ai_client import call_gemini

logger = logging.getLogger(__name__)

# Absolute path to prompts directory (VERY IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "..", "prompts", "refactor.txt")


def run_refactor_step(code, issues):
    """
    Runs AI-based refactor step with full debugging visibility.

    Guarantees:
    - No silent failures
    - Gemini text response handled correctly
    - Markdown fences stripped
    - compile() validation before returning
    - Safe fallback to original code
    """

    result = {}
    issues = issues or []

    try:
        # Load prompt template
        with open(PROMPT_PATH, encoding="utf-8") as f:
            template = f.read()

        # Build issues text
        issues_text = "\n".join(
            f"- {i.get('type')}: {i.get('message')}"
            for i in issues
        ) or "No issues detected."

        # Construct final prompt
        prompt = (
            template
            + "\n\nISSUES DETECTED:\n"
            + issues_text
            + "\n\nCODE TO REFACTOR:\n"
            + code
        )

        # Call Gemini
        response = call_gemini(prompt)

        # Normalize Gemini output
        if isinstance(response, dict):
            text = (
                response.get("text")
                or response.get("content")
                or response.get("refactored_code")
                or ""
            )
        else:
            text = str(response)

        text = text.strip()

        # Remove markdown fences if present
        if text.startswith("```"):
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1]
                if text.startswith("python"):
                    text = text[len("python"):]

        refactored_code = text.strip().replace("\r\n", "\n")

        # If empty - fallback
        if not refactored_code:
            result["refactored_code"] = code
            result["notes"] = "AI returned empty refactor output"
            return result

        # Validate generated code
        try:
            compile(refactored_code, "<string>", "exec")
            result["refactored_code"] = refactored_code
            result["notes"] = "Refactor successful"
        except Exception as compile_error:
            result["refactored_code"] = code
            result["notes"] = "AI refactor invalid — fallback"

    except Exception as e:
        logger.exception("Refactor step crashed")
        result["refactored_code"] = code
        result["notes"] = "AI refactor failed — fallback"

    return result
