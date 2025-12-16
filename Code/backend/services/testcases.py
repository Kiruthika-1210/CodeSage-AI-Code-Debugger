import logging
from services.ai_client import call_gemini

logger = logging.getLogger(__name__)

def run_testcases_step(refactored_code, issues):
    result = {}

    try:
        with open("prompts/testcases.txt") as f:
            template = f.read()

        prompt = template + f"\n\nCODE TO TEST:\n{refactored_code}"
        response = call_gemini(prompt)

        if isinstance(response, list):
            result["test_cases"] = response
        elif isinstance(response, dict):
            result["test_cases"] = response.get("test_cases", [])
        else:
            result["test_cases"] = []

    except:
        logger.exception("Testcase generation failed")
        result["test_cases"] = []

    return result
