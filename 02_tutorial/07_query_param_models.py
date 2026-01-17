# Query Parameter Models

'''
You can use Pydantic models to declare query parameters in FastAPI.
'''

## Query Parameters with a Pydantic Model

from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    limit: int = Field(10, ge=1, le=100)  # limit between 1 and 100
    offset: int = Field(0, ge=0)  # offset must be non-negative
    order_by: Literal["created_at", "updatedat"] = "created_at"
    tags: list[str] = None  # optional list of tags
    
@app.get("/items/")
async def read_items(
    filter_query: Annotated[
        FilterParams, # use FilterParams model to parse and validate query parameters
        Query(),
    ]
):
    return filter_query

## Forbid Extra Query Parameters
class StrictFilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # forbid extra data in the query parameters, raise validation error if any extra parameter is provided
    
    limit: int = Field(10, ge=1, le=100)  # limit between 1 and 100
    offset: int = Field(0, ge=0)  # offset must be non-negative
    order_by: Literal["created_at", "updatedat"] = "created_at"
    tags: list[str] = None  # optional list of tags
    
@app.get("/strict-items/")
async def read_strict_items(
    filter_query: Annotated[
        StrictFilterParams, # use StrictFilterParams model to parse and validate query parameters
        Query(),
    ]
):
    return filter_query