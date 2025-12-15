from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import ConvoCreate, ConvoResponse, AddDocumentRequest

from database.initializations import get_db, ConvoModel
from database.conversations import create_conversation, get_user_conversations, delete_conversation_with_cleanup

from routers.auth import get_current_user

from AI.rag import clear_rag, add_to_rag

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

@router.post("/{conversation_id}/add-document")
async def add_document_to_rag(
    conversation_id: int,
    doc_request: AddDocumentRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(
        select(ConvoModel).where(
            ConvoModel.id == conversation_id,
            ConvoModel.user_id == current_user.id
        )
    )
    convo = result.scalar_one_or_none()
    
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        rag_result = add_to_rag(conversation_id, doc_request.text)
        return {
            "message": "Document added successfully",
            "details": rag_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add document: {str(e)}")

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
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
    
    return result