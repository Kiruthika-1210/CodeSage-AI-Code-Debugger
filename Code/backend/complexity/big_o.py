import ast
from complexity.loops import analyze_loops

def detect_recursion(tree):
    linear = False
    exponential = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            calls = 0
            func_name = node.name

            for inner in ast.walk(node):
                if isinstance(inner, ast.Call):
                    if isinstance(inner.func, ast.Name) and inner.func.id == func_name:
                        calls += 1

            if calls >= 2:
                exponential = True
            elif calls == 1:
                linear = True

    return linear, exponential


def estimate_loop_big_o(depth):
    if depth <= 0:
        return "O(1)"
    elif depth == 1:
        return "O(n)"
    elif depth == 2:
        return "O(n^2)"
    elif depth == 3:
        return "O(n^3)"
    else:
        return "O(n^k)"


def estimate_big_o(tree):
    loop_data = analyze_loops(tree)

    loop_depth = loop_data["max_loop_depth"]

    linear, exponential = detect_recursion(tree)

    # Recursion dominates loops
    if exponential:
        return {"estimated_big_o": "O(2^n)"}
    if linear:
        return {"estimated_big_o": "O(n)"}

    # No recursion → use loops
    return {
        "estimated_big_o": estimate_loop_big_o(loop_depth)
    }
