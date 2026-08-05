import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.document_repository import DocumentRepository
from services.document_service import DocumentService
from services.indexing_service import IndexingService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

service = DocumentService()
indexer = IndexingService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filepath = service.save_file(file)
    document = service.create_document(
        db,
        file,
        filepath
    )
    
    # Try indexing
    try:
        chunks_count = indexer.index_document(filepath)
        document.chunk_count = chunks_count
        document.status = "Indexed"
        db.commit()
    except Exception as e:
        document.status = "Failed"
        db.commit()

    return {
        "message": "Document Uploaded",
        "document": {
            "id": document.id,
            "filename": document.filename,
            "file_size": document.file_size,
            "status": document.status,
            "uploaded_at": document.uploaded_at
        }
    }


@router.get("/list")
def list_documents(db: Session = Depends(get_db)):
    documents = DocumentRepository.get_all(db)
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "chunk_count": doc.chunk_count,
            "status": doc.status,
            "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None
        }
        for doc in documents
    ]


@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    success = DocumentRepository.delete(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


@router.post("/reindex")
def reindex_documents(db: Session = Depends(get_db)):
    documents = DocumentRepository.get_all(db)
    total_indexed = 0
    for doc in documents:
        if os.path.exists(doc.file_path):
            try:
                count = indexer.index_document(doc.file_path)
                doc.chunk_count = count
                doc.status = "Indexed"
                total_indexed += 1
            except Exception:
                doc.status = "Failed"
        else:
            doc.status = "Missing File"
    db.commit()
    return {
        "message": "Reindexing Completed",
        "documents_processed": total_indexed
    }