import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

logging.basicConfig(level=logging.INFO)

def generate_playlist_from_prompt(prompt: str) -> list[dict]:
    """
    Generate a playlist from a user prompt using Google Generative AI.

    Args:
        prompt (str): User input describing the playlist.
    Returns:
        list[dict]: List of songs with title and artist.
    """
    try:
        logging.info(f"Generating playlist for prompt: {prompt}")

        # Step 1: Query Google Generative AI
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)

        logging.debug(f"LLM Response: {response.text}")

        # Step 2: Parse the LLM's response
        song_list = response.text.strip()
        songs = []
        for line in song_list.split("\n"):
            if " - " in line:
                title, artist = line.split(" - ", 1)
                songs.append({"title": title.strip(), "artist": artist.strip()})

        logging.info(f"Generated playlist: {songs}")
        return songs
    except Exception as e:
        logging.error(f"Error calling LLM API: {e}")
        return []

def generate_emotion_based_playlist(emotion: str, artist: str, language: str) -> list[dict]:
    """
    Generate a playlist based on emotion, artist, and language preferences.

    Args:
        emotion (str): Detected emotion (e.g., "Happy").
        artist (str): User's preferred artist.
        language (str): User's preferred language.
    Returns:
        list[dict]: List of songs with title and artist.
    """
    try:
        logging.info(f"Generating emotion-based playlist for: emotion={emotion}, artist={artist}, language={language}")

        prompt = (
            f"Create a playlist for someone feeling {emotion}. "
            f"Focus on songs by {artist} in {language}. "
            f"Provide songs in the format '<song title> - <artist>'."
        )
        songs = generate_playlist_from_prompt(prompt)

        logging.info(f"Generated emotion-based playlist: {songs}")
        return songs
    except Exception as e:
        logging.error(f"Error generating emotion-based playlist: {e}")
        return []
