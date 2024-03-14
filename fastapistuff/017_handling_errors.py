from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

mango = {"mango1": "Tasty mango"}


@app.get("/mango/{mango_id}")
async def get_mango(mango_id: str):
    if mango_id not in mango:
        raise HTTPException(status_code=404, detail="Mango not found")
    return {"mango": mango[mango_id]}


@app.get("/mango-headers/{mango_id}")
async def get_mango_headers(mango_id: str):
    if mango_id not in mango:
        raise HTTPException(
            status_code=404,
            detail="Mango not found",
            headers={"X-Error": "This is header error"}
        )

    return {"mango": mango[mango_id]}


class SomeCustomException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(SomeCustomException)
async def some_custom_exception_handler(request: Request, exc: SomeCustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"This is exception: {exc.name}"}
    )


@app.get("/bananas/{name}")
async def get_banana(name: str):
    if name == "green":
        raise SomeCustomException(name=name)

    return {"banana name": name}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # return PlainTextResponse(str(exc), status_code=400)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Orange(BaseModel):
    name: str
    size: int


@app.post("/oranges/{orange_id}")
async def get_orange(orange_id: int, orange: Orange | None = None):
    if orange_id == 3:
        raise HTTPException(status_code=418, detail="This is not available number")
    return {"orange_id": orange_id, "orange": orange}
