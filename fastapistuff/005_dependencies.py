from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()


async def common_params(
    q: str | None = None, skip: int = 0, limit: int = 100
) -> dict:
    return {"q": q, "skip": skip, "limit": limit}


CommonDep = Annotated[dict, Depends(common_params)]


@app.get("/apples/")
async def get_apples(commons: CommonDep):
    return commons


@app.get("/oranges/")
async def read_users(commons: CommonDep):
    return commons
