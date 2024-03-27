from sqlalchemy.orm import Session
from schemas import CommentBase, Comment
from db.models import DbComment
from datetime import datetime


def create(db: Session, request_comment: CommentBase):
    new_comment = DbComment(
        text=request_comment.text,
        username=request_comment.username,
        post_id=request_comment.post_id,
        timestamp=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_by_post(db: Session, post_id: int) -> list[Comment]:
    return db.query(DbComment).filter(DbComment.id == post_id).all()
