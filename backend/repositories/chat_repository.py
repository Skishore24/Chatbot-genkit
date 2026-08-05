from sqlalchemy.orm import Session

from models.chat import ChatSession, ChatMessage


class ChatRepository:

    @staticmethod
    def create_chat(db: Session, user_id: int, title: str = "New Chat"):

        chat = ChatSession(user_id=user_id, title=title)

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat

    @staticmethod
    def get_user_chats(db: Session, user_id: int):

        return (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.updated_at.desc())
            .all()
        )

    @staticmethod
    def get_chat(db: Session, chat_id: str):

        return db.query(ChatSession).filter(ChatSession.id == chat_id).first()

    @staticmethod
    def delete_chat(db: Session, chat_id: str):

        chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()

        if not chat:
            return False

        db.delete(chat)
        db.commit()

        return True

    @staticmethod
    def rename_chat(db: Session, chat_id: str, title: str):

        chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()

        if not chat:
            return None

        chat.title = title

        db.commit()
        db.refresh(chat)

        return chat

    @staticmethod
    def add_message(
        db: Session,
        session_id: str,
        sender: str,
        content: str,
        context_used: str = "",
        token_count: int = 0,
    ):

        message = ChatMessage(
            session_id=session_id,
            sender=sender,
            content=content,
            context_used=context_used,
            token_count=token_count,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_messages(db: Session, session_id: str):

        return (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    @staticmethod
    def clear_chat(db: Session, session_id: str):

        (db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete())

        db.commit()
