from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated


class DBSession:
    def close(self):
        pass


async def get_db():
    db = DBSession()
    try:
        yield db
    # code following the yield statement is executed after the response has been delivered
    finally:
        db.close()


async def dependency_a():
    dep_a = None
    try:
        yield dep_a
    finally:
        print("work is done")


async def dependency_b(dep_a: Annotated[None, Depends(dependency_a)]):
    dep_b = "some dep"
    try:
        yield dep_b
    finally:
        print(dep_a)
        dep_b.upper()


async def dependency_c(dep_b: Annotated[str, Depends(dependency_b)]):
    dep_c = 123
    try:
        yield dep_c
    finally:
        print(dep_b)
        dep_c.to_bytes()


app = FastAPI()

data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item
