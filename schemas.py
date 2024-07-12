from pydantic import BaseModel

class BooksBase(BaseModel):
    name: str
    writer: str
    number: int
    published: str

    class Config:
        from_attributes = True