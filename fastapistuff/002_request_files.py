from fastapi import FastAPI, File, UploadFile
from typing import Annotated

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    print(contents)
    return {"filename": file.filename}


@app.post("/optionalfiles/")
async def create_optional_file(
    file: Annotated[bytes | None, File(description="A file read as bytes")] = None
):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/optionaluploadfile/")
async def create_optional_upload_file(
    file: Annotated[UploadFile | None, File(description="A file read as UploadFile")] = None
):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
