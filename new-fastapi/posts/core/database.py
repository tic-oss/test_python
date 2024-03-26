from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.info("Database connection established.")
    finally:
        db.close()
        logger.info("Database connection closed.")