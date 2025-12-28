# FastAPI
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
# Database
from sqlalchemy.ext.asyncio import AsyncSession
from database.initializations import get_db
from database.conversations import create_conversation, get_user_conversations, delete_conversation_with_cleanup

# Schemas
from schemas import ConvoCreate, ConvoResponse, DeleteConvoResponse

# Auth & AI
from routers.auth import get_current_user
from AI.rag import clear_rag

router = APIRouter(prefix='/conversations',tags=['conversations'])

@router.post("/", response_model=ConvoResponse)
async def create_convo(
    convo_data: ConvoCreate, 
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await create_conversation(db, current_user.id, convo_data.title)

@router.get("/", response_model=list[ConvoResponse])
async def list_conversations(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_user_conversations(db, current_user.id)

@router.delete("/{conversation_id}",response_model=DeleteConvoResponse)
async def delete_conversation(
    conversation_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await delete_conversation_with_cleanup(db, conversation_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    try:
        clear_rag(conversation_id)
    except Exception as e:
        print(f"Warning: Failed to clear RAG for conversation {conversation_id}: {e}")
    return {"result":result}