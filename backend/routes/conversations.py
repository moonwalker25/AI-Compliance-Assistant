import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db

from services.conversation_storage import (
    get_recent_conversations,
    get_conversation,
    get_conversation_messages,
    delete_conversation
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


# ============================================================
# SAFE MESSAGE DATA PARSER
# ============================================================

def parse_message_data(message_data):

    # No additional data
    if message_data is None:
        return None

    # SQLAlchemy JSON column already returns dict/list
    if isinstance(message_data, (dict, list)):
        return message_data

    # Handle old records stored as JSON strings
    if isinstance(message_data, str):

        try:
            return json.loads(message_data)

        except (json.JSONDecodeError, TypeError):
            return None

    return None


# ============================================================
# LIST RECENT CONVERSATIONS
# ============================================================

@router.get("/")
def list_conversations(
    db: Session = Depends(get_db)
):

    conversations = get_recent_conversations(db)

    return [
        {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at
        }
        for conversation in conversations
    ]


# ============================================================
# GET SINGLE CONVERSATION
# ============================================================

@router.get("/{session_id}")
def get_single_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):

    conversation = get_conversation(
        session_id,
        db
    )

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = get_conversation_messages(
        session_id,
        db
    )

    formatted_messages = []

    for message in messages:

        formatted_messages.append(
            {
                "id": message.id,
                "sender": message.sender,
                "message": message.message,

                # Important: preserve button/options data
                "message_data": parse_message_data(
                    message.message_data
                ),

                "created_at": message.created_at
            }
        )

    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": formatted_messages
    }


# ============================================================
# DELETE CONVERSATION
# ============================================================

@router.delete("/{session_id}")
def remove_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):

    deleted = delete_conversation(
        session_id,
        db
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return {
        "message": "Conversation deleted successfully"
    }