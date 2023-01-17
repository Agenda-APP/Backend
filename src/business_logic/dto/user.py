from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class UserDTO:
    email: str
    password: str
    name: str | None = None
    photo: UploadFile | None = None
