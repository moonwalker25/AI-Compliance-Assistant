from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.compliance import Compliance

router = APIRouter()

@router.get("/compliance")
def get_compliance(
    country: str,
    industry: str,
    db: Session = Depends(get_db)
):
    record = (
        db.query(Compliance)
        .filter(
            Compliance.country == country,
            Compliance.industry == industry
        )
        .first()
    )
    if not record:

        return {
            "message": "No compliance rule found."
        }

    return {
        "country": record.country,
        "industry": record.industry,
        "regulation": record.regulation,
        "description": record.description
    }