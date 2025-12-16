import ast

def analyze_loops(tree):
    total_loops = 0
    nested_loops_detected = False
    max_loop_depth = 0
    module_level_loops = 0
    loops_in_functions = {}
    current_function = None

    def loops_visit(node, depth):
        nonlocal total_loops, nested_loops_detected, max_loop_depth
        nonlocal module_level_loops, current_function

        # Detect function entry
        if isinstance(node, ast.FunctionDef):
            current_function = node.name
            loops_in_functions[current_function] = 0

        if isinstance(node, (ast.For, ast.While)):
            total_loops += 1
            depth += 1

            # module-level loop
            if current_function is None:
                module_level_loops += 1
            else:
                loops_in_functions[current_function] += 1
            
            # nested loop detection
            if depth >= 2:
                nested_loops_detected = True

            max_loop_depth = max(depth, max_loop_depth)

        for child in ast.iter_child_nodes(node):
            loops_visit(child, depth)

        # Detect leaving a function
        if isinstance(node, ast.FunctionDef):
            current_function = None
        
    loops_visit(tree, 0)

    return {
        "total_loops": total_loops,
        "max_loop_depth": max_loop_depth,
        "nested_loops_detected": nested_loops_detected,
        "module_level_loops": module_level_loops,
        "loops_in_functions": loops_in_functions
    }