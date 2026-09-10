COMPLIANCE_KEYWORDS = [
    "compliance",
    "regulation",
    "law",
    "policy",
    "gdpr",
    "hipaa",
    "iso",
    "security",
    "privacy",
    "risk",
    "audit"
]


def is_compliance_query(message, history=None):
    message = message.lower()

    if history:
        for chat in history:
            message += " " + chat["content"].lower()

    return any(
        keyword in message
        for keyword in COMPLIANCE_KEYWORDS
    )