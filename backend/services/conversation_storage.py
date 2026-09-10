from datetime import datetime

from sqlalchemy.orm import Session

from models.conversation import (
    Conversation,
    ConversationMessage
)


# ============================================================
# CREATE CONVERSATION
# ============================================================

def create_conversation(
    session_id: str,
    db: Session,
    title: str = "New Conversation"
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == session_id
        )
        .first()
    )

    if conversation:
        return conversation


    conversation = Conversation(
        id=session_id,
        title=title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

#===========================================================
# GET CONVERSATION
#===========================================================

def get_conversation(
    session_id: str,
    db: Session
):

    return (
        db.query(Conversation)
        .filter(
            Conversation.id == session_id
        )
        .first()
    )

# ============================================================
# SAVE MESSAGE
# ============================================================

def save_message(
    session_id: str,
    sender: str,
    message: str,
    db: Session,
    message_data=None
):

    conversation = create_conversation(
        session_id,
        db
    )


    new_message = ConversationMessage(

        conversation_id=session_id,

        sender=sender,

        message=message,

        # Save dictionary directly into JSON column
        message_data=message_data
    )


    db.add(new_message)

    conversation.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(new_message)

    return new_message


# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

def get_conversation_messages(
    session_id: str,
    db: Session
):

    return (
        db.query(ConversationMessage)
        .filter(
            ConversationMessage.conversation_id == session_id
        )
        .order_by(
            ConversationMessage.created_at.asc()
        )
        .all()
    )


# ============================================================
# GET RECENT CONVERSATIONS
# ============================================================

def get_recent_conversations(
    db: Session,
    limit: int = 20
):

    return (
        db.query(Conversation)
        .order_by(
            Conversation.updated_at.desc()
        )
        .limit(limit)
        .all()
    )


# ============================================================
# DELETE CONVERSATION
# ============================================================

def delete_conversation(
    session_id: str,
    db: Session
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == session_id
        )
        .first()
    )

    if not conversation:
        return False


    db.delete(conversation)

    db.commit()

    return True