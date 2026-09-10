def detect_suggestion(message):

    original_message = message.strip()

    upper_message = original_message.upper()

    keywords = [
        "SHOULD ALSO APPLY",
        "ALSO APPLIES",
        "SHOULD APPLY",
        "IS MISSING",
        "SHOULD BE INCLUDED"
    ]

    for keyword in keywords:

        if keyword in upper_message:

            # Find where the suggestion phrase starts
            index = upper_message.find(keyword)

            # Everything before the keyword is treated as the Act name
            suggested_act = original_message[:index].strip()

            # Remove common punctuation
            suggested_act = suggested_act.rstrip(
                ".,!?;:"
            ).strip()

            return suggested_act

    return None