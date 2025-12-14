from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from database.models import UserModel
from database.operations import get_db
from routers.auth import hash_password, verify_password, create_access_token
from schemas import UserRequest, Token

router = APIRouter(prefix="/users", tags=["users"])

@router.post('/register',response_model=Token)
async def register(user_request: UserRequest, db: AsyncSession = Depends(get_db)):

    # fetching from db
    result = await db.execute(select(UserModel).where(UserModel.email == user_request.email))
    existing_user = result.scalar_one_or_none()

    # if already signed up, we give an err
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # hashing password and creating user object
    hash_pw = hash_password(user_request.password)
    new_user = UserModel(email=user_request.email,hashed_password=hash_pw)

    # inserting into db
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # creating access token
    token = create_access_token({"sub": str(new_user.id) })
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # querying db
    result = await db.execute(select(UserModel).where(UserModel.email == user_data.email))
    user = result.scalar_one_or_none()
    
    # if no user we throw err
    if not user or not verify_password(hashed_password=user.hashed_password, plain_password=user_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # creating access tokens if valid
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
    



