DIRECT_EXTRACT_PROMPT = """
Analyze this resume document carefully. Extract all the information into valid JSON format.
Follow this schema exactly:
{
  "name": "Full Name",
  "email": "Email address",
  "phone": "Phone number",
  "location": "Location",
  "linkedin": "LinkedIn URL",
  "github": "GitHub URL",
  "objectives": "Professional summary",
  "skills": ["Skill 1", "Skill 2"],
  "projects": [{"name": "Project Name", "description": "Project Description"}],
  "education": [{"degree": "Degree", "institution": "Institution", "year": "Year"}],
  "experience": [{"role": "Role", "company": "Company", "duration": "Duration", "description": "Description"}],
  "certifications": ["Cert 1", "Cert 2"]
}
Return ONLY the raw JSON string, without any Markdown formatting or code blocks.
"""
