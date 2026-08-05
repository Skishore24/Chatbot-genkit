from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class SessionCreate(BaseModel):
    title: Optional[str] = "New Chat"


class SessionResponse(BaseModel):
    id: str
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    session_id: str
    prompt: str
    use_rag: Optional[bool] = True


class MessageResponse(BaseModel):
    id: int
    session_id: str
    sender: str
    content: str
    context_used: Optional[str] = None
    token_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_path: str
    file_size: int
    chunk_count: int
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class AdminMetrics(BaseModel):
    total_users: int
    total_sessions: int
    total_messages: int
    total_documents: int
    total_chunks: int
    system_status: str