from fastapi import FastAPI
from fastapi.responses import FileResponse

from stpapp.models.user import User

app = FastAPI()

FILE = "index.html"


@app.get("/start/", response_class=FileResponse)
def return_start_html():
    return FILE


@app.post("/summer/")
def return_sum(num1: float, num2: float):
    return {"result": num1 + num2}


@app.get("/user/")
def return_user() -> User:
    user = User(id=1, name="John", age=19)
    return user


@app.post("/user/create/")
def return_user(user: User) -> User:
    return User(id=user.id, name=user.name, age=user.age, is_adult=user.age >= 18)
