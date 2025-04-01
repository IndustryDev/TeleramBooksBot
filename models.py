
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    description: str
    rating: float
    genre: str
    author: str
    cover: str
    year: int
    price: int
    website: str
