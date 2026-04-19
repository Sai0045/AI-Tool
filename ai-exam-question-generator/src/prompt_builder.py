import json
from typing import Dict, List

def build_prompt(
    title: str,
    total_marks: int,
    units: Dict[str, List[str]],
    pattern: List[int],
    bloom_levels: List[str]   # ✅ NEW (one level per question)
) -> str:
    # ✅ EXACT instructions you want
    exam_instructions = [
        "Answer all questions.",
        "Marks for each question are indicated against each question.",
        "Draw neat diagrams wherever necessary.",
        "Justify your answers with suitable examples."
    ]

    # ✅ Example schema (structure guide)
    schema = {
        "title": "string",
        "total_marks": total_marks,
        "instructions": exam_instructions,
        "questions": [
            {
                "unit": "Unit 1",
                "topic": "string",
                "marks": 2,
                "bloom_level": "Remember/Understand/Apply/Analyze/Evaluate/Create",
                "difficulty": "Easy/Medium/Hard",
                "question": "string",
                "model_answer": ["point1", "point2"],
                "marking_scheme": ["part: marks", "part: marks"]
            }
        ]
    }

    # ✅ Safety: bloom list length should match number of questions
    n = len(pattern)
    if len(bloom_levels) != n:
        raise ValueError(
            f"bloom_levels length ({len(bloom_levels)}) must match total questions ({n})."
        )

    return f"""
You are a university exam paper setter.

Generate an exam paper strictly from the syllabus.
Follow the marks pattern EXACTLY: {pattern}
Total marks must be exactly: {total_marks}

IMPORTANT BLOOM RULE:
- There are {n} questions.
- Assign Bloom levels EXACTLY in this order for Q1..Q{n}:
{json.dumps(bloom_levels, indent=2)}
- Do NOT use a single Bloom level for all questions.

OUTPUT RULES:
- Output ONLY valid JSON.
- Do NOT add extra text or explanations.
- Use the instructions EXACTLY as given in the schema.
- The JSON must strictly follow this schema structure:
{json.dumps(schema, indent=2)}

INPUT:
Title: {title}
Syllabus (unit-wise topics):
{json.dumps(units, indent=2)}

QUALITY RULES:
- No duplicate questions.
- Model answers must be point-wise.
- Marking scheme must sum exactly to question marks.
""".strip()
