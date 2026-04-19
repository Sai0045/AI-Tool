import random
from typing import Dict, List, Optional
from .bloom import pick_bloom_level, verbs_for
from .paper_schema import Question, Paper

DIFFICULTY_BY_MARKS = {
    2: "Easy",
    5: "Medium",
    10: "Hard"
}

def simple_question_builder(topic: str, marks: int, bloom: str) -> str:
    verb = random.choice(verbs_for(bloom))
    if marks == 2:
        return f"{verb.title()} {topic}."
    if marks == 5:
        return f"{verb.title()} {topic} with suitable example."
    return f"{verb.title()} {topic} in detail with diagram/steps and justify your answer."

def simple_model_answer(topic: str, marks: int, bloom: str) -> List[str]:
    # Exam-style point-wise answers
    if marks == 2:
        return [
            f"{topic} is explained briefly as per the definition.",
            "Key point is stated clearly in one or two lines."
        ]
    if marks == 5:
        return [
            f"Definition/meaning of {topic} is written clearly.",
            "Main points are explained in 4–6 bullet points.",
            "One suitable example is included.",
            "Conclusion line is added."
        ]
    return [
        f"Introduction and definition of {topic}.",
        "Detailed explanation with proper steps/working.",
        "Diagram / flow / pseudo-code (if applicable).",
        "Advantages, limitations, and use-cases.",
        "One real example/case study.",
        "Final conclusion."
    ]

def simple_marking_scheme(marks: int) -> List[str]:
    if marks == 2:
        return ["Correct definition: 1", "One key point/example: 1"]
    if marks == 5:
        return ["Definition: 1", "Core explanation points: 3", "Example + conclusion: 1"]
    return ["Intro/definition: 2", "Core steps/derivation: 5", "Example/diagram: 2", "Conclusion: 1"]

def generate_paper(
    title: str,
    units: Dict[str, List[str]],
    pattern: List[int],
    bloom_preference: Optional[str] = None,
    seed: Optional[int] = None
) -> Paper:
    """
    pattern: list of marks for each question, e.g. [2,2,2,5,5,10]
    """
    if seed is not None:
        random.seed(seed)

    all_unit_topics = []
    for unit, topics in units.items():
        for topic in topics:
            all_unit_topics.append((unit, topic))

    if not all_unit_topics:
        raise ValueError("No topics found. Please check syllabus format.")

    questions: List[Question] = []
    used_questions = set()

    for marks in pattern:
        unit, topic = random.choice(all_unit_topics)
        bloom = pick_bloom_level(bloom_preference)
        difficulty = DIFFICULTY_BY_MARKS.get(marks, "Medium")

        q_text = simple_question_builder(topic, marks, bloom)
        # avoid duplicates
        tries = 0
        while q_text.lower() in used_questions and tries < 10:
            unit, topic = random.choice(all_unit_topics)
            q_text = simple_question_builder(topic, marks, bloom)
            tries += 1

        used_questions.add(q_text.lower())

        questions.append(
            Question(
                unit=unit,
                topic=topic,
                marks=marks,
                bloom_level=bloom,
                difficulty=difficulty,
                question=q_text,
                model_answer=simple_model_answer(topic, marks, bloom),
                marking_scheme=simple_marking_scheme(marks)
            )
        )

    total_marks = sum(pattern)
    instructions = [
        "All questions are compulsory unless mentioned.",
        "Write answers in points with neat diagram wherever required.",
        "Attempt the paper in a clean and structured format."
    ]
    return Paper(title=title, total_marks=total_marks, questions=questions, instructions=instructions)
