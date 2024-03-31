import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from schemas import PostBase
from db.models import DbPost
from datetime import datetime


async def create(session: AsyncSession, post_request: PostBase):
    new_post = DbPost(
        image_url=post_request.image_url,
        image_url_type=post_request.image_url_type,
        caption=post_request.caption,
        timestamp=datetime.now(),
        user_id=post_request.creator_id,
    )
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    return new_post


class NotAllowedDeletion(Exception):
    pass


async def delete(session: AsyncSession, post_id: int, user_id: int):
    post = sqlalchemy.select(DbPost).where(DbPost.id == post_id, DbPost.user_id == user_id).limit(1)
    post = await session.execute(post)
    if post:
        query = sqlalchemy.select(DbPost).where(DbPost.id == post_id, DbPost.user_id == user_id)
        await session.execute(query)
        await session.commit()
    else:
        raise NotAllowedDeletion


async def get_all(session: AsyncSession):
    all_posts = sqlalchemy.select(DbPost)
    result = await session.execute(all_posts)
    return [post for (post,) in result.all()]
