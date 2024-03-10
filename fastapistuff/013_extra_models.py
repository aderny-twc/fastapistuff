from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_pass: str):
    return "Supersecret" + raw_pass


def fake_save_user(user_in: UserIn) -> UserInDB:
    hashed_pass = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_pass)
    print("User saved!")

    return user_in_db


@app.post("/users/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


class ClientBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class ClientIn(ClientBase):
    password: str


class ClientInDB(ClientBase):
    hashed_password: str


def fake_save_client(client_in: ClientIn):
    hashed_pass = fake_password_hasher(client_in.password)
    client_in_db = ClientInDB(**client_in.dict(), hashed_password=hashed_pass)
    print("Client saved!")
    return client_in_db


@app.post("/client/", response_model=ClientBase)
async def create_client(client_in: ClientIn):
    client_saved = fake_save_client(client_in)
    return client_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


@app.get("/baseitems/", response_model=list[BaseItem])
async def read_items():
    return items.values()


@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
