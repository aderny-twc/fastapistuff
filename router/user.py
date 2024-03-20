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
@router.get("/")
def read_all_users(db: Session = Depends(get_db)) -> list[UserDisplay]:
    users = db_user.get_all_users(
        db,
    )
    return users


# Read one user
@router.get("/{user_id}")
def read_one_user(user_id: int, db: Session = Depends(get_db)) -> UserDisplay:
    user = db_user.get_user(
        db,
        user_id
    )
    return user


# Update
@router.post("/{user_id}")
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    status = db_user.update_user(
        db,
        user_id,
        user,
    )
    return {"status": status}


# Delete
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    status = db_user.delete_user(
        db,
        user_id,
    )
    return {"status": status}
