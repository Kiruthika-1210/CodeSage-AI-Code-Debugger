import ast

def analyze_nest(tree):
    nests = (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.AsyncFor, ast.AsyncWith)
    max_nesting_depth = 0

    def nest_visit(node, depth):
        nonlocal max_nesting_depth

        # If this node is a nesting structure
        if isinstance(node, nests):
            depth += 1
            max_nesting_depth = max(max_nesting_depth, depth)

        # Visit child nodes
        for child in ast.iter_child_nodes(node):
            nest_visit(child, depth)

    nest_visit(tree, 0)

    return {
        "max_nesting_depth": max_nesting_depth
    }
