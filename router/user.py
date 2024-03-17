from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db import db_user
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


# Create
@router.post("/")
def create_user(user: UserBase, db: Session = Depends(get_db)) -> UserDisplay:
    user = db_user.create_user(
        db,
        user,
    )
    return user

# Read


# Update


# Delete
