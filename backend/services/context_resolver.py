from services.entity_extractor import extract_entities


def resolve_context(message, history):
    current_entities=extract_entities(message)

    country = current_entities["country"]
    industry = current_entities["industry"]

    for chat in reversed(history):
        if chat["role"] != "user":
            continue

        previous_entities = extract_entities(chat["content"])

        if country is None and previous_entities["country"]:
            country = previous_entities["country"]

        if industry is None and previous_entities["industry"]:
            industry = previous_entities["industry"]

        if country and industry:
            break
    
    print("\n========== Context Resolver ==========")
    print("Original Message :", message)
    print("Resolved Country :", country)
    print("Resolved Industry:", industry)
    print("======================================")

    return {
        "message": message,
        "country": country,
        "industry": industry
    }

