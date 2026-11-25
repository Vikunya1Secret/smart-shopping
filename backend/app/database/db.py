from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Базовый класс для всех таблиц."""


def get_db():
    """Выдаёт сессию БД для одного запроса и закрывает её после ответа."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Создаёт таблицы, если их ещё нет."""
    from backend.app.database import models  # noqa: F401

    Base.metadata.create_all(bind=engine)