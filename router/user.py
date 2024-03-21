from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db import db_user
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/")
def create_user(user: UserBase, db: Session = Depends(get_db)) -> UserDisplay:
    user = db_user.create_user(
        db,
        user,
    )
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    status = db_user.delete_user(
        db,
        user_id,
    )
    return {"status": status}
