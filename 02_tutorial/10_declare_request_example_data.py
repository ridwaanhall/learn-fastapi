# declade request example data

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
    }
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# field additional arguments

from pydantic import Field

class ItemWithFieldExample(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
    
@app.put("/items_with_field/{item_id}")
async def update_item_with_field(item_id: int, item: ItemWithFieldExample):
    results = {"item_id": item_id, "item": item}
    return results

# examples in JSON Schema - OpenAPI

'''
path()
Query()
Header()
Cookie()
Body()
Form()
File()
'''

## body with examples

from fastapi import Body
from typing import Annotated

class ItemWithBodyExample(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
@app.put("/items_with_body/{item_id}")
async def update_item_with_body(
    item_id: int,
    item: Annotated[
        ItemWithBodyExample,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results

## body with multiple examples
class ItemWithMultipleExamples(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items_with_multiple_examples/{item_id}")
async def update_item_with_multiple_examples(
    *,
    item_id: int,
    item: Annotated[
        ItemWithMultipleExamples,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results

## openAPI-specific examples
class ItemWithOpenAPIExamples(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
@app.put("/items_with_openapi_examples/{item_id}")
async def update_item_with_openapi_examples(
    *,
    item_id: int,
    item: Annotated[
        ItemWithOpenAPIExamples,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results