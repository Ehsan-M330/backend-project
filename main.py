from fastapi import FastAPI, Depends
import models, schemas
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from faker import Faker

app=FastAPI()
faker=Faker()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# db = next(get_db())
# for _ in range(1000):
#     fake_book = models.Books(
#         name=faker.text(max_nb_chars=20),
#         writer=faker.name(),
#         number=faker.random_int(min=1, max=10000),
#         published=faker.date_time_this_decade()
#     )
#     db.add(fake_book)
# db.commit()
# db.close()

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
    