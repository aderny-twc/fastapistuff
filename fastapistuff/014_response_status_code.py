from fastapi import FastAPI, status

app = FastAPI()


@app.post("/orange/", status_code=status.HTTP_201_CREATED)
async def grow_orange(type: str):
    return {"type": type}
