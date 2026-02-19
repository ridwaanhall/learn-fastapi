# request forms and files

'''
Use File and Form together when you need to receive data and files in
the same request.
'''

from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_files(
    file: Annotated[
        bytes,
        File(description="A file to be uploaded") # add description to the file parameter
    ],
    fileb: Annotated[
        UploadFile,
        File(description="A file to be uploaded") # add description to the file parameter
    ],
    token: Annotated[
        str,
        Form(description="A token to be used as form data") # add description to the form parameter
    ]
):
    return {
        "file_size": len(file),
        "filename": fileb.filename,
        "token": token
    }