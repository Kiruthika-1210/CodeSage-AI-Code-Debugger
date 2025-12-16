# generator.py — Diff Engine
# Responsibilities:
# - Generate unified diff
# - Produce summary


import difflib

def generate_diff(old_code: str, new_code: str) -> dict:
    """
    Accepts:
      old_code -> original code version (string)
      new_code -> refactored code version (string)

    Returns:
      A dictionary containing:
        - unified diff text
        - summary of changes
    """

    old_code = old_code or ""
    new_code = new_code or ""

    # If both versions are identical - no diff needed
    if old_code.strip() == new_code.strip():
        return {
            "diff": "",
            "summary": "No changes detected"
        }

    try:
        old_lines = old_code.splitlines(keepends=True)
        new_lines = new_code.splitlines(keepends=True)

        # Generate unified diff (GitHub style)
        diff_lines = list(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile="original",
                tofile="refactored",
                lineterm=""
            )
        )

        # Combine lines into one full diff text
        diff_text = "\n".join(diff_lines)

        # Count changes for summary
        added = 0
        removed = 0

        for line in diff_lines:

            # Ignore diff metadata
            if (
                line.startswith("---") or
                line.startswith("+++") or
                line.startswith("@@")
            ):
                continue

            # Ignore file labels in unified diff
            if line.startswith("+original") or line.startswith("-refactored"):
                continue

            if line.startswith("+"):
                added += 1
            elif line.startswith("-"):
                removed += 1

        # Modified lines = lines that changed (paired add/remove)
        modified = min(added, removed)

        summary = f"{added} lines added, {removed} removed, {modified} modified"

        return {
            "diff": diff_text,
            "summary": summary
        }

    except Exception:
        return {
            "diff": "",
            "summary": "Diff generation failed"
        }
