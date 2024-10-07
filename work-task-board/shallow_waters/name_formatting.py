import re

data = [
    "HELENE_K (07:30 - 15:00)",
    "KARINA_ELEV (07:30 - 15:00) Forventningssamtale",
    "LONE_R (07:30 - 12:00) Telefoner",
    "LONE_HE (07:30 - 15:00) Syopgaver 13:30 - 15.00",
    "ANJA_S",
    "ZEINAB_STUD1 (07:15 - 14:00)",
    "ALICE_Ø (07:30 - 16:00) Virtuel 13:30 - 14.00",
    "ANJA PBL 14-16",
    "LONE_R Møde kl 13-13.45",
]

# Updated regex pattern
pattern = r"^([^\s(]+(?:_[^\s(]+)?)\s*(?:\(([^)]+)\))?\s*(.*)$"

for entry in data:
    match = re.match(pattern, entry)
    if match:
        name_full = match.group(1).strip()
        timeslot = match.group(2) or ""
        extra = match.group(3).strip()

        # Split the name into first name and initials/moniker
        if "_" in name_full:
            first_name, initials_or_moniker = name_full.split("_", 1)
        else:
            first_name = name_full
            initials_or_moniker = ""

        # Detect if initials_or_moniker is a known moniker
        monikers = {"ELEV", "STUD", "STUD1"}
        is_moniker = initials_or_moniker.upper() in monikers

        print(f"Entry: {entry}")
        print(f"Full Name: {name_full}")
        print(f"  First Name: {first_name}")
        print(f"  Initials or Moniker: {initials_or_moniker} (Moniker: {is_moniker})")
        print(f"  Timeslot: {timeslot}")
        print(f"  Extra: {extra}")
        print("-" * 40)
    else:
        print(f"Could not parse entry: {entry}")
