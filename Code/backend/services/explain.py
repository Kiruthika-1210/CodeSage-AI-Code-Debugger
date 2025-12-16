import logging
from services.ai_client import call_gemini

logger = logging.getLogger(__name__)


def run_explain_step(code, issues):
    """
    Runs AI-based code explanation.

    Returns:
    - explanation: str

    Safety guarantees:
    - Never raises exceptions to the caller
    - Falls back to empty explanation on failure
    """

    result = {}
    issues = issues or []

    try:
        # Load explanation prompt template
        with open("prompts/explain.txt", encoding="utf-8") as f:
            template = f.read()

        # Construct prompt
        prompt = template + "\n\nCODE TO ANALYZE:\n" + code

        # Call AI
        response = call_gemini(prompt)

        result["explanation"] = response.get("explanation", "")

    except Exception:
        logger.exception("Explain step failed")
        result["explanation"] = ""

    return result
