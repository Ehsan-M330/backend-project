from fastapi import FastAPI, Depends
import models, schemas
from database import engine, sessionLocal
from sqlalchemy.orm import Session

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/getbooks')
def get_books(db:Session=Depends(get_db)):
    return db.query(models.Books).all()

@app.post('/addbook')
async def add_book(book:schemas.BooksBase, db:Session=Depends(get_db)):
    db_book=models.Books(name=book.name,writer=book.writer,number=book.number,published=book.published)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {}
    