# Database models
from database.initializations import ConvoModel, MessageModel

# SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

async def create_conversation(db: AsyncSession, user_id: UUID, title: str):

    new_convo = ConvoModel(user_id=user_id, title=title)
    db.add(new_convo)
    await db.commit()
    await db.refresh(new_convo)
    
    return {
        "id": new_convo.id,
        "title": new_convo.title,
        "created_at": str(new_convo.created_at),
        "updated_at": str(new_convo.updated_at) if new_convo.updated_at else None
    }

async def get_user_conversations(db: AsyncSession, user_id: UUID):
    result = await db.execute(
        select(ConvoModel)
        .where(ConvoModel.user_id == user_id)
        .order_by(ConvoModel.created_at.desc())
    )
    convos = result.scalars().all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": str(c.created_at),
            "updated_at": str(c.updated_at) if c.updated_at else None
        }
        for c in convos
    ]

async def delete_conversation_with_cleanup(db: AsyncSession, conversation_id: int, user_id: UUID):

    result = await db.execute(
        select(ConvoModel).where(
            ConvoModel.id == conversation_id,
            ConvoModel.user_id == user_id
        )
    )
    convo = result.scalar_one_or_none()
    if not convo:
        return None
    await db.execute(
        delete(MessageModel).where(MessageModel.conversation_id == conversation_id)
    )
    await db.delete(convo)
    await db.commit()
    return {"message": "Conversation deleted"}