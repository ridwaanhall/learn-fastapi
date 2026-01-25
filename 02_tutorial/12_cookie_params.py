# cookie parameters
from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(
    ads_id: Annotated[
        str | None,
        Cookie() # declare a cookie parameter, using the same common pattern as Query, Path, etc.
    ] = None,
):
    return {"ads_id": ads_id}