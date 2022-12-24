from sqlalchemy import Column, Integer, String

from database.models.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(120), unique=True)
    password: str = Column(String(120))
    name: str = Column(String(120))
    photo: str | None = Column(String(120), nullable=True)
