from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# They can declare request requirements (like headers) or other sub-dependencies
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    # And they can return values or not, the values won't be used
    return x_key


@app.get("/mango/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def get_mango():
    return [{"item": "Mango1"}, {"item": "Mango2"}]
