from fastapi import FastAPI, Cookie
from typing import Annotated

app = FastAPI()


@app.get("/bananas/")
# async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
async def read_items(ads_id: int | None = Cookie(None)):
    print(ads_id)
    return {"ads_id": ads_id}
