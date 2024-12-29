from sqlalchemy.orm import Session
from app.models.playlist import Playlist
from app.models.user import User
from datetime import datetime

def save_playlist(db: Session, user_id: str, playlist_name: str, spotify_id: str, spotify_url: str):
    """
    Save the playlist metadata to the database.
    """
    new_playlist = Playlist(
        user_id=user_id,
        title=playlist_name,
        spotify_id=spotify_id,
        spotify_url=spotify_url,
        created_at=datetime.utcnow()
    )
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist

def get_user_playlists(db: Session, user: User):
    """Retrieve all playlists for a specific user."""
    return db.query(Playlist).filter(Playlist.user_id == user.id).all()

def delete_playlist(db: Session, user: User, playlist_id: str):
    """Delete a playlist from the database."""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.user_id == user.id).first()
    if not playlist:
        raise Exception("Playlist not found or access denied")
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted successfully"}

def shuffle_playlist(db: Session, user: User, playlist_id: str):
    """Shuffle songs in a playlist locally (logic can be extended to interact with Spotify)."""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id, Playlist.user_id == user.id).first()
    if not playlist:
        raise Exception("Playlist not found or access denied")
    # Logic to shuffle songs (depends on actual song storage structure)
    # Placeholder return for now
    return {"message": "Playlist shuffled successfully"}
