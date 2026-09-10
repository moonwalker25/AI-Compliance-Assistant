from database.database import SessionLocal
from models.compliance import Industry, Act, ComplianceParticular

db = SessionLocal()

print("\nIndustries")
print("=" * 40)
for industry in db.query(Industry).all():
    print(industry.id, industry.industry_name, industry.country)

print("\nActs")
print("=" * 40)
for act in db.query(Act).all():
    print(act.id, act.act_name, act.country, act.industry_id)

print("\nCompliance Particulars")
print("=" * 40)
for cp in db.query(ComplianceParticular).limit(10).all():
    print(cp.id, cp.particular)

db.close()