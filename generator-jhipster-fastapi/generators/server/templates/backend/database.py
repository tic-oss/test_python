<%_ if (postgresql){  _%>
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
<%_ } _%>

<%_ if (mongodb){  _%>
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB = os.getenv("MONGO_DB")
MONGO_MSG_COLLECTION = os.getenv("MONGO_MSG_COLLECTION")


DB = MONGO_DB 
MSG_COLLECTION = MONGO_MSG_COLLECTION
<%_ } _%>