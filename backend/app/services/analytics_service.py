from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.services.analytics_service import save_emotion, get_emotion_history, get_playlist_creation_stats
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/emotion/save")
def save_emotion_route(emotion: str, playlist_id: str = None, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    save_emotion(db, user.id, emotion, playlist_id)
    return {"message": "Emotion saved successfully"}

@router.get("/emotion/history")
def emotion_history(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return get_emotion_history(db, user.id)

@router.get("/stats/playlists")
def playlist_stats(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    count = get_playlist_creation_stats(db, user.id)
    return {"playlists_created": count}
