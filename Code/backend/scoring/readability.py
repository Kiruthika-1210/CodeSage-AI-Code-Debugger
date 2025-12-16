def analyze_readability(code: str):

    MAX_READABILITY_LOSS = 12

    penalty = 0
    base_score = 25
    slices = []

    # Split code into lines
    current_line = ""
    for i in code:
        if i == "\n":
            slices.append(current_line)
            current_line = ""
        else:
            current_line += i
    if current_line:
        slices.append(current_line)

    indent_set = set()

    for line in slices:
        stripped = line.strip()

        # 1. Check long lines
        if len(line) > 100:
            penalty += 5

        # 2. Check indentation consistency
        if stripped == "" or (not line.startswith(" ") and not line.startswith("\t")):
            continue

        space_count = 0
        tab_count = 0

        for ch in line:
            if ch == " ":
                space_count += 1
            elif ch == "\t":
                tab_count += 1
            else:
                break

        # Ignore lines with no indentation
        if space_count == 0 and tab_count == 0:
            continue

        # Store indentation style
        if tab_count > 0:
            indent_set.add(f"tab:{tab_count}")
        else:
            indent_set.add(f"spaces:{space_count}")

        # 3. Check multiple statements
        if ";" in line:
            penalty += 5

        # 4. Detect weird variable names
        if "=" in line and "==" not in line:  # ensure it's an assignment, not comparison
            var_name = line.split("=")[0].strip()
            
            if (len(var_name) <= 2) or (len(var_name) == 2 and var_name[0].isalpha() and var_name[1].isdigit()):
                penalty += 5

    # Inconsistent indentation
    if len(indent_set) > 1:
        penalty += 5

    # 5. Missing blank lines between functions
    for idx, line in enumerate(slices):
        if line.lstrip().startswith("def "):
            if idx > 0:
                if slices[idx - 1].strip() != "":
                    penalty += 5

    


    # Score clamp
    penalty = min(penalty, MAX_READABILITY_LOSS)
    readability_score = max(0, base_score - penalty)

    return {"readability_score": readability_score}
