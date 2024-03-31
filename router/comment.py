from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.oauth2 import get_current_user
from db.database import async_session
from db import db_comment
from schemas import UserAuth, CommentBase, Comment

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)


@router.post("/")
async def create_comment(comment: CommentBase, session: AsyncSession = Depends(async_session), _current_user: UserAuth = Depends(get_current_user)):
    comment = await db_comment.create(
            session,
            comment
        )

    return comment


@router.get("/post/")
async def post_comments(post_id: int, session: AsyncSession = Depends(async_session)) -> list[Comment]:
    return await db_comment.get_by_post(session, post_id)
