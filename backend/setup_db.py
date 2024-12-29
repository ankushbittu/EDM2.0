from app.dependencies.db import Base, engine
from app.models.user import User
from app.models.playlist import Playlist
from app.models.emotion import Emotion

def reset_database():
    """
    Drop all tables (optional for a complete reset) and recreate the schema.
    """
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Database schema created successfully!")

if __name__ == "__main__":
    reset_database()
