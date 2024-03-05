from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/oranges/")
async def get_oranges(strange_header: Annotated[str | None, Header(convert_underscores=False)] = None):
    return {"User-Agent": strange_header}


@app.get("/doubleheaders/")
async def get_duplicated_headers(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
