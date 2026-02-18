# cookie parameter models

## cookie with a pydantic model

from typing import Annotated

from fastapi import FastAPI, Cookie
from pydantic import BaseModel

app = FastAPI()


class CookieModel(BaseModel):
    session_id: str
    facebook: str | None = None
    twitter: str | None = None
    
@app.get("/cookie/")
async def read_cookie(
    cookies: Annotated[
        CookieModel,
        Cookie()
    ]):
    return cookies

## forbid exra cookies
class CookieModel2(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    
    session_id: str
    facebook: str | None = None
    twitter: str | None = None
    
@app.get("/cookie2/")
async def read_cookie2(
    cookies: Annotated[
        CookieModel2,
        Cookie()
    ]):
    return cookies