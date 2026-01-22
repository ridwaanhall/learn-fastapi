# Body - Multiple Parameters

## Mix Path, Query and body parameters

from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[
        int,
        Path(
            title="The ID of the item to update",
            ge=1,  # greater than or equal to 1
        ),
    ],
    q: str | None = None,  # optional query parameter q of type str or None, default is None
    item: Item | None = None,  # optional request body item of type Item or None, default is None
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item})
    return result

## Multiple body parameters

class User(BaseModel):
    username: str
    full_name: str | None = None
    
@app.put("/users/{user_id}")
async def update_user(
    user_id: int,  # path parameter user_id of type int
    item: Item,  # request body item of type Item
    user: User  # request body user of type User
):
    result = {"user_id": user_id, "item": item, "user": user}
    return result

## singular values in body
from fastapi import Body

@app.put("/singular/{singular_id}")
async def update_singular(
    singular_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()]
):
    result = {
        "singular_id": singular_id,
        "item": item,
        "user": user,
        "importance": importance,
    }
    return result

## multiple body params and query
@app.put("/multiple/{multiple_id}")
async def update_multiple(
    *,
    multiple_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
    q: str | None = None # optional query parameter q of type str or None, default is None
):
    result = {
        "multiple_id": multiple_id,
        "item": item,
        "user": user,
        "importance": importance,
    }
    if q:
        result.update({"q": q})
    return result

## embed a single body param
@app.put("/embed/{embed_id}")
async def update_embed(
    embed_id: int,
    item: Annotated[Item, Body(embed=True)]
):
    result = {
        "embed_id": embed_id,
        "item": item,
    }
    return result