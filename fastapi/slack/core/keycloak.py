from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=KEYCLOAK_URL)