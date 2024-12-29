from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    """
    A test route to retrieve user profile information.
    """
    return {"email": user.email, "message": "Profile data retrieved successfully"}
