from sqlalchemy import Column, Integer, String, TIMESTAMP , Index
from database import Base

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    writer = Column(String)
    number = Column(Integer)
    published = Column(TIMESTAMP)
