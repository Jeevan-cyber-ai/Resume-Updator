from pydantic import BaseModel
from typing import Any, Dict

class CompareRequest(BaseModel):
    """Request body for POST /api/compare endpoint."""
    resume_data: Dict[str, Any]
    job_title: str

class CompareScores(BaseModel):
    """LLM-generated match scores for a resume vs job title."""
    title_score: int
    skill_score: int
    project_score: int
    objective_score: int
    title_suggestion: str
    skill_suggestion: str
    project_suggestion: str
    objective_suggestion: str

class CompareResponse(BaseModel):
    """Response body for POST /api/compare endpoint."""
    message: str
    job_title: str
    scores: CompareScores
