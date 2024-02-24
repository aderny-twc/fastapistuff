from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

FILE = "index.html"


@app.get("/start/", response_class=FileResponse)
def return_start_html():
    return FILE


@app.post("/summer/")
def return_sum(num1: float, num2: float):
    return {"result": num1 + num2}
