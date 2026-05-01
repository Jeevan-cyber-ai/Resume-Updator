IMPROVE_OBJECTIVE_PROMPT = """
You are an expert technical resume writer.

Your task is to write a highly professional, impactful resume objective/summary for a candidate.

Target Job Title: {job_title}

Candidate's current/past experience:
{experience}

Candidate's rough input or goal:
{user_input}

Feedback from the candidate on previous drafts (if any):
{feedback_history}

Instructions:
1. Write a professional objective/summary paragraph (3-4 sentences max).
2. It MUST be tailored to the '{job_title}' role.
3. Incorporate the candidate's rough input in a professional, action-oriented way.
4. If there is feedback history, ensure you adjust the tone, length, or focus according to their latest feedback.
5. Return ONLY the final polished text. Do not include any conversational filler like "Here is your summary:"
"""

IMPROVE_PROJECTS_PROMPT = """
You are an expert technical resume writer.

Your task is to write professional, impact-driven bullet points for a project the candidate worked on.

Target Job Title: {job_title}

Candidate's rough input about the project (what they did, tech used):
{user_input}

Feedback from the candidate on previous drafts (if any):
{feedback_history}

Instructions:
1. Write 3-4 professional bullet points using the STAR method (Situation, Task, Action, Result).
2. Start each bullet point with a strong action verb (e.g., Developed, Architected, Optimized).
3. Weave the technologies used naturally into the bullet points.
4. If there is feedback history, adjust the bullet points to address their feedback exactly.
5. Return ONLY the bullet points (using standard markdown bullets '-'). Do not include any conversational filler.
"""

IMPROVE_SKILLS_PROMPT = """
You are an expert technical recruiter.

Target Job Title: {job_title}

Candidate's Current Skills:
{current_skills}

Instructions:
1. Analyze the target job title and the candidate's current skills.
2. Identify highly relevant skills, tools, and technologies for the '{job_title}' role that the candidate might be missing.
3. Suggest a clean, comma-separated list of 10-15 skills that would strengthen this resume.
4. Only suggest skills that are realistic for their level of experience.
5. Return ONLY the comma-separated list of skills. No introductory text.
"""
