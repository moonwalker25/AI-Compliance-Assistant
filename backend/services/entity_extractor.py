import json

from prompts.entity_extraction_prompt import build_entity_prompt
from services.llm_service import ask_llm


def extract_entities(message):

    prompts = build_entity_prompt(message)

    response = ask_llm(
        prompts["system"],
        prompts["user"]
    )

    print("\nEntity Extraction:")
    print(response)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        return json.loads(response)

    except Exception:

        return {
            "country": None,
            "industry": None,
            "act": None,
            "particular": None
        }