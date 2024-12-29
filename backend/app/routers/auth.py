import fastapi
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.services.auth_service import hash_password, create_access_token, authenticate_user
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and save the user
    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Log in an existing user and generate a JWT token.
    """
    # Authenticate the user
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate a JWT token
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}