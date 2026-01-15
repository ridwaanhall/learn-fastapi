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
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict