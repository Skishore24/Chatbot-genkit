import logging
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

logger = logging.getLogger("GenkitChatbot.Database")

# Prepare database engine with MySQL auto-create and SQLite fallback fallback
def init_database_engine():
    password = quote_plus(settings.MYSQL_PASSWORD)
    mysql_url = (
        f"mysql+pymysql://{settings.MYSQL_USER}:{password}"
        f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
    )

    try:
        # Try connecting to MySQL host to ensure target database exists
        server_url = (
            f"mysql+pymysql://{settings.MYSQL_USER}:{password}"
            f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}"
        )
        temp_engine = create_engine(server_url, pool_pre_ping=True)
        with temp_engine.connect() as conn:
            conn.execute(
                text(f"CREATE DATABASE IF NOT EXISTS `{settings.MYSQL_DATABASE}` CHARACTER SET utf8mb4;")
            )
            conn.commit()
        temp_engine.dispose()

        # Connect to MySQL DB
        db_engine = create_engine(mysql_url, echo=False, pool_pre_ping=True)
        # Test connection
        with db_engine.connect() as conn:
            pass
        logger.info(f"✅ Connected to MySQL database '{settings.MYSQL_DATABASE}' successfully.")
        return db_engine
    except Exception as e:
        logger.warning(f"⚠️ MySQL connection failed ({e}). Falling back to SQLite database...")
        db_dir = Path(__file__).resolve().parent
        sqlite_file = db_dir / "genkit_chatbot.db"
        sqlite_url = f"sqlite:///{sqlite_file}"
        db_engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})
        logger.info(f"✅ Connected to SQLite database at '{sqlite_file}' successfully.")
        return db_engine

engine = init_database_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()