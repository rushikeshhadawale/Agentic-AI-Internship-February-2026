from utils.config import get_llm
from prompts.match_prompt import match_prompt

llm = get_llm()

match_chain = match_prompt | llm