from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    unit: str
    topic: str
    marks: int
    bloom_level: str
    difficulty: str = Field(default="Medium")
    question: str
    model_answer: List[str]
    marking_scheme: List[str]

class Paper(BaseModel):
    title: str
    total_marks: int
    questions: List[Question]
    instructions: Optional[List[str]] = None
