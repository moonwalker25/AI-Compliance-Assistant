from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database.database import get_db

from models.compliance import (
    MappingSuggestion,
    IndustryActMapping
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ============================================================
# GET PENDING SUGGESTIONS
# ============================================================

@router.get("/suggestions")
def get_pending(
    db: Session = Depends(get_db)
):

    suggestions = (
        db.query(MappingSuggestion)
        .filter(
            MappingSuggestion.status == "PENDING"
        )
        .order_by(
            MappingSuggestion.id.desc()
        )
        .all()
    )

    return [
        {
            "id": suggestion.id,
            "country": suggestion.country,
            "industry": suggestion.industry,
            "suggested_act": suggestion.suggested_act,
            "ai_reason": suggestion.ai_reason,
            "confidence": suggestion.confidence,
            "status": suggestion.status
        }
        for suggestion in suggestions
    ]


# ============================================================
# APPROVE SUGGESTION
# ============================================================

@router.post("/approve/{suggestion_id}")
def approve_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db)
):

    suggestion = (
        db.query(MappingSuggestion)
        .filter(
            MappingSuggestion.id == suggestion_id
        )
        .first()
    )

    # --------------------------------------------------------
    # SUGGESTION NOT FOUND
    # --------------------------------------------------------

    if not suggestion:

        raise HTTPException(
            status_code=404,
            detail="Suggestion not found."
        )

    # --------------------------------------------------------
    # PREVENT PROCESSING TWICE
    # --------------------------------------------------------

    if suggestion.status != "PENDING":

        raise HTTPException(
            status_code=400,
            detail=(
                f"This suggestion has already been "
                f"{suggestion.status.lower()}."
            )
        )

    # ========================================================
    # CHECK IF MAPPING ALREADY EXISTS
    # ========================================================

    existing_mapping = (
        db.query(IndustryActMapping)
        .filter(
            IndustryActMapping.country
            == suggestion.country,

            IndustryActMapping.industry_name
            == suggestion.industry,

            IndustryActMapping.act_name
            == suggestion.suggested_act
        )
        .first()
    )

    mapping_created = False

    try:

        # ====================================================
        # CREATE MAPPING IF IT DOESN'T ALREADY EXIST
        # ====================================================

        if not existing_mapping:

            mapping = IndustryActMapping(

                country=suggestion.country,

                industry_name=suggestion.industry,

                act_name=suggestion.suggested_act
            )

            db.add(mapping)

            mapping_created = True

        # ====================================================
        # UPDATE SUGGESTION STATUS
        # ====================================================

        suggestion.status = "APPROVED"

        db.commit()

        db.refresh(suggestion)

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to approve suggestion: {str(e)}"
        )

    return {
        "message": "Suggestion approved successfully.",
        "status": suggestion.status,
        "suggestion_id": suggestion.id,
        "mapping_created": mapping_created
    }


# ============================================================
# REJECT SUGGESTION
# ============================================================

@router.post("/reject/{suggestion_id}")
def reject_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db)
):

    suggestion = (
        db.query(MappingSuggestion)
        .filter(
            MappingSuggestion.id == suggestion_id
        )
        .first()
    )

    # --------------------------------------------------------
    # SUGGESTION NOT FOUND
    # --------------------------------------------------------

    if not suggestion:

        raise HTTPException(
            status_code=404,
            detail="Suggestion not found."
        )

    # --------------------------------------------------------
    # PREVENT PROCESSING TWICE
    # --------------------------------------------------------

    if suggestion.status != "PENDING":

        raise HTTPException(
            status_code=400,
            detail=(
                f"This suggestion has already been "
                f"{suggestion.status.lower()}."
            )
        )

    try:

        # ====================================================
        # UPDATE STATUS
        # ====================================================

        suggestion.status = "REJECTED"

        db.commit()

        db.refresh(suggestion)

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to reject suggestion: {str(e)}"
        )

    return {
        "message": "Suggestion rejected successfully.",
        "status": suggestion.status,
        "suggestion_id": suggestion.id
    }