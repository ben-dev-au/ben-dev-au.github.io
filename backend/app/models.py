# from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base


# class Project(Base):
#     __tablename__ = "projects"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(Text)
#     link = Column(String)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # created_at = Column(String, default=lambda: datetime.now(datetime.timezone.utc))


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"extend_existing": True}  # Allow table redefinition

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=False)  # Path to the project image
    link = Column(String(255), nullable=True)  # Optional link to the project
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # created_at = Column(DateTime, default=datetime.now(timezone.utc))
