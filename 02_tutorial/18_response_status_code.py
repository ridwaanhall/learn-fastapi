# response status code
'''
@app.get()
@app.post()
@app.put()
@app.delete()
etc.
'''

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/", status_code=201) # created
async def create_item(name: str):
    return {"name": name}

'''
100-199: Informational
200-299: Success
300-399: Redirection
400-499: Client Errors
500-599: Server Errors
'''

## shortcut to remember the names

from fastapi import status

@app.get("/items-short/", status_code=status.HTTP_201_CREATED) # created
async def create_item_short(name: str):
    return {"name": name}