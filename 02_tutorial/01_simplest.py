from fastapi import FastAPI

app = FastAPI()


# simplest endpoint
@app.get("/")
async def read_root():
    return {"Hello": "RoneAI"}


# path parameters with type hints
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# another path parameter example
@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}

# path parameters containing paths
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}