# SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Database models
from database.initializations import UserModel

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, email: str, hashed_password: str):
    new_user = UserModel(email=email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user