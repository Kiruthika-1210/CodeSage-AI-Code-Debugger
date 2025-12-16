from fastapi import APIRouter
from models.ai_request import AIRequest
from services.refactor import run_refactor_step
from services.explain import run_explain_step
from services.testcases import run_testcases_step
from services.analyze_service import analyze_full

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/refactor")
def api_refactor(payload: AIRequest):
    issues = payload.issues or []
    result = run_refactor_step(payload.code, issues)
    return {
        "refactored_code": result["refactored_code"],
        "notes": result["notes"],
        "ai_model": "gemini-flash-latest",
    }

@router.post("/explain")
def api_explain(payload: AIRequest):
    issues = payload.issues or []
    result = run_explain_step(payload.code, issues)
    return {
        "explanation": result["explanation"],
        "ai_model": "gemini-flash-latest",
    }

@router.post("/testcases")
def api_testcases(payload: AIRequest):
    issues = payload.issues or []
    result = run_testcases_step(payload.code, issues)
    return {
        "test_cases": result.get("test_cases", []),
        "ai_model": "gemini-flash-latest",
    }

@router.post("/analyze-and-refactor")
def api_analyze_and_refactor(payload: AIRequest):
    analysis = analyze_full(payload.code)

    raw_complexity = analysis.get("complexity", {})

    # NORMALIZED complexity 
    complexity = {
        "nestingDepth": raw_complexity.get("nesting", {}).get("max_nesting_depth", "—"),
        "loopDepth": raw_complexity.get("loops", {}).get("max_loop_depth", "—"),
        "bigO": raw_complexity.get("big_o", "—"),
        "score": raw_complexity.get("score", 0),
        "patterns": (
            ["Nested Loops"]
            if raw_complexity.get("loops", {}).get("nested_loops_detected")
            else []
        ),
    }

    refactor = run_refactor_step(
        payload.code,
        analysis.get("issues", [])
    )

    return {
        # Static analysis
        "issues": analysis.get("issues", []),
        "complexity": complexity,

        # Quality scores
        "readability": analysis.get("readability", 0),
        "maintainability": analysis.get("maintainability", 0),
        "style": analysis.get("style", 0),
        "documentation": analysis.get("documentation", 0),
        "qualityScore": analysis.get("qualityScore", 0),

        # AI refactor
        "refactoredCode": refactor.get("refactored_code", payload.code),
        "explanation": refactor.get("notes", ""),

        "ai_model": "gemini-flash-latest",
    }





