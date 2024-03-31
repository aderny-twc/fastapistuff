import shutil

from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from random import choice
import string

from auth.oauth2 import get_current_user
from db.database import async_session
from db import db_post
from db.db_post import NotAllowedDeletion
from schemas import PostBase, PostDisplay, UserAuth

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_types = ["absolute", "relative"]


@router.post("/")
async def create_post(post: PostBase, session: AsyncSession = Depends(async_session), _current_user: UserAuth = Depends(get_current_user)) -> PostDisplay:
    if post.image_url_type not in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Image types might be only {image_url_types}"
        )

    new_post = await db_post.create(
        session,
        post,
    )
    return new_post


@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(async_session), _current_user: UserAuth = Depends(get_current_user)):
    try:
        await db_post.delete(
            session,
            post_id,
            _current_user.id,
        )
    except NotAllowedDeletion:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This is not your post")
    return {"status": "OK"}


@router.get("/")
async def get_all_posts(session: AsyncSession = Depends(async_session)) -> list[PostDisplay]:
    return await db_post.get_all(session)


@router.post("/image")
def load_image(image: UploadFile = File(...), _current_user: UserAuth = Depends(get_current_user)):
    generated_name = ''.join(choice(string.ascii_letters) for i in range(6))
    suffix = f"_{generated_name}."
    filename = suffix.join(image.filename.rsplit(".", 1))
    path = f"media/{filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}
