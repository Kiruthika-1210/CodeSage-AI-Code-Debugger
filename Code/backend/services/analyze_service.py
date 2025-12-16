# services/analyze_service.py
from analysis.run_all import run_static_analysis
from scoring.overall import overall_score

def analyze_full(code: str):
    analysis_result = run_static_analysis(code)
    scores = overall_score(code)

    return {
        "issues": analysis_result["issues"],
        "complexity": analysis_result["complexity"],
        "qualityScore": scores["qualityScore"],
        "readability": scores["readability"],
        "maintainability": scores["maintainability"],
        "style": scores["style"],
        "documentation": scores["documentation"],
    }
