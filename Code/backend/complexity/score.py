import ast
from complexity.loops import analyze_loops
from complexity.nesting_depth import analyze_nest
from complexity.big_o import estimate_big_o

def complexity_score(code: str):
    tree = ast.parse(code)

    # Penalty accumulators
    loop_penalty = 0
    nesting_penalty = 0
    big_o_penalty = 0
    cyclomatic_penalty = 0
    branching_penalty = 0

    # Run previous analyses
    loop_result = analyze_loops(tree)
    nest_result = analyze_nest(tree)
    big_o_result = estimate_big_o(tree)

    # LOOP PENALTY
    loops = loop_result["total_loops"]
    depth = loop_result["max_loop_depth"]

    # Loop count penalty
    if loops == 0:
        loop_penalty += 0
    elif loops == 1:
        loop_penalty += 3
    elif loops == 2:
        loop_penalty += 5
    elif loops == 3:
        loop_penalty += 8
    else:
        loop_penalty += 12

    # Nested depth penalty
    if depth == 1:
        loop_penalty += 0
    elif depth == 2:
        loop_penalty += 5
    elif depth == 3:
        loop_penalty += 10
    elif depth >= 4:
        loop_penalty += 15

    # NESTING PENALTY
    ndepth = nest_result["max_nesting_depth"]

    if ndepth <= 1:
        nesting_penalty += 0
    elif ndepth == 2:
        nesting_penalty += 4
    elif ndepth == 3:
        nesting_penalty += 8
    elif ndepth == 4:
        nesting_penalty += 12
    elif ndepth == 5:
        nesting_penalty += 16
    else:
        nesting_penalty += 20

    # BIG-O PENALTY
    big_o = big_o_result["estimated_big_o"]

    if big_o == "O(1)":
        big_o_penalty += 0
    elif big_o == "O(n)":
        big_o_penalty += 5
    elif big_o == "O(n^2)":
        big_o_penalty += 10
    elif big_o == "O(n^3)":
        big_o_penalty += 20
    elif big_o == "O(n^k)":
        big_o_penalty += 25
    elif big_o == "O(2^n)":
        big_o_penalty += 30
    elif big_o == "O(n!)":
        big_o_penalty += 35

    # CYCLOMATIC COMPLEXITY PENALTY
    cc_count = 1  # CC starts at 1
    branch_nodes = [ast.If, ast.Try, ast.ExceptHandler]
    
    # These nodes exist only in Python 3.10–3.11
    if hasattr(ast, "Match"):
        branch_nodes.append(ast.Match)
    if hasattr(ast, "MatchCase"):
        branch_nodes.append(ast.MatchCase)
    if hasattr(ast, "MatchClass"):  # Python 3.12–3.13 replacement
        branch_nodes.append(ast.MatchClass)
    
    branch_nodes = tuple(branch_nodes)


    for node in ast.walk(tree):
        # Decision nodes
        if isinstance(node, branch_nodes):
            cc_count += 1
        
        # Logical conditions (and/or)
        if isinstance(node, ast.BoolOp):
            cc_count += 1

    # CC penalty
    if cc_count <= 5:
        cyclomatic_penalty += 3
    elif cc_count <= 10:
        cyclomatic_penalty += 7
    elif cc_count <= 15:
        cyclomatic_penalty += 12
    elif cc_count <= 20:
        cyclomatic_penalty += 16
    else:
        cyclomatic_penalty += 20

    # BRANCHING PENALTY

    # Count functions
    num_functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))

    # Function penalty
    if num_functions <= 2:
        function_penalty = 0
    elif num_functions <= 5:
        function_penalty = 5
    elif num_functions <= 10:
        function_penalty = 10
    else:
        function_penalty = 15

    # Count branches (if + elif)
    num_branches = sum(1 for node in ast.walk(tree) if isinstance(node, ast.If))

    # Branch penalty
    if num_branches <= 3:
        branch_penalty = 2
    elif num_branches <= 6:
        branch_penalty = 5
    elif num_branches <= 10:
        branch_penalty = 10
    else:
        branch_penalty = 20

    # Combine — cap at 20
    branching_penalty = min(function_penalty + branch_penalty, 20)

    # FINAL SCORE
    total_penalty = (
        loop_penalty +
        nesting_penalty +
        big_o_penalty +
        cyclomatic_penalty +
        branching_penalty
    )

    qualityScore = max(0, 100 - total_penalty)

    return qualityScore
