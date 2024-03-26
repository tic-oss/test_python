from fastapi.security import OAuth2PasswordBearer
import os

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=KEYCLOAK_URL)