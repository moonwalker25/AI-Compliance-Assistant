import json

from prompts.industry_reasoning_prompt import build_industry_prompt
from services.llm_service import ask_llm


def find_applicable_acts(country, industry, available_acts):

    print("\n========== INDUSTRY REASONER DEBUG ==========")
    print("Country:", country)
    print("Industry:", industry)
    print("Available Acts:", available_acts)
    print("Number of Available Acts:", len(available_acts))
    print("=============================================\n")

    prompts = build_industry_prompt(
        country,
        industry,
        available_acts
    )

    response = ask_llm(
        prompts["system"],
        prompts["user"]
    )

    print("\nRaw LLM Response:")
    print(response)

    clean_response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    print("\nClean Response:")
    print(clean_response)

    try:

        data = json.loads(clean_response)

        predicted_acts = data.get(
            "applicable_acts",
            []
        )

        print("\nPredicted Acts:")
        print(predicted_acts)

        validated_acts = []

        for act in predicted_acts:

            act = act.strip().upper()

            for db_act in available_acts:

                if act == db_act.strip().upper():
                    validated_acts.append(db_act)
                    break

        print("\nValidated Acts:")
        print(validated_acts)

        return validated_acts

    except Exception as e:

        print("JSON Parsing Error:", e)

        return []