import os
import shutil
import uuid

from fastapi import UploadFile

from models.document import Document


class DocumentService:

    BASE_FOLDER = "uploads"

    def save_file(self, file: UploadFile):

        extension = file.filename.split(".")[-1].lower()

        folder = os.path.join(self.BASE_FOLDER, extension)

        os.makedirs(folder, exist_ok=True)

        filename = str(uuid.uuid4()) + "." + extension

        filepath = os.path.join(folder, filename)

        with open(filepath, "wb") as buffer:

            shutil.copyfileobj(file.file, buffer)

        return filepath

    def create_document(self, db, file, filepath):

        document = Document(
            filename=file.filename,
            file_type=file.filename.split(".")[-1],
            file_path=filepath,
            file_size=file.size,
            status="Uploaded",
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return document
