# Query Parameters and String Validations

from fastapi import FastAPI

app = FastAPI()


# example endpoint with optional query parameter
@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
