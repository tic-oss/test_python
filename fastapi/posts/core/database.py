from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker 
import os




# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine('postgresql://postgres:pass123@localhost/python')


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db = None

def get_database():
    return db
# Function to get a database session
def get_db():
    global db
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # Handle database connection errors
        print("An error occurred while connecting to the database:", e)
        raise
    finally:
        # Close the session when done
        db.close()