# pydantic models for forms

from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str
    
    # forbid extra fields
    model_config = {
        "extra": "forbid"
    }
    
@app.post("/login/")
async def login(
    data: Annotated[FormData, Form()]
):
    return data