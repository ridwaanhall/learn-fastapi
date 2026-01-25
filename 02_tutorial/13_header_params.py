# header parameters

from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    user_agent: Annotated[
        str | None,
        Header()
    ] = None
):
    return {"User-Agent": user_agent}

## automatic conversion
@app.get("/users/")
async def read_users(
    strange_header: Annotated[
        str | None,
        Header(convert_underscores=False) # before settting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage of headers with underscores
    ] = None
):
    return {"Strange-Header": strange_header}

## duplicate headers
@app.get("/projects/")
async def read_projects(
    x_token: Annotated[
        list[str] | None,
        Header()
    ] = None
):
    return {"X-Token values": x_token}