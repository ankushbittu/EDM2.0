from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.services.llm_service import generate_playlist_from_prompt
from app.services.spotify_service import generate_and_create_playlist
from app.services.playlist_service import save_playlist
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/generate")
def generate_playlist(prompt: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """
    Generate a playlist based on user input prompt.
    """
    try:
        # Step 1: Generate song list from LLM
        songs = generate_playlist_from_prompt(prompt)

        # Step 2: Create Spotify playlist
        playlist_url = generate_and_create_playlist(user.spotify_token, user.spotify_user_id, songs, "Generated Playlist")

        # Step 3: Save playlist to database
        # Step 3: Save playlist to database
        playlist_id = playlist_url.split("/")[-1]  # Extract Spotify playlist ID
        save_playlist(
            db=db,
            user_id=user.id,
            playlist_name="Generated Playlist",
            spotify_id=playlist_id,
            spotify_url=playlist_url
        )
        
        return {"playlist_url": playlist_url, "songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
