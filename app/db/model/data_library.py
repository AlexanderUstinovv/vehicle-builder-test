from sqlalchemy import Column
from sqlalchemy import String

from .base import BaseModel


class Function(BaseModel):
    __tablename__ = "base_function"

    name = Column(String(255))
