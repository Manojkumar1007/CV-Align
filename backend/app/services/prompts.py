"""
Prompt templates for CV evaluation tasks using LLM
"""

CV_EVALUATION_PROMPTS = {
    "skills_evaluation": """Evaluate the candidate's skills based on the provided CV and job requirements. 
Consider both technical skills and their relevance to the position.
Rate the skills match on a scale of 0-100 where:
- 90-100: Excellent match, possesses all key skills and advanced expertise
- 70-89: Good match, has most required skills with some advanced capabilities
- 50-69: Moderate match, has basic required skills but lacks advanced expertise
- 30-49: Limited match, has some related skills but significant gaps
- 0-29: Poor match, skills do not align with requirements

CV Skills Section:
{cv_skills}

Job Requirements:
{job_requirements}

Provide only the numeric score (0-100) without any explanation or additional text:""",

    "experience_evaluation": """Evaluate the relevance and quality of the candidate's experience for the job. Consider:
- Years of experience in relevant field
- Progression and growth in roles
- Responsibilities and achievements that match job requirements
- Industry experience
- Leadership or management experience if relevant

Rate the experience match on a scale of 0-100 where:
- 90-100: Excellent match, extensive relevant experience with clear progression
- 70-89: Good match, solid relevant experience with some achievements
- 50-69: Moderate match, some relevant experience but limited
- 30-49: Limited match, minimal relevant experience
- 0-29: Poor match, experience not aligned with requirements

CV Experience Section:
{cv_experience}

Job Context:
{job_context}

Provide only the numeric score (0-100) without any explanation or additional text:""",

    "education_evaluation": """Evaluate the candidate's education against job requirements. Consider:
- Degree level relative to requirements
- Field of study relevance
- Institution prestige (if applicable)
- Additional certifications
- Continuing education or professional development

Rate the education match on a scale of 0-100 where:
- 90-100: Excellent match, exceeds educational requirements
- 70-89: Good match, meets all educational requirements
- 50-69: Moderate match, meets minimum requirements
- 30-49: Limited match, partially meets requirements
- 0-29: Poor match, does not meet requirements

CV Education Section:
{cv_education}

Job Requirements:
{job_requirements}

Provide only the numeric score (0-100) without any explanation or additional text:""",

    "soft_skills_evaluation": """Analyze the candidate's CV for evidence of soft skills relevant to the job. 
Identify signs of communication, teamwork, leadership, problem-solving, adaptability, and other interpersonal skills.
Rate the soft skills indication on a scale of 0-100 where:
- 90-100: Strong evidence of soft skills throughout the CV
- 70-89: Good evidence of soft skills with specific examples
- 50-69: Moderate evidence of soft skills
- 30-49: Limited evidence of soft skills
- 0-29: Little to no evidence of soft skills

CV Sections:
{cv_text}

Job Context:
{job_context}

Provide only the numeric score (0-100) without any explanation or additional text:""",

    "contextual_understanding": """Analyze the candidate's CV in the context of the specific job requirements and industry. 
Consider how well the candidate's background aligns with the role's specific needs, company culture, and industry trends.
Rate the contextual alignment on a scale of 0-100 where:
- 90-100: Excellent alignment with role, company culture, and industry needs
- 70-89: Good alignment considering the context of the role
- 50-69: Moderate alignment with contextual factors
- 30-49: Limited alignment with the specific role context
- 0-29: Poor alignment with role context and company needs

CV:
{cv_text}

Job Description:
{job_description}

Job Requirements:
{job_requirements}

Company/Industry Context:
{context_info}

Provide only the numeric score (0-100) without any explanation or additional text:""",

    "feedback_generation": """Based on the CV and job requirements, generate specific and actionable feedback. Provide feedback in the following JSON format:

{{
    "strengths": ["specific strength 1", "specific strength 2", ...],
    "weaknesses": ["specific weakness 1", "specific weakness 2", ...],
    "recommendations": ["specific recommendation 1", "specific recommendation 2", ...],
    "summary": "A concise summary of the candidate's fit for the position."
}}

CV:
{cv_text}

Job Description:
{job_description}

Job Requirements:
{job_requirements}

Provide only the JSON response without any explanation or additional text:""",

    "detailed_feedback_with_soft_skills": """Based on the CV and job requirements, generate comprehensive feedback that includes assessment of soft skills. 
Focus on both technical qualifications and interpersonal abilities.
Provide feedback in the following JSON format:

{{
    "strengths": ["specific strength 1", "specific strength 2", ...],
    "weaknesses": ["specific weakness 1", "specific weakness 2", ...],
    "recommendations": ["specific recommendation 1", "specific recommendation 2", ...],
    "soft_skills_assessment": ["soft skill observation 1", "soft skill observation 2", ...],
    "summary": "A concise summary of the candidate's fit for the position."
}}

CV:
{cv_text}

Job Description:
{job_description}

Job Requirements:
{job_requirements}

Provide only the JSON response without any explanation or additional text:"""
}