# SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

# Database models
from database.initializations import ConvoModel, MessageModel

async def get_conversation_messages(db: AsyncSession, conversation_id: UUID, user_id: UUID):

    convo_result = await db.execute(
        select(ConvoModel).where(
            ConvoModel.id == conversation_id,
            ConvoModel.user_id == user_id
        )
    )
    convo = convo_result.scalar_one_or_none()
    
    if not convo:
        return None

    messages_result = await db.execute(
        select(MessageModel)
        .where(MessageModel.conversation_id == conversation_id)
        .order_by(MessageModel.created_at.asc())
    )
    messages = messages_result.scalars().all()
    
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": str(msg.created_at)
        }
        for msg in messages
    ]

async def get_recent_messages(db: AsyncSession, conversation_id: UUID, limit: int = 20):
    """Get recent messages for chat context"""
    result = await db.execute(
        select(MessageModel)
        .where(MessageModel.conversation_id == conversation_id)
        .order_by(MessageModel.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    return list(reversed(messages))

async def save_chat_messages(db: AsyncSession, conversation_id: UUID, user_message: str, ai_response: str):
    """Save both user and AI messages"""
    user_msg = MessageModel(
        conversation_id=conversation_id,
        role="user",
        content=user_message,
    )
    
    ai_msg = MessageModel(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response,
    )
    
    db.add(user_msg)
    db.add(ai_msg)
    await db.commit()
    await db.refresh(ai_msg)
    
    return {
        "id": ai_msg.id,
        "role": ai_msg.role,
        "content": ai_msg.content,
        "created_at": str(ai_msg.created_at)
    }

async def verify_conversation_access(db: AsyncSession, conversation_id: UUID, user_id: UUID):
    """Check if conversation exists and belongs to user"""
    result = await db.execute(
        select(ConvoModel).where(
            ConvoModel.id == conversation_id,
            ConvoModel.user_id == user_id
        )
    )
    return result.scalar_one_or_none()

