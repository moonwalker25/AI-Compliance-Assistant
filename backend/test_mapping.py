from database.database import SessionLocal

from services.mapping_service import (
    save_mapping,
    get_mapping
)

db = SessionLocal()

save_mapping(
    "India",
    "Healthcare",
    [
        "GST ACT",
        "DPDP ACT",
        "COMPANIES ACT"
    ],
    db
)

print(
    get_mapping(
        "India",
        "Healthcare",
        db
    )
)

db.close()