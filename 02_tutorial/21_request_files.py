# rquest files

'''
Use File, bytes, and UploadFile to declare files to be uploaded in
the request, sent as form data.
'''

from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/file/")
async def create_file(
    file: Annotated[
        bytes | None, # add None if the file is optional
        File( # define file parameters
            description="A file to be uploaded" # add description to the file parameter
        )
    ]
):
    if file is None:
        return {"file_size": 0}
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile | None = None # add None if the file is optional
):
    if file is None:
        return {"filename": None}
    else:
        return {"filename": file.filename}
    
@app.post("/uploadfile-desc/")
async def create_upload_desc(
    file: Annotated[
        UploadFile,
        File(description="Multiple files to be uploaded") # add description to the file parameter
    ]
):
    return {"filename": file.filename}


## multiple file uploads
from fastapi.responses import HTMLResponse

@app.post("/files/")
async def create_files(
    files: Annotated[
        list[bytes],
        File(description="Multiple files to be uploaded") # add description to the file parameter
    ]
):
    sizes = {
        "file_sizes": [len(file) for file in files]
    }
    return sizes

@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile]
):
    filenames = {
        "filenames": [file.filename for file in files]
    }
    return filenames

@app.post("/uploadfiles-desc/")
async def create_upload_files_desc(
    files: Annotated[
        list[UploadFile],
        File(description="Multiple files to be uploaded") # add description to the file parameter
    ]
):
    filenames = {
        "filenames": [file.filename for file in files]
    }
    return filenames

@app.get("/")
async def main():
    content = """
<body>
    <form action="/files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
    </form>
        <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
    </form>
</body>
    """
    return HTMLResponse(content=content)