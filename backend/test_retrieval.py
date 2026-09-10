from database.database import SessionLocal
from services.retrieval_engine import get_all_acts
from services.industry_reasoner import find_applicable_acts


db = SessionLocal()

acts = get_all_acts("India", db)

print("\nAvailable Acts:")
print(acts)

result = find_applicable_acts(
    "India",
    "Healthcare",
    acts
)

print("\nApplicable Acts:")
print(result)

db.close()