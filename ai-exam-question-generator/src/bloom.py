BLOOM_LEVELS = [
    "Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"
]

# Simple action verbs to guide question style
BLOOM_VERBS = {
    "Remember": ["define", "list", "state", "identify"],
    "Understand": ["explain", "summarize", "describe", "interpret"],
    "Apply": ["solve", "use", "demonstrate", "implement"],
    "Analyze": ["compare", "differentiate", "analyze", "examine"],
    "Evaluate": ["justify", "critique", "evaluate", "argue"],
    "Create": ["design", "propose", "develop", "formulate"]
}

def pick_bloom_level(preferred: str | None = None) -> str:
    if preferred and preferred in BLOOM_LEVELS:
        return preferred
    return "Understand"

def verbs_for(level: str) -> list[str]:
    return BLOOM_VERBS.get(level, ["explain"])
