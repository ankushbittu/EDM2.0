from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.dependencies.db import Base
import uuid

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    spotify_id = Column(String, nullable=False)
    spotify_url = Column(String, nullable=False)  # Add this column for the Spotify link
    created_at = Column(DateTime, nullable=False)

    # Define the relationship with User
    user = relationship("User", back_populates="playlists")
