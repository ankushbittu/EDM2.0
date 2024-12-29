import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API Configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_BASE_URL = "https://api.spotify.com/v1"

def get_spotify_auth_url() -> str:
    """
    Generate the Spotify authorization URL for OAuth.
    """
    url = (
        f"https://accounts.spotify.com/authorize?"
        f"client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope=playlist-modify-private"
    )
    print(f"Generated Spotify Auth URL: {url}")  # Debugging line
    return url

def exchange_code_for_tokens(code: str) -> dict:
    """
    Exchange the authorization code for Spotify access and refresh tokens.
    """
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    
    # Debugging: Log Spotify's response if token exchange fails
    print("Failed to exchange code for tokens:", response.json())
    raise Exception("Failed to exchange Spotify code for tokens")

def save_spotify_tokens(db, user, tokens: dict):
    """
    Save Spotify access and refresh tokens and user ID to the database.
    """
    user.spotify_token = tokens.get("access_token")
    user.spotify_refresh = tokens.get("refresh_token")

    # Fetch user_id from Spotify /me endpoint
    headers = {"Authorization": f"Bearer {user.spotify_token}"}
    response = requests.get(f"{SPOTIFY_BASE_URL}/me", headers=headers)
    if response.status_code == 200:
        user.spotify_user_id = response.json().get("id")
    else:
        raise Exception("Failed to fetch Spotify user ID")

    db.commit()

def validate_spotify_token(access_token: str) -> bool:
    """
    Validate a Spotify access token by making a test API call.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{SPOTIFY_BASE_URL}/me"
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def refresh_spotify_token(refresh_token: str) -> str:
    """
    Refresh the Spotify access token using the refresh token.
    """
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    
    # Debugging: Log response if refreshing tokens fails
    print("Failed to refresh Spotify token:", response.json())
    raise Exception("Failed to refresh Spotify token")

import re

def clean_text(text: str) -> str:
    """
    Remove unnecessary characters like asterisks or extra spaces from text.
    """
    return re.sub(r"[\*\"]", "", text).strip()

def search_song_on_spotify(access_token: str, title: str, artist: str) -> str:
    """
    Search for a song on Spotify and return its URI.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    # Clean the title and artist
    clean_title = clean_text(title)
    clean_artist = clean_text(artist)

    query = f"track:{clean_title} artist:{clean_artist}"
    url = f"{SPOTIFY_BASE_URL}/search?q={query}&type=track&limit=1"
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("items", [])
        if tracks:
            return tracks[0]["uri"]
    
    logging.warning(f"Failed to find song: {title} by {artist}, Response: {response.json()}")
    return None


def generate_and_create_playlist(access_token: str, user_id: str, songs: list[dict], playlist_name: str):
    """
    Create a Spotify playlist and add songs to it.
    """
    logging.info(f"Creating playlist for user_id: {user_id} with access_token: {access_token[:10]}...")
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"name": playlist_name, "public": False}
    url = f"{SPOTIFY_BASE_URL}/users/{user_id}/playlists"
    response = requests.post(url, json=payload, headers=headers)
    logging.info(f"Playlist creation response: {response.status_code} {response.json()}")

    if response.status_code != 201:
        raise Exception(f"Failed to create playlist: {response.json()}")
    
    playlist_id = response.json()["id"]
    song_uris = []

    for song in songs:
        uri = search_song_on_spotify(access_token, song["title"], song["artist"])
        if uri:
            song_uris.append(uri)
    add_url = f"{SPOTIFY_BASE_URL}/playlists/{playlist_id}/tracks"
    requests.post(add_url, json={"uris": song_uris}, headers=headers)

    return f"https://open.spotify.com/playlist/{playlist_id}"

