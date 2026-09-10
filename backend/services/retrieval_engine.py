from sqlalchemy.orm import Session
from sqlalchemy import distinct, func

from models.compliance import (
    Compliance,
    Act,
    ComplianceParticular
)


# ============================================================
# GET ALL ACTS FOR A COUNTRY
# ============================================================

def get_all_acts(country: str, db: Session):

    print("\n========== GET ALL ACTS DEBUG ==========")
    print("Requested country:", repr(country))

    all_db_acts = db.query(Act).all()

    print("TOTAL ACTS IN DATABASE:", len(all_db_acts))

    print("\nALL ACT RECORDS:")

    for act in all_db_acts:
        print(
            f"Act: {act.act_name} | "
            f"Country: {repr(act.country)}"
        )

    acts = (
        db.query(
            distinct(Act.act_name)
        )
        .filter(
            func.lower(Act.country)
            ==
            country.strip().lower()
        )
        .all()
    )

    result = [
        act[0]
        for act in acts
        if act[0]
    ]

    print("\nMATCHED ACTS:", result)
    print("========================================\n")

    return result


# ============================================================
# GET PARTICULARS FOR AN ACT
# ============================================================

def get_particulars(
    act_name: str,
    db: Session
):

    act = (
        db.query(Act)
        .filter(
            func.lower(Act.act_name)
            ==
            act_name.strip().lower()
        )
        .first()
    )

    if not act:
        return []

    particulars = (
        db.query(
            distinct(ComplianceParticular.particular)
        )
        .filter(
            ComplianceParticular.act_id == act.id
        )
        .all()
    )

    return [
        particular[0]
        for particular in particulars
        if particular[0]
    ]


# ============================================================
# GET DESCRIPTION FOR A PARTICULAR
# ============================================================

def get_description(
    act_name: str,
    particular_name: str,
    db: Session
):

    act = (
        db.query(Act)
        .filter(
            func.lower(Act.act_name)
            ==
            act_name.strip().lower()
        )
        .first()
    )

    if not act:
        return None

    particulars = (
        db.query(ComplianceParticular)
        .filter(
            ComplianceParticular.act_id == act.id,
            func.lower(
                ComplianceParticular.particular
            )
            ==
            particular_name.strip().lower()
        )
        .all()
    )

    if not particulars:
        return None

    # Return the first non-empty description
    for particular in particulars:

        if (
            particular.description
            and particular.description.strip()
        ):

            return {
                "particular": particular.particular,
                "description": particular.description
            }

    # If descriptions are empty
    return {
        "particular": particulars[0].particular,
        "description": "Description not available."
    }


# ============================================================
# OLD RETRIEVAL FLOW
# TODO: Remove after new retrieval flow is fully integrated
# ============================================================

def retrieve_compliance(
    country: str,
    industry: str,
    db: Session
):

    result = (
        db.query(Compliance)
        .filter(
            func.lower(Compliance.country)
            ==
            country.strip().lower(),

            func.lower(Compliance.industry)
            ==
            industry.strip().lower()
        )
        .first()
    )

    return result