# Query Parameters and String Validations
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


# example endpoint with optional query parameter
@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# example endpoint with string validations on query parameter
@app.get("/users/")
async def read_users(
    q: Annotated[ # Annotated means we can add extra information to the type
        str | None, # optional query parameter of type str or None, default is None
        Query(
            max_length=50 # maximum length of the string is 50 characters
        ),
    ] = None
):
    results = {"users": [{"username": "johndoe"}, {"username": "alice"}]}
    if q:
        results.update({"q": q})
    return results