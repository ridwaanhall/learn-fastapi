from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str # required field
    description: str | None = None # str or none. optional field with default None
    price: float # required field
    tax: float | None = None # float or none. optional field with default None
    
'''
json
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}

but, description and tax are optional
{
    "name": "Bar",
    "price": 23.5
}
'''

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump() # model_dump() method to convert Pydantic model to dictionary
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# request body + path parameters
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()} # ** to unpack dictionary

# request body + path + query parameters
@app.put("/users/{user_id}/items/{item_id}")
async def update_user_item(
    user_id: int, # path parameter user_id int
    item_id: int, # path parameter item_id int
    item: Item, # request body item of type Item
    q: str | None = None # optional query parameter q of type str or None, default is None
):
    result = {"user_id": user_id, "item_id": item_id, **item.model_dump()}
    if q: # if query parameter q is provided
        result.update({"q": q})
    return result