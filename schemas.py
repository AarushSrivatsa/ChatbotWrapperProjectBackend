from pydantic import BaseModel

class UserRequest(BaseModel):
    email: str
    password: str

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
    role: str  # "user" or "assistant"
    content: str
    created_at: str

class ChatRequest(BaseModel):
    message: str

class AddDocumentRequest(BaseModel):
    text: str