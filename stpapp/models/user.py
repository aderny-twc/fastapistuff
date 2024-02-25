from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    is_adult: bool = False
