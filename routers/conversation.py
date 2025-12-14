from fastapi import APIRouter, Depends, HTTPException
from schemas import ConvoCreate, ConvoResponse, AddDocumentRequest
from database.operations import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_user
from database.models import ConvoModel
from sqlalchemy import select
from sqlalchemy import delete
from database.models import MessageModel
from AI.rag import clear_rag, add_to_rag

router = APIRouter(prefix='/conversations',tags=['conversations'])

@router.post("/", response_model=ConvoResponse)
async def create_convo(
    convo_data: ConvoCreate, 
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_convo = ConvoModel(
        user_id=current_user.id,
        title=convo_data.title
    )
    db.add(new_convo)
    await db.commit()
    await db.refresh(new_convo)
    
    return {
        "id": new_convo.id,
        "title": new_convo.title,
        "created_at": str(new_convo.created_at),
        "updated_at": str(new_convo.updated_at) if new_convo.updated_at else None
    }

@router.get("/", response_model=list[ConvoResponse])
async def list_conversations(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConvoModel)
        .where(ConvoModel.user_id == current_user.id)
        .order_by(ConvoModel.updated_at.desc())
    )
    convos = result.scalars().all()
    
    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": str(c.created_at),
            "updated_at": str(c.updated_at) if c.updated_at else None
        }
        for c in convos
    ]

@router.post("/{conversation_id}/add-document")
async def add_document_to_rag(
    conversation_id: int,
    doc_request: AddDocumentRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify conversation exists and belongs to user
    result = await db.execute(
        select(ConvoModel).where(
            ConvoModel.id == conversation_id,
            ConvoModel.user_id == current_user.id
        )
    )
    convo = result.scalar_one_or_none()
    
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Add document text to RAG
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
    result = await db.execute(
        select(ConvoModel)
        .where(ConvoModel.id == conversation_id, ConvoModel.user_id == current_user.id)
    )
    convo = result.scalar_one_or_none()
    
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    await db.execute(
        delete(MessageModel).where(MessageModel.conversation_id == conversation_id)
    )
    
    await db.delete(convo)
    await db.commit()

    try:
        clear_rag(conversation_id)
    except Exception as e:
        # Log but don't fail if RAG cleanup fails
        print(f"Warning: Failed to clear RAG for conversation {conversation_id}: {e}")
    
    return {"message": "Conversation deleted"}
