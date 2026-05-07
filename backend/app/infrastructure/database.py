from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


engine = create_engine(
    settings.databaseUrl,
    echo=settings.debug,        # loga SQLs no terminal se estiver em debug
    pool_pre_ping=True,         # verifica conexão antes de usar
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependência do FastAPI — fornece sessão do banco
    e garante fechamento ao final da requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()