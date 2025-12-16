def analyze_documentation(code: str):

    MAX_DOC_PENALTY = 10

    slices = code.split("\n")
    penalty = 0

    # 1. CHECK MODULE DOCSTRING
    first_real_line = ""
    for line in slices:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            first_real_line = stripped
            break

    # Missing module docstring
    if not (first_real_line.startswith('"""') or first_real_line.startswith("'''")):
        penalty += 10

    # 2. FUNCTION & CLASS DOCSTRING CHECKS
    i = 0
    n = len(slices)

    while i < n:
        line = slices[i].strip()

        # FUNCTION DOCSTRING CHECK
        if line.startswith("def "):
            # Extract parameters
            fn_signature = line
            params_section = fn_signature[fn_signature.find("(") + 1 : fn_signature.find(")")]
            params = [p.strip() for p in params_section.split(",") if p.strip()]

            # Move to next meaningful line
            j = i + 1
            while j < n and slices[j].strip() == "":
                j += 1

            # Check if next meaningful line is a docstring
            if j >= n or not (slices[j].strip().startswith('"""') or slices[j].strip().startswith("'''")):
                penalty += 5
            else:
                # Extract docstring content
                doc = slices[j].strip()

                # Check short docstring
                if doc in ['"""', "'''"]:
                    penalty += 3
                elif len(doc.replace('"', "").replace("'", "").strip()) < 3:
                    penalty += 3

                # Check parameter names appear in docstring
                doc_lower = doc.lower()
                for p in params:
                    if p and p not in doc_lower:
                        penalty += 1  # small penalty per missing param

            i = j

        # CLASS DOCSTRING CHECK
        elif line.startswith("class "):
            j = i + 1
            while j < n and slices[j].strip() == "":
                j += 1

            if j >= n or not (slices[j].strip().startswith('"""') or slices[j].strip().startswith("'''")):
                penalty += 5

            i = j
        else:
            i += 1

    # FINAL DOCUMENTATION SCORE
    penalty = min(penalty, MAX_DOC_PENALTY)
    documentation_score = max(15, 25 - penalty)

    return {
        "documentation_score": documentation_score
    }
