from pydantic import BaseModel

class BooksBase(BaseModel):
    id: int
    name: str
    writer: str
    number: int
    published: str
