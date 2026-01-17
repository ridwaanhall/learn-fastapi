# Query Parameters and String Validations
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


# example endpoint with optional query parameter
@app.get("/items/")
async def read_items(
    q: str | None = None
):
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
            min_length=3, # minimum length of the string is 3 characters
            max_length=50 # maximum length of the string is 50 characters
        ),
    ] = None
):
    results = {"users": [{"username": "pejabat"}, {"username": "theotown"}]}
    if q:
        results.update({"q": q})
    return results

# example endpoint without Annotated
@app.get("/products/")
async def read_products(
    q: str | None = Query( # optional query parameter of type str or None, default is None
        default=None, # default value is None
        min_length=3, # minimum length of the string is 3 characters
        max_length=20, # maximum length of the string is 20 characters
    )
):
    results = {"products": [{"product_id": "Widget"}, {"product_id": "Gadget"}]}
    if q:
        results.update({"q": q})
    return results

# add regular expression validation to query parameter
@app.get("/orders/")
async def read_orders(
    q: Annotated[ # Annotated means we can add extra information to the type
        str | None, # optional query parameter of type str or None, default is None
        Query(
            min_length=3, # minimum length of the string is 3 characters
            max_length=50, # maximum length of the string is 50 characters
            pattern="^fixedquery$", # regular expression pattern to match the exact string "fixedquery". ^: stars with following characters does not have any character before it, $: ends with preceding characters does not have any character after it.
        ),
    ] = None
):
    results = {"orders": [{"order_id": "Order1"}, {"order_id": "Order2"}]}
    if q:
        results.update({"q": q})
    return results

# example endpoint with default values other tnan None
@app.get("/customers/")
async def read_users(
    q: Annotated[
        str,
        Query(
            min_length=3
        )
    ] = "fixedquery" # default value is "fixedquery" or dont add default value to make it required
):
    results = {"customers": [{"customer_id": "Cust1"}, {"customer_id": "Cust2"}]}
    if q:
        results.update({"q": q})
    return results

# required, can be None
@app.get("/invoices/")
async def read_invoices(
    q: Annotated[
        str | None, # can be None
        Query(
            min_length=3
        )
    ]
):
    results = {"invoices": [{"invoice_id": "Inv1"}, {"invoice_id": "Inv2"}]}
    if q:
        results.update({"q": q})
    return results

# query parameter list / multiple values
@app.get("/payments/")
async def read_payment(
    q: Annotated[
        list[str] | None, # list of strings or None
        Query()
    ] # = None #  add = None to make it optional
):
    results = {"payments": [{"payment_id": "Pay1"}, {"payment_id": "Pay2"}]}
    if q:
        results.update({"q": q})
    return results

# query parameter list / multiple values with default values
@app.get("/shipments/")
async def read_shipments(
    q: Annotated[
        list[str], # list of strings
        Query()
    ] = ["default1", "default2"] # default values
):
    query_items = {"q": q}
    return query_items

# use list directly instead of list[str]
@app.get("/deliveries/")
async def read_deliveries(
    q: Annotated[
        list, # list of any type
        Query()
    ] = []
):
    query_items = {"q": q}
    return query_items

# declare more metadata
@app.get("/reviews/")
async def read_reviews(
    q: Annotated[
        str | None,
        Query(
            title="Query Title", # title metadata
            description="Query string for the reviews to search in the database that have a good match", # description metadata
        )
    ] = None
):
    results = {"reviews": [{"review_id": "Rev1"}, {"review_id": "Rev2"}]}
    if q:
        results.update({"q": q})
    return results


# alias parameters
@app.get("/coupons/")
async def read_coupons(
    q: Annotated[
        str | None,
        Query(
            alias="coupon-code" # alias for the query parameter q
        )
    ] = None
):
    results = {"coupons": [{"coupon_id": "Coup1"}, {"coupon_id": "Coup2"}]}
    if q:
        results.update({"q": q})
    return results

# deprecated parameters
@app.get("/vouchers/")
async def read_vouchers(
    q: Annotated[
        str | None,
        Query(
            alias="voucher-code",
            title="Voucher Code",
            description="Code to redeem voucher. Format: VOUCHER-XXX where XXX are digits.",
            min_length=5,
            max_length=20,
            pattern="^VOUCHER-[0-9]{3}$",
            deprecated=True # mark the query parameter q as deprecated (will show warning in docs)
        )
    ] = None,
):
    results = {"vouchers": [{"voucher_id": "Vouch1"}, {"voucher_id": "Vouch2"}]}
    if q:
        results.update({"q": q})
    return results

# exclude params from OpenAPI
@app.get("/subscriptions/")
async def read_subscriptions(
    hidden_query: Annotated[
        str | None,
        Query(
            include_in_schema=False # exclude this query parameter from OpenAPI schema
        )
    ] = None
):
    results = {"subscriptions": [{"subscription_id": "Sub1"}, {"subscription_id": "Sub2"}]}
    if hidden_query:
        return {"subscription_id": "Sub1", "hidden_query": hidden_query}
    return results

# custom validation
import random
from pydantic import AfterValidator

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format. Must start with 'isbn-' or 'imdb-'.")
    return id

@app.get("/books/")
async def read_books(
    id: Annotated[
        str | None,
        AfterValidator(check_valid_id) # custom validation using AfterValidator
    ] = None
):
    if id:
        title = data.get(id, "Unknown Book")
    else:
        id, title = random.choice(list(data.items()))
    return {"id": id, "title": title}