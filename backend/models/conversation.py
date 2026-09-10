from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON
)

from sqlalchemy.orm import relationship

from models.compliance import Base


# ============================================================
# CONVERSATION
# ============================================================

class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        String,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False,
        default="New Conversation"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    messages = relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


# ============================================================
# CONVERSATION MESSAGE
# ============================================================

class ConversationMessage(Base):

    __tablename__ = "conversation_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True
    )

    sender = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    # Stores structured UI data such as:
    # industries, applicable_acts, particulars, next_step, etc.
    message_data = Column(
        JSON,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )