from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CommentBase, Comment
from db.models import DbComment
from datetime import datetime
import sqlalchemy


async def create(session: AsyncSession, request_comment: CommentBase):
    new_comment = DbComment(
        text=request_comment.text,
        username=request_comment.username,
        post_id=request_comment.post_id,
        timestamp=datetime.now()
    )
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment


async def get_by_post(session: AsyncSession, post_id: int) -> list[Comment]:
    query = sqlalchemy.select(DbComment).where(DbComment.id == post_id)
    result = await session.execute(query)
    return [comment for (comment,) in result.all()]
