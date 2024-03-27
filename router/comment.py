from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db.database import get_db
from db import db_comment
from schemas import UserAuth, CommentBase, Comment

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.post("/")
def create_comment(comment: CommentBase, db: Session = Depends(get_db), _current_user: UserAuth = Depends(get_current_user)):
    comment = db_comment.create(
            db,
            comment
        )

    return comment


@router.get("/post/")
def post_comments(post_id: int, db: Session = Depends(get_db)) -> list[Comment]:
    return db_comment.get_by_post(db, post_id)
