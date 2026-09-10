from database.database import engine
from models.compliance import Base

Base.metadata.create_all(bind=engine)

print("Database Created Successfully!")