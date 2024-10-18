from pydantic import BaseModel, Field
from typing import List, Optional
# AV84yrYMicEXWdjl
class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: Optional[str] = None  # Make this optional
    reference_id: Optional[str] = None  # Make this optional
    hint: Optional[str] = None  # Make this optional
    params: Optional[dict] = {}

class Section(BaseModel):
    marks_per_question: Optional[int] = 0  # Provide a default value if needed
    type: str
    questions: List[Question]

class PaperParams(BaseModel):
    board: Optional[str] = None  # If board can be empty, make it optional
    grade: Optional[int] = 0  # Provide a default value for grade
    subject: str

class SamplePaper(BaseModel):
    title: str
    type: str
    time: Optional[int] = 0  # Provide a default value for time
    marks: Optional[int] = 0  # Provide a default value for marks
    params: PaperParams
    tags: List[str]
    chapters: List[str]
    sections: List[Section]