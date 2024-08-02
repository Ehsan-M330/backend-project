from fastapi import APIRouter, Depends, HTTPException
from typing import List
import app.models as models, app.schemas as schemas
from app.database import engine, sessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import and_, func , text , select
import logging
import math
from fastapi_pagination import Page,add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

router=APIRouter()

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/update_book_number/{book_id}")
def update_book_number(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    try:
        # Start a transaction
        db.begin()

        # Lock the row for update
        book = db.query(models.Books).where(models.Books.id == book_id).with_for_update().first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if book_update.increase:
            book.number += book_update.number
        else:
            if book.number - book_update.number < 0:
                raise HTTPException(status_code=400, detail="Not enough books")
            else:
                book.number -= book_update.number

        db.commit()
        db.refresh(book)
        return book

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/getbooks')
def get_books(db:Session=Depends(get_db)):
    return db.query(models.Books).limit(1000).all()

@router.get('/getbooksbyfilter')
def get_books(page:int=1, size:int =10, min_book_number: int = 1,
    max_book_number: int = 10, db:Session=Depends(get_db)):
    total_data = db.execute(text("SELECT reltuples AS estimated_count FROM pg_class WHERE relname = 'books';")).scalar()
    total_pages=math.ceil(total_data / size)
    
    data = db.query(models.Books).offset(page-1).limit(size).all()
    return {
        "data": data,
        "total_data": total_data,
        "total_pages": total_pages,
    }

@router.get('/getbook/{book_name}')
def get_book(book_name:str,db:Session=Depends(get_db)):
    return db.query(models.Books.writer).filter(models.Books.name == book_name).first()
    
#    # ORM query
#     writer_query = db.query(models.Books.writer).filter(models.Books.name == book_name).limit(1)
#     # Capture the SQL string for the query
#     query_str = str(writer_query.statement.compile(compile_kwargs={"literal_binds": True}))
    
#     # Capture the execution plan using raw SQL
#     explain_query = text("EXPLAIN ANALYZE " + query_str)
#     execution_plan = db.execute(explain_query).fetchall()
    
#     # Execute the original ORM query
#     writer = writer_query.scalar()
    
#     # Convert the execution plan to a list of strings
#     execution_plan_lines = [line[0] for line in execution_plan]
    
#     # Log the execution plan
#     logging.info("Execution Plan for query:")
#     for line in execution_plan_lines:
#         logging.info(line)

#     return {"writer": writer, "execution_plan": execution_plan_lines}

@router.post('/addbook')
async def add_book(book:schemas.BooksBase, db:Session=Depends(get_db)):
    db_book=models.Books(name=book.name,writer=book.writer,number=book.number,published=book.published)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {}
    