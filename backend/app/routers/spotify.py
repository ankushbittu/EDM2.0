from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.spotify_service import get_spotify_auth_url, exchange_code_for_tokens, save_spotify_tokens
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/connect")
def connect_to_spotify():
    return {"url": get_spotify_auth_url()}

@router.get("/callback")
def spotify_callback(code: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        tokens = exchange_code_for_tokens(code)
        save_spotify_tokens(db, user, tokens)
        return {"message": "Spotify connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
