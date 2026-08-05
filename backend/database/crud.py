from typing import List, Optional
from sqlalchemy.orm import Session

from database.models import User, ChatSession, ChatMessage, Document
from utils.security import hash_password


# User Operations
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session) -> List[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


def create_user(db: Session, user) -> User:
    # Set first user as admin automatically
    user_count = db.query(User).count()
    is_admin = True if user_count == 0 else getattr(user, "is_admin", False)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        is_admin=is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Chat Session Operations
def create_chat_session(db: Session, user_id: int, title: str = "New Chat") -> ChatSession:
    session = ChatSession(user_id=user_id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_user_sessions(db: Session, user_id: int) -> List[ChatSession]:
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )


def get_chat_session(db: Session, session_id: str) -> Optional[ChatSession]:
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()


def delete_chat_session(db: Session, session_id: str) -> bool:
    session = get_chat_session(db, session_id)
    if session:
        db.delete(session)
        db.commit()
        return True
    return False


# Chat Message Operations
def add_chat_message(
    db: Session,
    session_id: str,
    sender: str,
    content: str,
    context_used: Optional[str] = None,
    token_count: int = 0,
) -> ChatMessage:
    msg = ChatMessage(
        session_id=session_id,
        sender=sender,
        content=content,
        context_used=context_used,
        token_count=token_count,
    )
    db.add(msg)
    
    # Touch updated_at on session
    session = get_chat_session(db, session_id)
    if session:
        # Update session title from first user message if default
        if session.title == "New Chat" and sender == "user":
            session.title = content[:30] + ("..." if len(content) > 30 else "")
    
    db.commit()
    db.refresh(msg)
    return msg


def get_session_messages(db: Session, session_id: str) -> List[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


# Document Operations
def create_document(
    db: Session,
    filename: str,
    file_type: str,
    file_path: str,
    file_size: int,
    chunk_count: int,
    status: str = "Indexed",
) -> Document:
    doc = Document(
        filename=filename,
        file_type=file_type,
        file_path=file_path,
        file_size=file_size,
        chunk_count=chunk_count,
        status=status,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_all_documents(db: Session) -> List[Document]:
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


def delete_document(db: Session, doc_id: str) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False