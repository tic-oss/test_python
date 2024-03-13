from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl= os.getenv("KEYCLOAK_URL"))
                                     
                                 

                              