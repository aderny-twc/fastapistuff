from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy
from schemas import UserBase
from db.models import DbUser
from db.hash import Hash


async def create_user(session: AsyncSession, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def delete_user(session: AsyncSession, id: int):
    query = sqlalchemy.select(DbUser).where(DbUser.id == id).limit(1)
    user = await session.execute(query)

    if user:
        query = sqlalchemy.delete(DbUser).where(DbUser.id == id)
        await session.execute(query)
        await session.commit()
        return "OK"

    return "Not found"


async def get_user_by_username(session: AsyncSession, username: str):
    users_query = await session.execute(
        sqlalchemy.select(DbUser)
        .where(DbUser.username == username)
        .limit(1)
    )
    user = users_query.first()
    return user[0] if user else None
