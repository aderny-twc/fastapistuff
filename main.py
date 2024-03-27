from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db.database import engine
from db import models
from router import user, post, comment
from auth import authentication

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router)


@app.get("/")
def index():
    return {"message": "Hello world!"}


models.Base.metadata.create_all(engine)

app.mount("/media", StaticFiles(directory="media"), name="media")
