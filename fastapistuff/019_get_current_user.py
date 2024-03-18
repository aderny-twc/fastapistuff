from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="jim@mail.com", full_name="Jim Halpert"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return fake_decode_token(token)


@app.get("/user/me")
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
