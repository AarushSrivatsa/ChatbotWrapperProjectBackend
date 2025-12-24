# FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Database
from sqlalchemy.ext.asyncio import AsyncSession
from database.initializations import get_db
from database.user import get_user_by_email, create_user

# Schemas
from schemas import UserRequest, Token

# Auth
from routers.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post('/register', response_model=Token)
async def register(user_request: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user_request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user_request.password)
    new_user = await create_user(db, user_request.email, hashed_pw)
    return create_access_token(new_user.id)

@router.post("/login", response_model=Token)
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user.hashed_password, user_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return create_access_token(user.id)