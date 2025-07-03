from sqlalchemy import Column, Integer, String, Text, DateTime, func
from backend.app.database import Base


class Project(Base):
    __tablename__: str = "projects"
    __table_args__: dict[str, bool] = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=False)
    link = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
