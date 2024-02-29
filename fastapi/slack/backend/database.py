from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB = os.getenv("MONGO_DB")
MONGO_MSG_COLLECTION = os.getenv("MONGO_MSG_COLLECTION")


DB = MONGO_DB 
MSG_COLLECTION = MONGO_MSG_COLLECTION