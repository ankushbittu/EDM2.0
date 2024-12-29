from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.orm import relationship
from app.models.emotion import Emotion
from app.models.playlist import Playlist
from app.dependencies.db import Base
import uuid
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    spotify_user_id = Column(String, unique=True, nullable=True)
    spotify_token = Column(String, nullable=True)
    spotify_refresh = Column(String, nullable=True)
    spotify_expiry = Column(DateTime, nullable=True)
    emotions = relationship("Emotion", back_populates="user", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")

