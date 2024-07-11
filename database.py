from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL='postgresql://postgres:admin@localhost:5432/database'

engine=create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False ,autoflush=False ,bind=engine)

Base = declarative_base()