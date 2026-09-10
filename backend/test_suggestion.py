from database.database import SessionLocal

from services.suggestion_service import save_suggestion

db = SessionLocal()

verification = {

    "applicable": True,

    "confidence": 94,

    "reason": "Factories Act governs workplace safety."
}

result = save_suggestion(

    "India",

    "Healthcare",

    "FACTORIES ACT",

    verification,

    db
)

print(result.id)

print(result.status)

db.close()