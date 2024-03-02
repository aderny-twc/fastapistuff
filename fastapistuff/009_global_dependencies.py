from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get("/mango/")
async def get_mango():
    return [{"item": "Mango one"}, {"item": "Mango two"}]


@app.get("/banana/")
async def get_banana():
    return [{"item": "Banana one"}, {"item": "Banana two"}]
