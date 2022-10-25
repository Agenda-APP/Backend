import os
from shutil import copyfileobj


def save_photo(photo_instance):
    path = os.path.join('static/photos/', photo_instance.filename)
    with open(path, "wb") as buffer:
        copyfileobj(photo_instance.file, buffer)
