# header parameter models

## header parameters wih a pydantic model

from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class MainHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
    
    
@app.get("/items/")
async def read_items(headers: Annotated[MainHeaders, Header()]):
    return headers


## forbid extra headers
class MainHeaders2(BaseModel):
    model_config = {
        "extra": "forbid"
    }
    
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
    
    
@app.get("/items2/")
async def read_items2(headers: Annotated[MainHeaders2, Header()]):
    return headers