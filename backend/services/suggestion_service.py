from models.compliance import MappingSuggestion

def save_suggestion(
    country,
    industry,
    act,
    verification,
    db
):
    existing = (
        db.query(MappingSuggestion)
        .filter(
            MappingSuggestion.country == country,
            MappingSuggestion.industry == industry,
            MappingSuggestion.suggested_act == act,
            MappingSuggestion.status == "PENDING"
        )
        .first()
    )

    if existing:
        return existing
    
    suggestion = MappingSuggestion(

        country=country,

        industry=industry,

        suggested_act=act,

        ai_reason=verification["reason"],

        confidence=verification["confidence"],

        status="PENDING"
    )
    db.add(suggestion)

    db.commit()

    db.refresh(suggestion)

    return suggestion