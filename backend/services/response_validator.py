def validate_response(answer: str, record):


    if not answer.strip():
        return (
            "I'm sorry, but I couldn't generate a reliable response "
            "based on the available compliance information."
        )
    if len(answer.split()) < 8:
        return (
            "The generated response was too brief to provide useful "
            "compliance guidance."
        )
    if record.regulation.lower() not in answer.lower():
        print("Warning: Regulation name not found in LLM response.")
    return answer