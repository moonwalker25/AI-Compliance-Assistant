from services.llm_service import ask_llm

system_prompt = """
You are an expert compliance assistant.
Answer only using the provided compliance information.
"""

user_prompt = """
Country: India

Industry: Healthcare

Regulation: Clinical Establishments Act

Description:
Hospitals must register with the appropriate authority.

User Question:
What are the healthcare regulations in India?
"""

answer = ask_llm(system_prompt, user_prompt)

print(answer)