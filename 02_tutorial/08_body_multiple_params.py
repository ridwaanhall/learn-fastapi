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