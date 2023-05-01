import os
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile, APIRouter

router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # https://www.slingacademy.com/article/fastapi-how-to-upload-and-validate-files/
    validate_file(file)

    upload_dir = os.path.join(os.getcwd(), "uploads")
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)
    print(dest)

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


def validate_file(file: UploadFile):
    # Get the file size (in bytes)
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    file.seek(0)

    if file_size > 2 * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only upload Images")
