# FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Database
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.initializations import get_db, RefreshTokenModel
from routers.auth import get_current_user, hash_refresh_token
from database.user import get_user_by_email, create_user
from datetime import datetime, timezone

# Schemas
from schemas import UserRequest, TokenResponse, RefreshRequest

# Auth
from routers.auth import hash_password, verify_password, create_tokens

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register",response_model=TokenResponse)
async def register(user_request: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user_request.email)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user_request.password)
    new_user = await create_user(db, user_request.email, hashed_pw)
    
    return await create_tokens(new_user.id, db)  # Added await

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, user_data.email)
    
    if not user or not verify_password(user.hashed_password, user_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return await create_tokens(user.id, db)  # Already correct

@router.post("/logout")
async def logout(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.execute(
        update(RefreshTokenModel)
        .where(
            RefreshTokenModel.user_id == current_user.id,
            RefreshTokenModel.revoked == False
        )
        .values(revoked=True)
    )
    await db.commit()
    
    return {"message": "Logged out successfully"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    refresh_request: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    token_hash = hash_refresh_token(refresh_request.refresh_token)
    
    result = await db.execute(
        select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash,
            RefreshTokenModel.revoked == False,
            RefreshTokenModel.expires_at > datetime.now(tz=timezone.utc)
        )
    )
    db_token = result.scalar_one_or_none()
    
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # Revoke old token
    db_token.revoked = True
    
    # Issue new tokens
    new_tokens = await create_tokens(db_token.user_id, db)
    await db.commit()
    
    return new_tokens