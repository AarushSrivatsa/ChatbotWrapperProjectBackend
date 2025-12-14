from fastapi import APIRouter, Depends, HTTPException
from schemas import MessageResponse, ChatRequest
from routers.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from database.operations import get_db
from sqlalchemy import select
from database.models import ConvoModel, MessageModel
from langchain_core.messages import AIMessage, HumanMessage
from AI.bot import get_ai_response
from AI.rag import add_to_rag

router = APIRouter(prefix="/convo/{conversation_id}/messages", tags=["messages"])
message_limit = 25 

@router.get("/", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if conversation exists and belongs to current user
    convo_result = await db.execute(
        select(ConvoModel).where(
            ConvoModel.id == conversation_id,
            ConvoModel.user_id == current_user.id
        )
    )
    convo = convo_result.scalar_one_or_none()
    
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get all messages for this conversation
    messages_result = await db.execute(
        select(MessageModel)
        .where(MessageModel.conversation_id == conversation_id)
        .order_by(MessageModel.created_at.asc())
    )
    messages = messages_result.scalars().all()
    
    # Return messages
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": str(msg.created_at)
        }
        for msg in messages
    ]

@router.post("/", response_model=MessageResponse)
async def post_message(
    conversation_id: int,
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Check if conversation exists and belongs to user
    convo = (
        await db.execute(
            select(ConvoModel).where(
                ConvoModel.id == conversation_id,
                ConvoModel.user_id == current_user.id
            )
        )
    ).scalar_one_or_none()
    
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get recent message history (last 20 messages)
    message_limit = 20
    result = await db.execute(
        select(MessageModel)
        .where(MessageModel.conversation_id == conversation_id)
        .order_by(MessageModel.created_at.desc())
        .limit(message_limit)
    )
    messages = result.scalars().all()
    messages.reverse()  # oldest → newest
    
    # Format chat history for LangChain
    chat_history = []
    for message in messages:
        if message.role == "assistant":
            chat_history.append(AIMessage(content=message.content))
        elif message.role == "user":
            chat_history.append(HumanMessage(content=message.content))
    
    # Get AI response
    ai_response = await get_ai_response(
        user_message=chat_request.message,
        conversation_id=conversation_id,
        chat_history=chat_history
    )
    
    # Save user message
    user_msg = MessageModel(
        conversation_id=conversation_id,
        role="user",
        content=chat_request.message,
    )
    
    # Save AI message
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

    









