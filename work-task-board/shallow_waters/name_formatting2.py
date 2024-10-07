import toml
import re

# Valid monikers
config = toml.load("config.toml")
monikers = config["settings"]["valid_monikers"]

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


for entry in data:
    match = re.match(pattern, entry)
    if match:
        name = match.group(1)
        parentheses_content = match.group(2)

        is_moniker = None
        if parentheses_content is not None:
            # Detect if initials_or_moniker is a known moniker
            for moniker in monikers:
                if moniker.lower() in parentheses_content.lower():
                    is_moniker = True
                    break

        print(f"Entry: {entry}")
        print(f"Full Name: {name}")
        print(f"  Parentheses: {parentheses_content}")
        print(f"  Valid parentheses? : {is_moniker}")
        print("-" * 40)
    else:
        print(f"Could not parse entry: {entry}")
