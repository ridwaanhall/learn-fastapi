from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str # required field
    description: str | None = None # str or none. optional field with default None
    price: float # required field
    tax: float | None = None # float or none. optional field with default None
    total: float | None = None  # optional field to hold computed total price
    
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
    item.name = item.name.upper()  # just an example operation
    item.total = item.price + item.tax # calculate total price
    return item