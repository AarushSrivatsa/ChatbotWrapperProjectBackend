
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import MessageResponse, ChatRequest, PostDocumentResponse

from database.initializations import get_db, ConvoModel, AsyncSessionLocal
from database.messages import get_conversation_messages, get_recent_messages, save_chat_messages, verify_conversation_access

from utils.auth import get_current_user

from AI.bot import get_ai_response
from AI.rag import add_to_rag

router = APIRouter(prefix="/conversations/{conversation_id}/messages", tags=["messages"])
message_limit = 25 

@router.get("/", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    messages = await get_conversation_messages(db, conversation_id, current_user.id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages

@router.post("/", response_model=MessageResponse)
async def post_message(
    conversation_id: UUID,
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

@router.post("/document",response_model=PostDocumentResponse)
async def post_document(
    conversation_id: UUID,
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(ConvoModel).where(
                ConvoModel.id == conversation_id,
                ConvoModel.user_id == current_user.id
            )
        )
        convo = result.scalar_one_or_none()
        if not convo:
            raise HTTPException(status_code=404, detail="Conversation not found")
    file_bytes = await file.read()

    try:
        rag_result = await run_in_threadpool(
            add_to_rag,         
            conversation_id,
            file_bytes,
            file.filename
        )
        return {
            "message": "Document added successfully",
            "filename": file.filename,
            "details": rag_result
        }
    except Exception as e:
        print("RAG ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to add document"
        )


