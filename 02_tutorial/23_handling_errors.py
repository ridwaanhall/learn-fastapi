# Handling Errors

## use httpexceptions

from fastapi import FastAPI, HTTPException

app = FastAPI()

sawit = {
    "sawit": "The Sawit is a tall tropical plant with feather-like leaves and clusters of reddish fruits rich in oil."
}


@app.get("/sawit/{sawit_id}")
async def read_sawit(sawit_id: str):
    if sawit_id not in sawit:
        raise HTTPException(
            status_code=404,
            detail="No sawit found with the given ID",
            headers={"X-Error": "No sawit found with the given ID"},
        )
    return {"sawit_id": sawit_id, "name": sawit[sawit_id]}


## install custom exception handlers

from fastapi import Request
from fastapi.responses import JSONResponse


class SawitException(Exception):
    def __init__(self, name: str):
        self.name = name
        
@app.exception_handler(SawitException)
async def sawit_exception_handler(request: Request, exc: SawitException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a sawit!"
        },
    )
    
@app.get("/sawits/{sawit_id}")
async def read_sawits(sawit_id: str):
    if sawit_id != "sawit":
        raise SawitException(name=sawit_id)
    return {
        "sawit_id": sawit_id,
        "name": sawit[sawit_id]
    }
    
    
## override the default exception handlers

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handlers(request, exc: RequestValidationError):
    # return a plain text response with the validation errors
    # message = "Validation errors:"
    # for error in exc.errors():
    #     message += f"\nField: {error['loc']}, Error: {error['msg']}"
    # return PlainTextResponse(message, status_code=400)

    # return a json response with the validation errors
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation errors",
            "details": exc.errors(),
            "body": exc.body
        }
    )

@app.get("/sawitz/{sawit_id}")
async def read_sawitz(sawit_id: int):
    if sawit_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"sawit_id": sawit_id}


## reuse fastapis exception handlers
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}