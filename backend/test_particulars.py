from database.database import SessionLocal
from services.retrieval_engine import get_particulars

db = SessionLocal()

result = get_particulars(
    "COMPANIES ACT",
    db
)

print(result)

db.close()