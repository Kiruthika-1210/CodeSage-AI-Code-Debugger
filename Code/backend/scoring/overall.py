from scoring.documentation import analyze_documentation
from scoring.maintainability import analyze_maintainability
from scoring.readability import analyze_readability
from scoring.style import analyze_style

def overall_score(code: str):
    # Run analyzers
    r = analyze_readability(code)["readability_score"]        # 0–25
    m = analyze_maintainability(code)["maintainability_score"]
    d = analyze_documentation(code)["documentation_score"]
    s = analyze_style(code)["style_score"]

    # BASE SCORE 
    base_score = (
        0.40 * r +
        0.40 * m +
        0.15 * d +
        0.05 * s
    ) * 4   # convert to 0–100

    bonus = 0

    if r >= 20 and m >= 22 and d >= 20 and s >= 16:
        bonus = 7

    final_score = min(100, round(base_score + bonus, 1))

    return {
        "qualityScore": final_score,
        "readability": r * 4,
        "maintainability": m * 4,
        "documentation": d * 4,
        "style": s * 4,
    }
