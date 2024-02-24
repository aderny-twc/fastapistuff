from fastapi import FastAPI, Response
from fastapi.responses import (
    ORJSONResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
    FileResponse,
)

app = FastAPI()


# Custom Response - HTML, Stream, File, others

@app.get("/objects/", response_class=ORJSONResponse)
async def read_items():
    return ORJSONResponse([{"object_id": "123ID"}])


@app.get("/pages/", response_class=HTMLResponse)
async def return_html_response():
    html_string = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """

    return html_string


@app.get("/responses/")
async def read_responses():
    html_string = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! This is new HTML!</h1>
        </body>
    </html>
    """

    return HTMLResponse(content=html_string, status_code=200)


@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """

    return Response(content=data, media_type="application/xml")


@app.get("/plaintext/", response_class=PlainTextResponse)
def get_plain_text_response():
    return "How you doing?"


@app.get("/redirector")
def get_redirector():
    return RedirectResponse("https://www.google.com")


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


@app.get("/streamer/")
def get_streamer():
    return StreamingResponse(fake_video_streamer())


FILE_PATH = "/somepath/index.html"


@app.get("/somefile/")
async def get_somefile():
    return FileResponse(FILE_PATH)


@app.get("/somefile2/", response_class=FileResponse)
async def get_somefile2():
    return FILE_PATH
