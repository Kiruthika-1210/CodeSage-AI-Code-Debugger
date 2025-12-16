import ast
from analysis.common import make_issue


class _UnusedNameVisitor(ast.NodeVisitor):
    def __init__(self):
        # First scope = module scope
        self.scope_stack = [{"assigned": {}, "used": set()}]
        self.assigned_imports = []
        self.issues = []

    # Scope helpers
    def enter_scope(self):
        self.scope_stack.append({"assigned": {}, "used": set()})

    def exit_scope(self):
        return self.scope_stack.pop()

    def add_assigned(self, name, line):
        self.scope_stack[-1]["assigned"][name] = line

    def mark_used(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope["assigned"]:
                scope["used"].add(name)
                return

    # Visitors
    def visit_Import(self, node):
        for alias in node.names:
            self.assigned_imports.append({
                "name": alias.asname or alias.name,
                "line": node.lineno
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.assigned_imports.append({
                "name": alias.asname or alias.name,
                "line": node.lineno
            })
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.add_assigned(target.id, target.lineno)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name):
            self.add_assigned(node.target.id, node.target.lineno)
        self.generic_visit(node)

    def visit_For(self, node):
        if isinstance(node.target, ast.Name):
            self.add_assigned(node.target.id, node.target.lineno)
        self.generic_visit(node)

    def visit_With(self, node):
        for item in node.items:
            if isinstance(item.optional_vars, ast.Name):
                self.add_assigned(item.optional_vars.id, item.optional_vars.lineno)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if isinstance(node.name, str):
            self.add_assigned(node.name, node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.mark_used(node.id)

    def visit_FunctionDef(self, node):
        self.enter_scope()
        self.generic_visit(node)
        self._finalize_scope()
        self.exit_scope()

    def visit_AsyncFunctionDef(self, node):
        self.enter_scope()
        self.generic_visit(node)
        self._finalize_scope()
        self.exit_scope()

    def visit_ClassDef(self, node):
        self.enter_scope()
        self.generic_visit(node)
        self._finalize_scope()
        self.exit_scope()

    # Finalization
    def _finalize_scope(self):
        scope = self.scope_stack[-1]

        for name, line in scope["assigned"].items():
            if name.startswith("_"):
                continue
            if name not in scope["used"]:
                self.issues.append(
                    make_issue(
                        issue_type="unused-variable",
                        message=f"Variable '{name}' is assigned but never used.",
                        line=line,
                        severity="low",
                        suggestion=f"Remove variable '{name}' or use it."
                    )
                )


def rule_unused_names(code: str):
    """
    Detect unused variables and imports using AST-safe scope tracking.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    visitor = _UnusedNameVisitor()
    visitor.visit(tree)

    # Module-level unused vars
    module_scope = visitor.scope_stack[0]

    for name, line in module_scope["assigned"].items():
        if name.startswith("_"):
            continue
        if name not in module_scope["used"]:
            visitor.issues.append(
                make_issue(
                    issue_type="unused-variable",
                    message=f"Variable '{name}' is assigned but never used.",
                    line=line,
                    severity="low",
                    suggestion=f"Remove variable '{name}' or use it."
                )
            )

    # Unused imports
    all_used = set().union(*(s["used"] for s in visitor.scope_stack))

    for imp in visitor.assigned_imports:
        if imp["name"] not in all_used:
            visitor.issues.append(
                make_issue(
                    issue_type="unused-import",
                    message=f"Import '{imp['name']}' is never used.",
                    line=imp["line"],
                    severity="low",
                    suggestion=f"Remove the unused import '{imp['name']}'."
                )
            )

    return visitor.issues
