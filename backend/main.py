import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.compliance import router as compliance_router
from routes.chat import router as chat_router
from routes.admin import router as admin_router

# Database
from database.database import engine
from models.compliance import Base

# Import models so SQLAlchemy registers them with Base.metadata
from models.conversation import Conversation, ConversationMessage

from routes.conversations import router as conversations_router


# --------------------------------
# CREATE DATABASE TABLES
# --------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------
# FASTAPI APP
# --------------------------------

app = FastAPI(
    title="AI Compliance Assistant",
    version="1.0"
)


# --------------------------------
# CORS
# --------------------------------

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


frontend_url = os.getenv("FRONTEND_URL")

if frontend_url:
    allowed_origins.append(frontend_url)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------
# ROUTES
# --------------------------------

app.include_router(compliance_router)
app.include_router(chat_router)
app.include_router(admin_router)
app.include_router(conversations_router)


# --------------------------------
# BASIC ENDPOINTS
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Compliance Assistant Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }