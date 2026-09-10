from database.database import SessionLocal
from models.compliance import Compliance

db = SessionLocal()

data = [
    Compliance(
        country="India",
        industry="Healthcare",
        regulation="HIPAA Equivalent",
        description="Patient medical records must remain confidential."
    ),

    Compliance(
        country="India",
        industry="Finance",
        regulation="RBI Data Security",
        description="Financial data should be encrypted."
    ),

    Compliance(
        country="USA",
        industry="Healthcare",
        regulation="HIPAA",
        description="Protect patient health information."
    ),

    Compliance(
        country="Germany",
        industry="Manufacturing",
        regulation="GDPR",
        description="Personal data must be protected."
    )
]

db.add_all(data)
db.commit()

print("Dummy Data Added Successfully!")