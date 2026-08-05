from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from database.database import engine, Base
from api.auth.auth import router as auth_router
from api.chat.chat import router as chat_router
from api.documents.routes import router as documents_router
import models.user
import models.chat
import models.document

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(documents_router)


@app.get("/")
def home():
    return {
        "message": "GenKit AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "database": "Connected",
        "status": "Healthy"
    }