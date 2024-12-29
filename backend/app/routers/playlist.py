from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.services.playlist_service import save_playlist, get_user_playlists, delete_playlist, shuffle_playlist
from app.dependencies.auth import get_current_user


router = APIRouter()

@router.post("/save")
def save_new_playlist(
    title: str,
    spotify_id: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)  # Authentication dependency
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Call the service to save the playlist
    playlist = save_playlist(db, user, title, spotify_id)
    return {"message": "Playlist saved successfully", "playlist": playlist}
@router.get("/")
def fetch_user_playlists(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Fetch all playlists for the logged-in user."""
    try:
        playlists = get_user_playlists(db, user)
        return playlists
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{playlist_id}")
def delete_user_playlist(playlist_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Delete a user's playlist from the database."""
    try:
        result = delete_playlist(db, user, playlist_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{playlist_id}/shuffle")
def shuffle_user_playlist(playlist_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """Shuffle a user's playlist."""
    try:
        result = shuffle_playlist(db, user, playlist_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

