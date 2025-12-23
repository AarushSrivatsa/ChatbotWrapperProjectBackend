from pydantic import BaseModel, EmailStr, Field

class UserRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters"
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class ConvoCreate(BaseModel):
    title: str = "New Chat"

class ConvoResponse(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str | None

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

class ChatRequest(BaseModel):
    message: str

class AddDocumentRequest(BaseModel):
    text: str