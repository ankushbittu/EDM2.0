from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, spotify, llm, emotion, playlist,user
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Initialize FastAPI app
app = FastAPI(title="PlaylistAI API", description="API for managing playlists, Spotify integration, and emotions")

# Middleware: CORS (Allow frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(spotify.router, prefix="/spotify", tags=["Spotify"])
app.include_router(user.router, prefix="/user", tags=["User Profile"])
app.include_router(llm.router, prefix="/llm", tags=["LLM"])
app.include_router(emotion.router, prefix="/emotion", tags=["Emotion-Based Playlists"])
app.include_router(playlist.router, prefix="/playlist", tags=["Playlist Management"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the PlaylistAI API. Visit /docs for API documentation."}
