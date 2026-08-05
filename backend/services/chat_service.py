from sqlalchemy.orm import Session

from repositories.chat_repository import ChatRepository
from services.rag_service import RAGService


class ChatService:

    @staticmethod
    def create_chat(db: Session, user_id: int, title: str):

        return ChatRepository.create_chat(db, user_id, title)

    @staticmethod
    def send_message(db: Session, session_id: str, message: str):

        # Save User Message
        ChatRepository.save_message(db, session_id, "user", message)

        # Temporary AI Response
        ai_response = (
            "Hello! I'm GenKit AI. "
            "The RAG engine will be connected in the next phase."
        )

        # Save AI Message
        ChatRepository.save_message(db, session_id, "assistant", ai_response)

        return ai_response
