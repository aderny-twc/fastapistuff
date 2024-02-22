from enum import Enum
from pydantic import BaseModel, Field, HttpUrl

from fastapi import FastAPI, Query, Path, Body
from typing import Annotated

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


class OrderItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/order-items/")
async def create_item(item: OrderItem):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: OrderItem, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}

    if q:
        result.update({"q": q})

    return result


@app.get("/products/")
async def get_products(q: Annotated[
    str | None, Query(title="New title", description="New description", min_length=5, max_length=50,
                      pattern="^fixedquery$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})

    return results


@app.get("/positions/")
async def get_positions(q: Annotated[str | None, Query(alias="item-query", deprecated=True)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})

    return results


@app.get("/things/")
async def get_things(q: Annotated[str | None, Query(alias="item-query", include_in_schema=False)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})

    return results


@app.get("/some_values/{value_id}")
async def get_some_values(value_id: Annotated[int, Path(title="ID of a value")],
                          q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"value_id": value_id}
    if q:
        results.update({"q": q})

    return results


@app.get("/handy_order/{item_id}")
async def read_values(*, item_id: int = Path(title="Title"), q: str):
    return []


@app.get("/numbers/{num_id}")
async def get_numbers(num_id: Annotated[int, Path(gt=0, le=1000)], q: str):
    results = {"num_id": num_id}
    if q:
        results.update({"q": q})

    return results


class Parameter(BaseModel):
    name: str
    descripton: str | None = Field(
        default=None, title="The title of the parameter", max_length=300
    )
    price: float = Field(gt=0, description="This is the price of the parameter")
    tas: float | None = None


class Apples(BaseModel):
    weight: float
    color: str
    quantity: int = 1


@app.put("/body_parameter/{param_id}")
async def update_parameters(
        param_id: Annotated[int, Path(ge=0, le=1000)],
        q: str | None = None,
        param: Parameter | None = None,
        # param: Annotated[Parameter, Body(embed=True)] = None,
        apples: Apples | None = None,
        importance: Annotated[int, Body(gt=0)] = None,
):
    results = {"param_id": param_id}
    if q:
        results.update({"q": q})
    if param:
        results.update({"param": param})
    if apples:
        results.update({"apples": apples})
    if importance:
        results.update({"importance_id": importance})

    return results


class Image(BaseModel):
    url: HttpUrl
    name: str


class Orange(BaseModel):
    name: str
    description: str | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/oranges/{orange_id}")
async def update_orange(orange_id: int, orange: Orange):
    result = {"orange_id": orange_id, "orange": orange}
    return result


@app.post("/orange_images/multiple/")
async def create_multiple_orange_images(images: list[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
