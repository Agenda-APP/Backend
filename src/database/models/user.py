from sqlalchemy import Column, Integer, String

from database.models.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Column[Integer] = Column(Integer, primary_key=True)
    email: Column[String] = Column(String(120), unique=True)
    password: Column[String] = Column(String(120))
    name: Column[String] = Column(String(120))
    photo: Column[String] = Column(String(120), nullable=True)
