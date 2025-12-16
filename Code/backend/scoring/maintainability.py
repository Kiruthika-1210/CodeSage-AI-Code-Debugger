def analyze_maintainability(code: str):
    lines = code.splitlines()
    penalty = 0

    # FUNCTION LENGTH
    functions = []
    n = len(lines)
    i = 0

    while i < n:
        if lines[i].lstrip().startswith("def "):
            start = i
            indent = len(lines[i]) - len(lines[i].lstrip())
            i += 1

            while i < n:
                curr_indent = len(lines[i]) - len(lines[i].lstrip())
                if curr_indent <= indent and lines[i].strip():
                    break
                i += 1

            length = i - start
            functions.append(length)
        else:
            i += 1

    for length in functions:
        if length > 50:
            penalty += 8
        elif length > 30:
            penalty += 5

    # REPEATED LOGIC 
    seen = set()
    repeat_hits = 0

    for i in range(len(lines) - 2):
        block = (
            lines[i].strip(),
            lines[i + 1].strip(),
            lines[i + 2].strip(),
        )

        if not any(block):
            continue

        if block in seen:
            repeat_hits += 1
        else:
            seen.add(block)

    if repeat_hits >= 2:
        penalty += 5   

    # DEEP NESTING 
    max_depth = 0
    for line in lines:
        if line.strip():
            depth = (len(line) - len(line.lstrip())) // 4
            max_depth = max(max_depth, depth)

    if max_depth >= 6:
        penalty += 6
    elif max_depth >= 4:
        penalty += 3

    # BRANCH COUNT
    branch_count = sum(
        1 for line in lines
        if line.strip().startswith(("if ", "elif ", "else:", "match ", "case "))
    )

    if branch_count >= 6:
        penalty += 6
    elif branch_count >= 4:
        penalty += 3

    # FINAL SCORE
    penalty = min(penalty, 25)
    score = max(0, 25 - penalty)

    return {
        "maintainability_score": score
    }
