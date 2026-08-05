from pydantic import BaseModel


class CreateChat(BaseModel):
    user_id: int
    title: str = "New Chat"


class SendMessage(BaseModel):
    session_id: str
    sender: str
    content: str


class RenameChat(BaseModel):
    chat_id: str
    title: str