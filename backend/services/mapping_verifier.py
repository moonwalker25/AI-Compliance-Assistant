import json

from prompts.verify_mapping_prompt import build_verification_prompt

from services.llm_service import ask_llm

def verify_mapping(
    country,
    industry,
    suggested_act,
    available_acts
):
        prompts = build_verification_prompt(
            country,
            industry,
            suggested_act,
            available_acts
        )
        response = ask_llm(
            prompts["system"],
            prompts["user"]
        )
        print("\nRaw Verification Response:")
        print(response)

        clean_response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )
        try:

            data = json.loads(clean_response)

            return data

        except Exception as e:

            print("Verification Parsing Error:", e)

            return {
                "applicable": False,
                "confidence": 0,
                "reason": "Unable to verify."
            }