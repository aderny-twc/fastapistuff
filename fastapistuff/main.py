from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():  # This name is showed in swagger docs
    return {"message": "hello"}
