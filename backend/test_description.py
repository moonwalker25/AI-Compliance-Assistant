from database.database import SessionLocal
from services.retrieval_engine import get_description

db = SessionLocal()

result = get_description(
    "FORM 11",
    db
)

print(result)

db.close()