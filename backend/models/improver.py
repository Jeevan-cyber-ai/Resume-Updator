from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class FeedbackMessage(BaseModel):
    role: str # "ai" or "user"
    content: str

class ImproveRequest(BaseModel):
    """Request body for POST /api/improve endpoint."""
    section: str # "title", "objective", "skills", or "projects"
    resume_data: Dict[str, Any]
    job_title: str
    user_input: str # The user's rough draft or instructions
    feedback_history: Optional[List[FeedbackMessage]] = [] # Previous iterations for HITL

class ImproveResponse(BaseModel):
    """Response body for POST /api/improve endpoint."""
    message: str
    generated_output: str # The polished AI output
