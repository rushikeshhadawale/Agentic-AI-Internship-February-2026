from utils.config import get_llm
from prompts.extract_prompt import extract_prompt

llm = get_llm()

extract_chain = extract_prompt | llm