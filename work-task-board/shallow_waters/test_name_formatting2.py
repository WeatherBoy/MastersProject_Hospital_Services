import re

data = [
    "Laura K. A.",
    "Anette W.",
    "Anja",
    "Karina (Elev)",
    "Charlotte S. I. F.",
    "Zeinab (Stud1)",
    "Kim",
    "Alice Ø.",
    "Lønne",
]

# Updated regex pattern
pattern = r"^([A-Za-zÆØÅæøå]+(?:\s[A-Za-zÆØÅæøå]\.)*)\s*(?:\(([^)]+)\))?$"

# Valid monikers
monikers = {"elev", "stud", "stud1"}

for entry in data:
    match = re.match(pattern, entry)
    if match:
        name = match.group(1)
        parentheses_content = match.group(2)

        is_moniker = None
        if parentheses_content is not None:
            # Detect if initials_or_moniker is a known moniker
            is_moniker = parentheses_content.lower() in monikers

        print(f"Entry: {entry}")
        print(f"Full Name: {name}")
        print(f"  Parentheses: {parentheses_content}")
        print(f"  Valid parentheses? : {is_moniker}")
        print("-" * 40)
    else:
        print(f"Could not parse entry: {entry}")
