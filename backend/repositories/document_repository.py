from sqlalchemy.orm import Session

from models.document import Document


class DocumentRepository:

    @staticmethod
    def create(db: Session, document):

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(Document)
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    @staticmethod
    def delete(db: Session, document_id: str):

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return False

        db.delete(document)

        db.commit()

        return True