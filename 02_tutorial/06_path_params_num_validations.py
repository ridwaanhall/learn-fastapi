# Path Parameters and Numeric Validations

from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

'''
gt: greater than
ge: greater than or equal
lt: less than
le: less than or equal
'''

# example endpoint with path parameter
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[
        int,
        Path(
            title="The ID of the item to get", # title for documentation
        )
    ],
    q: Annotated[
        str | None,
        Query(
            alias="item-query", # alias for the query parameter
        ),
    ] = None
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result

# Number validations: greater than or equal
@app.get("/users/{user_id}")
async def read_users(
    user_id: Annotated[
        int,
        Path(
            title="The ID of the user to get",
            ge=2, # greater than or equal to 2
        )
    ],
    q: str
):
    result = {"user_id": user_id}
    if q:
        result.update({"q": q})
    return result

# Number validations: greater than and less than or equal
@app.get("/products/{product_id}")
async def read_products(
    product_id: Annotated[
        int,
        Path(
            title="The ID of the product to get",
            gt=5, # greater than 5
            le=10, # less than or equal to 10
        )
    ],
    q: str
):
    result = {"product_id": product_id}
    if q:
        result.update({"q": q})
    return result

# Number validations: floats, greater than and less than
@app.get("/orders/{order_id}")
async def read_orders(
    *,
    order_id: Annotated[
        int,
        Path(
            title="The ID of the order to get",
            ge=0, # greater than or equal to 0
            le=1000, # less than or equal to 1000
        )
    ],
    q: str,
    price: Annotated[
        float,
        Query(
            gt=0, # greater than 0
            lt=10.5, # less than 10.5
        )
    ]
):
    result = {"order_id": order_id}
    if q:
        result.update({"q": q})
    if price:
        result.update({"price": price})
    return result