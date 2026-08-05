from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):

    id: str

    filename: str

    file_type: str

    file_size: int

    status: str

    uploaded_at: datetime

    class Config:

        from_attributes = True
