from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["score", "match_result"],
    template="""
Explain why this score was assigned.

Return short explanation.

Score:
{score}

Match:
{match_result}
"""
)