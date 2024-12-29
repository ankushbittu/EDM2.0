
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.dependencies.db import Base
import uuid

class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    emotion = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    # Define the relationship with User
    user = relationship("User", back_populates="emotions")
