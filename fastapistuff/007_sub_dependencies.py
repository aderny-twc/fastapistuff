from fastapi import FastAPI, Cookie, Depends
from typing import Annotated

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


def another_query_extractor(
    q: Annotated[str, Depends(query_extractor)]
):
    if not q:
        return "Another query"


@app.get("/dragonfruit/")
async def get_dragonfruit(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}


@app.get("/peach/")
async def get_peach(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
    another_query: Annotated[str, Depends(another_query_extractor, use_cache=False)]
):
    return {"q_or_cookie": query_or_default, "another": another_query}
