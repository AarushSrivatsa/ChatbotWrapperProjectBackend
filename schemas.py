from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class SendOTPRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters"
    )
class VerifyOTPRequest(BaseModel):
    otp: str = Field(..., min_length=6, max_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=128)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class ConvoCreate(BaseModel):
    title: str = "New Chat"

class ConvoResponse(BaseModel):
    id: UUID
    title: str
    created_at: str
    updated_at: str | None

class DeleteConvoResponse(BaseModel):
    result : str

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: str

class ChatRequest(BaseModel):
    message: str

class PostDocumentResponse(BaseModel):
    text: str