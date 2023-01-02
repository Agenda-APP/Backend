from pydantic import BaseModel


class CategoryCreation(BaseModel):
    name: str


class Category(BaseModel):
    name: str

    class Config:
        orm_mode = True
