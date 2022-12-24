from pydantic import BaseModel


class CategoryCreation(BaseModel):
    name: str


class CategoryDeletion(BaseModel):
    name: str
