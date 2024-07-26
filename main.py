from fastapi import FastAPI, Depends
import models, schemas
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

app=FastAPI()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/getbooks')
def get_books(db:Session=Depends(get_db)):
    return db.query(models.Books).limit(1000).all()

@app.get('/getbook/{book_name}')
def get_book(book_name:str,db:Session=Depends(get_db)):
   # ORM query
    writer_query = db.query(models.Books.writer).filter(models.Books.name == book_name).limit(1)
    # Capture the SQL string for the query
    query_str = str(writer_query.statement.compile(compile_kwargs={"literal_binds": True}))
    
    # Capture the execution plan using raw SQL
    explain_query = text("EXPLAIN ANALYZE " + query_str)
    execution_plan = db.execute(explain_query).fetchall()
    
    # Execute the original ORM query
    writer = writer_query.scalar()
    
    # Convert the execution plan to a list of strings
    execution_plan_lines = [line[0] for line in execution_plan]
    
    # Log the execution plan
    logging.info("Execution Plan for query:")
    for line in execution_plan_lines:
        logging.info(line)
    
    return {"writer": writer, "execution_plan": execution_plan_lines}

@app.post('/addbook')
async def add_book(book:schemas.BooksBase, db:Session=Depends(get_db)):
    db_book=models.Books(name=book.name,writer=book.writer,number=book.number,published=book.published)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {}
    