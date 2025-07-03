from pathlib import Path
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR: Path = Path(__file__).resolve().parents[2]
SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{BASE_DIR}/portfolio.db"

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
