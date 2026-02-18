# response model - return type

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    
    
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(
            name="Foo",
            description="The Foo item",
            price=50.2,
            tax=10.5,
            tags=["foo", "item"]
        ),
        Item(
            name="Bar",
            description="The Bar item",
            price=62,
            tax=20.2,
            tags=["bar", "item"]
        )
    ]
    
    
## response_model parameter
from typing import Any

@app.post("/items2/", response_model=Item)
async def create_item2(item: Item) -> Any:
    return item


@app.get("/items2/", response_model=list[Item])
async def read_items2() -> Any:
    return [
        Item(
            name="Portal Gub",
            description="The Portal Gub item",
            price=100.0,
            tax=20.0,
            tags=["portal", "gub"]
        )
    ]
    
    
## Return the same input data

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
    
# dont do this in production, this is just for demonstration purposes
@app.post("/users/")
async def create_user(user: UserIn) -> UserIn:
    return user

## add an output model to hide the password
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
@app.post("/users2/", response_model=UserOut)
async def create_user2(user: UserIn) -> Any:
    return user

## Return Type and Data Filtering

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
class UserIn2(BaseUser):
    password: str
    
@app.post("/users3/")
async def create_user3(user: UserIn2) -> BaseUser:
    return user


## Return a Response Directly

from fastapi import Response
from fastapi.responses import JSONResponse, RedirectResponse


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Welcome to the portal!"})

## return a response directly
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

## annotate a response subclass
@app.get("/teleport2")
async def get_teleport2() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

## invalid return type
# @app.get("/invalid")
# async def get_invalid(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Welcome to the portal!"}

## disable response model
@app.get("/no_response_model/", response_model=None)
async def get_portal_no_response_model(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Welcome to the portal!"}


## response model encoding parameters

class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.9
    tags: list[str] = []
    
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items3/{item_id}", response_model=Item2, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

## response_model_include and response_model_exclude

class Item4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items4/{item_id}/name",
    response_model=Item4,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items4/{item_id}/public", response_model=Item4, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]