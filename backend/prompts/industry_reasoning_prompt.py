def build_industry_prompt(
    country,
    industry,
    acts
):
    act_list = "\n".join(
        f"- {act}"
        for act in acts
    )

    system_prompt = """
You are an Enterprise AI Compliance Assistant.

Your task is to identify which Acts from the supplied list are
reasonably applicable to organizations operating in the selected
industry and country.

IMPORTANT:

An Act should be included only if it has a clear and meaningful
connection to the selected industry or generally applies to businesses
operating in that industry.

Do NOT include an Act merely because it could theoretically apply to
any business.

Be selective and relevant.

Rules:

1. Choose ONLY from the supplied list of Acts.

2. Return an Act only when it is reasonably applicable to the selected
industry.

3. Do not include Acts that are primarily relevant to unrelated
industries.

4. General business, employment, taxation, corporate, data protection,
or regulatory Acts may be included when they reasonably apply to
organizations in the selected industry.

5. If none of the supplied Acts are reasonably applicable, return:

{
    "applicable_acts": []
}

6. Never invent new Acts.

7. Every returned Act MUST exactly match an Act from the supplied list.

8. Do not return duplicate Acts.

9. Return ONLY valid JSON.

10. Do NOT include explanations.

11. Do NOT wrap the response in markdown code blocks.

Required response format:

{
    "applicable_acts": [
        "ACT NAME"
    ]
}
"""

    user_prompt = f"""
Country:
{country}

Selected Industry:
{industry}

Available Acts:

{act_list}

Identify ONLY the Acts that are reasonably and meaningfully applicable
to organizations operating in the selected industry.

Be selective. Do not return Acts simply because they might apply to
any company.

Return only the JSON object.
"""

    return {
        "system": system_prompt,
        "user": user_prompt
    }