from pydantic import BaseModel
from datetime import datetime

class BooksBase(BaseModel):
    name: str
    writer: str
    number: int
    published: datetime

    class Config:
        from_attributes = True