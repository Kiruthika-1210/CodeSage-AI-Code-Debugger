def analyze_style(code: str):

    MAX_STYLE_LOSS = 8

    slices = []
    penalty = 0

    # SPLIT CODE INTO LINES
    current_line = ""
    for ch in code:
        if ch == "\n":
            slices.append(current_line)
            current_line = ""
        else:
            current_line += ch
    if current_line:
        slices.append(current_line)

    for line in slices:
        stripped = line.strip()

        # Trailing spaces
        if line.endswith(" "):
            penalty += 2

        # Bad parentheses around conditions: if(x==1):
        if stripped.startswith(("if(", "elif(", "while(")):
            penalty += 4

        # Bad spacing around '=' (ignore '==')
        if "=" in line and "==" not in line:
            idx = line.index("=")
            left = line[idx - 1] if idx > 0 else ""
            right = line[idx + 1] if idx < len(line) - 1 else ""

            if left != " " or right != " ":
                penalty += 3

        # Bad spacing around + - * /
        operators = ["+", "-", "*", "/"]
        for op in operators:
            if op in line:
                pos = line.index(op)

                left = line[pos - 1] if pos > 0 else ""
                right = line[pos + 1] if pos < len(line) - 1 else ""

                # Skip augmented operators like +=
                if left == op or right == "=":
                    continue

                if left != " " or right != " ":
                    penalty += 3

        # Colon misuse - statement on same line
        if ":" in line:
            parts = line.split(":")
            if len(parts) > 1 and parts[1].strip() != "":
                penalty += 3

    # Missing newline at end of file
    if slices and slices[-1].strip() != "":
        penalty += 2

    # Final style score
    penalty = min(penalty, MAX_STYLE_LOSS)
    style_score = max(10, 25 - penalty)

    return {
        "style_score": style_score
    }
