from models.compliance import IndustryActMapping


def save_mapping(country, industry, acts, db):

    for act in acts:

        existing = (
            db.query(IndustryActMapping)
            .filter(
                IndustryActMapping.country == country,
                IndustryActMapping.industry_name == industry,
                IndustryActMapping.act_name == act
            )
            .first()
        )

        if existing:
            continue

        mapping = IndustryActMapping(
            country=country,
            industry_name=industry,
            act_name=act
        )

        db.add(mapping)

    db.commit()
    
def get_mapping(country, industry, db):

    mappings = (
        db.query(IndustryActMapping)
        .filter(
            IndustryActMapping.country == country,
            IndustryActMapping.industry_name == industry
        )
        .all()
    )

    return [mapping.act_name for mapping in mappings]