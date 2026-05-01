from pydantic import BaseModel, Field
from typing import List, Optional

# Define the expected JSON structure
class ResumeSchema(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    location: str = Field(description="Location or address")
    linkedin: str = Field(description="LinkedIn URL")
    github: str = Field(description="GitHub URL")
    summary: str = Field(description="Professional summary")
    skills: List[str] = Field(description="List of skills")
    projects: List[dict] = Field(description="List of projects with 'name' and 'description'")
    education: List[dict] = Field(description="List of educational qualifications with 'degree', 'institution', and 'year'")
    experience: List[dict] = Field(description="List of work experiences with 'role', 'company', 'duration', and 'description'")
    certifications: List[str] = Field(description="List of certifications")
