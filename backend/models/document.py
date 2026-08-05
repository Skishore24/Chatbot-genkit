from datetime import datetime
import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from database.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    filename = Column(
        String(255),
        nullable=False
    )

    file_type = Column(
        String(50),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    file_size = Column(
        Integer,
        default=0
    )

    chunk_count = Column(
        Integer,
        default=0
    )

    status = Column(
        String(50),
        default="Indexed"
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )