from sqlalchemy.orm import Session
from sqlalchemy import func

from models.compliance import IndustryActMapping


def get_industries_by_country(country: str, db: Session):

    industries = (
        db.query(IndustryActMapping.industry_name)
        .filter(
            func.lower(IndustryActMapping.country)
            == country.strip().lower()
        )
        .all()
    )

    cleaned_industries = {}

    for industry in industries:

        industry_name = industry[0]

        if not industry_name:
            continue

        cleaned_name = industry_name.strip()

        # Ignore invalid generic values
        if cleaned_name.lower() in [
            "industry",
            "industries",
            "unknown",
            "none",
            "n/a"
        ]:
            continue

        # Case-insensitive deduplication
        key = cleaned_name.lower()

        if key not in cleaned_industries:
            cleaned_industries[key] = cleaned_name.title()

    return sorted(cleaned_industries.values())