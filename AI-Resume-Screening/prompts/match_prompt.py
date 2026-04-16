from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
Compare resume with job description.

Return JSON:
{{
  "matching_skills": [],
  "missing_skills": []
}}

Job Description:
{job_description}

Resume Data:
{resume_data}
"""
)