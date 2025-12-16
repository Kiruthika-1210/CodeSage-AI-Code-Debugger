import ast
from analysis.common import make_issue, parse_code_safely
from analysis.unused_imports import rule_unused_names
from analysis.nesting import rule_nesting
from analysis.naming import rule_bad_naming
from analysis.long_functions import rule_long_function
from analysis.dead_code import rule_dead_code
from analysis.docstrings import rule_docstrings
from analysis.duplicate_logic import rule_duplicate_logic
from complexity.loops import analyze_loops
from complexity.nesting_depth import analyze_nest
from complexity.big_o import estimate_big_o
from complexity.score import complexity_score


# RULE CONFIG (enable/disable specific rules)
RULES_ENABLED = {
    "unused_imports": True,
    "unused_variables": True,
    "deep_nesting": True,
    "long_functions": True,
    "duplicate_logic": True,
    "dead_code": True,
    "naming": True,
    "docstrings": True,
}

def run_static_analysis(code: str):
    issues = []
    complexity = {}

    tree, syntax_issue = parse_code_safely(code)
    if syntax_issue:
        return {
            "issues": [syntax_issue],
            "complexity": {}
            }
    
    
    #ISSUES
    try:
        if RULES_ENABLED["unused_imports"]:
            issues += rule_unused_names(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'unused_imports' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )

    try:
        if RULES_ENABLED["deep_nesting"]:
            issues += rule_nesting(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'deep_nesting' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )

    try:
        if RULES_ENABLED["naming"]:
            issues += rule_bad_naming(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'naming' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )

    try:
        if RULES_ENABLED["long_functions"]:
            issues += rule_long_function(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'long_functions' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )

    try:
        if RULES_ENABLED["dead_code"]:
            issues += rule_dead_code(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'dead_code' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )

    try:
        if RULES_ENABLED["docstrings"]:
            issues += rule_docstrings(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'docstrings' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )

    try:
        if RULES_ENABLED["duplicate_logic"]:
            issues += rule_duplicate_logic(code)
    except:
        issues.append(make_issue(
            issue_type="rule-error",
            message="Rule 'duplicate_logic' failed internally.",
            line=1,
            severity="high",
            suggestion="Contact tool developer."
            )
            )
    
    if issues:
        issues = sorted(issues, key=lambda x: x.get("line", 0))

    
    #COMPLEXITY
    loops_result = analyze_loops(tree)
    nesting_result = analyze_nest(tree)
    big_o_result = estimate_big_o(tree)
    complexity_final_score = complexity_score(code)

    complexity = {
        "loops": loops_result,
        "nesting": nesting_result,
        "big_o": big_o_result["estimated_big_o"],
        "score": complexity_final_score
    }

    return {
        "issues": issues,
        "complexity": complexity
    }
    
