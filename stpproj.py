from fastapi import FastAPI
# for serving static files
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount


@app.get("/start/")
def return_start_html():
    return
