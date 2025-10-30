from pydantic import BaseModel
from typing import Optional, Dict, Any

class MathQuestion(BaseModel):
    question: str
    user_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    question: str
    original_solution: Dict[str, Any]
    feedback: str
    improved_solution: Optional[str] = None