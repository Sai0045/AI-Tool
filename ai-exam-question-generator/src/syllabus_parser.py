import re
from typing import Dict, List

def parse_syllabus(text: str) -> Dict[str, List[str]]:
    """
    Supports:
    - Unit 1: topic1, topic2
    - Unit 1: ... Unit 2: ... (same line)
    - UNIT I, UNIT II (Roman numerals)
    """

    units: Dict[str, List[str]] = {}

    # Normalize spaces
    text = re.sub(r"\s+", " ", text.strip())

    # --- Case 1 & 2: Unit 1 / Unit 2 (even on same line)
    pattern = re.compile(r"(Unit\s+\d+\s*:)", re.IGNORECASE)
    splits = pattern.split(text)

    if len(splits) > 1:
        for i in range(1, len(splits), 2):
            unit_name = splits[i].strip().replace(":", "")
            content = splits[i + 1].strip()

            # Stop at next Unit if present
            content = re.split(r"Unit\s+\d+\s*:", content, flags=re.IGNORECASE)[0]

            topics = [t.strip() for t in content.split(",") if t.strip()]
            if topics:
                units[unit_name] = topics

        if units:
            return units

    # --- Case 3: Roman numerals (UNIT I, UNIT II)
    roman_pattern = re.compile(r"(UNIT\s+[IVX]+\b)", re.IGNORECASE)
    splits = roman_pattern.split(text)

    roman_map = {
        "I": "1", "II": "2", "III": "3",
        "IV": "4", "V": "5", "VI": "6"
    }

    if len(splits) > 1:
        for i in range(1, len(splits), 2):
            roman = splits[i].split()[-1].upper()
            unit_name = f"Unit {roman_map.get(roman, roman)}"
            content = splits[i + 1].strip()

            topics = [t.strip() for t in content.split(",") if t.strip()]
            if topics:
                units[unit_name] = topics

    return units
