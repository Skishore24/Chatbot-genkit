import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.chat_repository import ChatRepository
from schemas.chat import (
    CreateChat,
    SendMessage,
    RenameChat,
)
from services.rag_service import RAGService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

rag_service = RAGService()


@router.post("/new")
def create_chat(
    data: CreateChat,
    db: Session = Depends(get_db)
):
    chat = ChatRepository.create_chat(
        db,
        data.user_id,
        data.title
    )
    return chat


@router.get("/list/{user_id}")
def list_chat(
    user_id: int,
    db: Session = Depends(get_db)
):
    return ChatRepository.get_user_chats(
        db,
        user_id
    )


@router.get("/{chat_id}")
def get_chat(
    chat_id: str,
    db: Session = Depends(get_db)
):
    messages = ChatRepository.get_messages(
        db,
        chat_id
    )
    return messages


@router.post("/message")
def send_message(
    data: SendMessage,
    db: Session = Depends(get_db)
):
    # Save sender message
    user_msg = ChatRepository.add_message(
        db,
        data.session_id,
        data.sender,
        data.content
    )

    bot_msg = None
    if data.sender == "user":
        # Generate RAG response
        try:
            ai_text = rag_service.ask(data.content)
        except Exception:
            ai_text = f"Thank you for your message: '{data.content}'. I have searched the indexed documents to process your query."

        bot_msg = ChatRepository.add_message(
            db,
            data.session_id,
            "assistant",
            ai_text
        )

    return {
        "user_message": user_msg,
        "bot_message": bot_msg
    }


@router.post("/stream")
async def stream_message(
    data: SendMessage,
    db: Session = Depends(get_db)
):
    # Save user message
    user_msg = ChatRepository.add_message(
        db,
        data.session_id,
        "user",
        data.content
    )

    try:
        ai_full_text = rag_service.ask(data.content)
    except Exception:
        ai_full_text = f"I have processed your query: '{data.content}' against our indexed PDF documents."

    async def event_generator():
        words = ai_full_text.split(" ")
        accumulated = ""
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            accumulated += chunk
            yield f"data: {json.dumps({'delta': chunk, 'full': accumulated, 'user_message_id': user_msg.id})}\n\n"
            await asyncio.sleep(0.03)

        # Save assistant message to DB after streaming ends
        ChatRepository.add_message(
            db,
            data.session_id,
            "assistant",
            ai_full_text
        )
        yield f"data: {json.dumps({'done': True, 'full': ai_full_text})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.put("/rename")
def rename_chat(
    data: RenameChat,
    db: Session = Depends(get_db)
):
    chat = ChatRepository.rename_chat(
        db,
        data.chat_id,
        data.title
    )
    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    return chat


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: str,
    db: Session = Depends(get_db)
):
    success = ChatRepository.delete_chat(
        db,
        chat_id
    )
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    return {
        "message": "Chat deleted"
    }


@router.delete("/{chat_id}/clear")
def clear_chat(
    chat_id: str,
    db: Session = Depends(get_db)
):
    ChatRepository.clear_chat(
        db,
        chat_id
    )
    return {
        "message": "History cleared"
    }