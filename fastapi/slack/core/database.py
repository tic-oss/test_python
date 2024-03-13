from dotenv import load_dotenv
import os

load_dotenv()



DB =  os.getenv("MONGO_DB")
MSG_COLLECTION = os.getenv("MONGO_MSG_COLLECTION")