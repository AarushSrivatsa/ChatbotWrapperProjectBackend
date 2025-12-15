from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import MessageResponse, ChatRequest

from database.initializations import get_db
from database.messages import get_conversation_messages, get_recent_messages, save_chat_messages, verify_conversation_access

from routers.auth import get_current_user

from AI.bot import get_ai_response

router = APIRouter(prefix="/convo/{conversation_id}/messages", tags=["messages"])
message_limit = 25 

@router.get("/", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    messages = await get_conversation_messages(db, conversation_id, current_user.id)
    
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return messages

@router.post("/", response_model=MessageResponse)
async def post_message(
    conversation_id: int,
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    
    convo = await verify_conversation_access(db, conversation_id, current_user.id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = await get_recent_messages(db, conversation_id, limit=20)

    ai_response = await get_ai_response(
        user_message=chat_request.message,
        conversation_id=conversation_id,
        messages=messages
    )
    
    return await save_chat_messages(db, conversation_id, chat_request.message, ai_response)
    









