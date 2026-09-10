def build_entity_prompt(message):

    system_prompt = """
You are an AI Entity Extraction Engine.

Extract the following entities from the user's message.

Return ONLY valid JSON.

Schema:

{
    "country": "...",
    "industry": "...",
    "act": "...",
    "particular": "..."
}

Rules:

1. If an entity is absent, return null.
2. Never explain anything.
3. Never return markdown.
4. Return JSON only.
"""

    user_prompt = f"""
Extract entities from:

{message}
"""

    return {
        "system": system_prompt,
        "user": user_prompt
    }