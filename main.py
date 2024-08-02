from fastapi import FastAPI, APIRouter, Depends
import app.models as models
from app.database import engine, sessionLocal
import logging
from fastapi_pagination import add_pagination
from app.routers import book_routes

models.Base.metadata.create_all(bind=engine)
app=FastAPI()
add_pagination(app)
app.include_router(book_routes.router)

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

    