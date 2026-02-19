# form data
from typing import Annotated

from fastapi import FastAPI, Form

"""
Use Form to declare form data input parameters.
tip
to declare form bodies, you can use Form, which is imported from fastapi.
coz without it the parameters would be interpreted as query parameters or body (JSON) parameters,
and not form data.
"""

app = FastAPI()

@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    login_data = {
        "username": username,
        "password": password
    }
    return login_data