def build_verification_prompt(
    country,
    industry,
    suggested_act,
    available_acts
):

    acts = "\n".join(available_acts)

    system_prompt = """
You are an Enterprise Compliance Expert.

Your task is to verify whether a suggested Act is applicable to a given industry.

Rules:

1. Use compliance knowledge.
2. Be conservative.
3. Do not guess.
4. If uncertain, return applicable=false.
5. Return ONLY valid JSON.
6. Do NOT wrap JSON inside markdown.
"""

    user_prompt = f"""
Country:
{country}

Industry:
{industry}

Suggested Act:
{suggested_act}

Available Acts:

{acts}

Return JSON in this format:

{{
    "applicable": true,
    "confidence": 95,
    "reason": "Explain why."
}}
"""

    return {
        "system": system_prompt,
        "user": user_prompt
    }