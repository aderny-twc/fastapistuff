from enum import Enum

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():  # This name is showed in swagger docs
    return {"message": "hello"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):  # this type will be validated
    return {"item_id": item_id}


@app.get("/users/me")
async def get_current_user():
    return {"user": {"user_id": 1, "name": "Admin"}}


@app.get("/users/{user_id}")
async def get_specific_user(user_id: int):
    return {"user": {"user_id": user_id, "name": "John"}}


class Values(str, Enum):
    one = "one"
    two = "two"
    three = "three"


@app.get("/values/{value_name}")
async def get_value(value_name: Values):
    if value_name is Values.one:
        return {"value": value_name, "message": "Value number one"}

    if value_name is Values.two:
        return {"value": value_name, "message": "Value number two"}

    if value_name is Values.three:
        return {"value": value_name, "message": "Value number three"}

    return {"value": "undefined", "message": "What is this"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/someitems/{item_id}")
async def read_items1(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long descr"}
        )
    return item