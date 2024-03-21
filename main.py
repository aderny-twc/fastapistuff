from fastapi import FastAPI

from db.database import engine
from db import models
from router import user

app = FastAPI()
app.include_router(user.router)


@app.get("/")
def index():
    return {"message": "Hello world!"}


models.Base.metadata.create_all(engine)
