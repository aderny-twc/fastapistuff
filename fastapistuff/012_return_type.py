from fastapi import FastAPI, Response
from pydantic import BaseModel, EmailStr
from typing import Any
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


@app.post("/items/response_model/", response_model=Item)
async def create_item2(item: Item) -> Any:
    return item


@app.get("/items/response_model/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> UserIn:
    return user


class BaseClient(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class ClientIn(BaseClient):
    password: str


@app.post("/client/")
async def create_user(user: ClientIn) -> BaseClient:
    return user


@app.get("/mango/")
async def get_mango(juicy: bool = False) -> Response:
    if not juicy:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your juicy mango"})


@app.get("/apple/")
async def get_apple() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# This will fail:
# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here's your interdimensional portal."}


@app.get("/banana", response_model=None)
async def get_banana(yellow: bool = False) -> Response | dict:
    if yellow:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


class Camera(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


cameras = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/cameras/{camera_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(camera_id: str):
    return cameras[camera_id]
