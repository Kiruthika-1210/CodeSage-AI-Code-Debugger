import ast

def analyze_loops(tree):
    total_loops = 0
    nested_loops_detected = False
    max_loop_depth = 0
    module_level_loops = 0
    loops_in_functions = {}

    function_stack = []

    def loops_visit(node, depth):
        nonlocal total_loops, nested_loops_detected, max_loop_depth, module_level_loops

        # ---- Function entry (sync + async) ----
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_stack.append(node.name)
            loops_in_functions.setdefault(node.name, 0)

        # ---- Loop detection ----
        if isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
            total_loops += 1
            current_depth = depth + 1

            if function_stack:
                loops_in_functions[function_stack[-1]] += 1
            else:
                module_level_loops += 1

            if current_depth >= 2:
                nested_loops_detected = True

            max_loop_depth = max(max_loop_depth, current_depth)
        else:
            current_depth = depth

        # ---- Visit children ----
        for child in ast.iter_child_nodes(node):
            loops_visit(child, current_depth)

        # ---- Function exit (sync + async) ----
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_stack.pop()

    loops_visit(tree, 0)

    return {
        "total_loops": total_loops,
        "max_loop_depth": max_loop_depth,
        "nested_loops_detected": nested_loops_detected,
        "module_level_loops": module_level_loops,
        "loops_in_functions": loops_in_functions,
    }
