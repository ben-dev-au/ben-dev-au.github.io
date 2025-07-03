from sqlalchemy.orm.session import Session
from backend.app.database import SessionLocal


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
