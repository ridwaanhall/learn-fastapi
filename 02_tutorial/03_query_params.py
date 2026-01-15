from fastapi import FastAPI

app = FastAPI()

fake_items_db = [
    {
        "item_name": "Foo"
    },
    {
        "item_name": "Bar"
    },
    {
        "item_name": "Baz"
    },
    {
        "item_name": "Qux"
    },
    {
        "item_name": "Quux"
    },
    {
        "item_name": "Corge"
    },
    {
        "item_name": "Grault"
    },
    {
        "item_name": "Garply"
    },
    {
        "item_name": "Waldo"
    },
    {
        "item_name": "Fred"
    },
    {
        "item_name": "Plugh"
    },
    {
        "item_name": "Fufu"
    },
    {
        "item_name": "Fafa"
    },
]

# default query parameters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit] # skip means start from index skip, limit means take limit items

# optional query parameters
@app.get("/users/")
async def read_user(username: str | None = None): # | is used for Union in Python 3.10+. what is union? union means either one type or another type.
    if username:
        return {"username": username} # use ?username=your_name to test
    return {"message": "Hello, Guest"}

# another optional query and path parameter example
@app.get("/articles/{article_id}")
async def read_article(article_id: int, q: str | None = None):
    if q:
        return {"article_id": article_id, "q": q} # article_id is a path parameter integer (int). use ?q=your_query to test
    return {"article_id": article_id}

# query parameter type conversion (declare bool types)
'''
bool type conversion rules:
    1. (case insensitive) "true", "1", "on", and "yes" are converted to True
    2. (case insensitive) "false", "0", "off", and "no" are converted to False
    3. any other value will raise a validation error
'''
@app.get("/products/{product_id}")
async def read_product(product_id: str, q: str | None = None, short: bool = False):
    product = {
        "product_id": product_id
    }
    if q: # q is optional str or None but default is None
        product.update({"q": q})
    if not short: # short is bool, default is False
        product.update(
            {
                "description": "This is a long description for the product. Hidup Jokowii!!"
            }
        )
    return product

# multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, # user_id is path parameter int
    item_id: str, # item_id is path parameter str
    q: str | None = None, # q is optional query parameter str or None. default is None
    short: bool = False # short is query parameter bool, default is False
):
    item = {
        "item_id": item_id,
        "owner_id": user_id
    }
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is a long description for the item. Hidup Jokowii!!"
            }
        )
    return item

# required query parameters
@app.get("/orders/{order_id}")
async def read_order(order_id: str, needy: str): # needy is required query parameter str
    order = {
        "order_id": order_id,
        "needy": needy
    }
    return order

# required parameters as required, some having defaults, some entirely optional
@app.get("/comments/{comment_id}")
async def read_comment(
    comment_id: int, # comment_id is path parameter int
    required: str, # required is required query parameter str
    skip: int = 0, # skip is query parameter int, default is 0
    limit: int | None = None # limit is optional query parameter int or None, default is None
):
    comment = {
        "comment_id": comment_id,
        "required": required,
        "skip": skip
    }
    if limit:
        comment.update({"limit": limit})
    return comment