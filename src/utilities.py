import os
from shutil import copyfileobj

from fastapi import UploadFile


def save_photo(photo_instance: UploadFile) -> str:
    path = os.path.join("static/photos", photo_instance.filename)
    with open(path, "wb") as buffer:
        copyfileobj(photo_instance.file, buffer)
    photo_url = f"localhost/static/photos/{photo_instance.filename}"
    return photo_url
