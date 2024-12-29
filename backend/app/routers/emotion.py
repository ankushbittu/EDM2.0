
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.services.emotion_service import detect_emotion
from app.services.llm_service import  generate_playlist_from_prompt
from app.services.spotify_service import generate_and_create_playlist
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/capture")
def capture_emotion(file: UploadFile = File(...), artist: str = "", language: str = "", db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """
    Capture emotion, generate playlist, and save it.
    """
    try:
        # Step 1: Detect emotion
        emotion = detect_emotion(file.file.read())

        # Step 2: Generate songs from emotion
        prompt = f"Create a {emotion} playlist with songs by {artist} in {language}."
        songs = generate_playlist_from_prompt(prompt)

        # Step 3: Create Spotify playlist
        playlist_url = generate_and_create_playlist(user.spotify_token, user.spotify_user_id, songs, f"{emotion} Playlist")

        return {"playlist_url": playlist_url, "emotion": emotion, "songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

