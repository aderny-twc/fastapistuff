from sqlalchemy.orm import Session
from schemas import PostBase
from db.models import DbPost
from datetime import datetime


def create(db: Session, post_request: PostBase):
    new_post = DbPost(
        image_url=post_request.image_url,
        image_url_type=post_request.image_url_type,
        caption=post_request.caption,
        timestamp=datetime.now(),
        user_id=post_request.creator_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def get_all(db: Session):
    all_posts = db.query(DbPost).all()

    return all_posts