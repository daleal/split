from typing import Generator

from sqlalchemy.orm import Session

from split.database import SessionLocal


def get_db() -> Generator[Session, Session, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
