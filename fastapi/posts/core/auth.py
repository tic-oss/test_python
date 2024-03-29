#/auth.py
import os
from fastapi import HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID # pip require python-keycloak
# from config import settings
from fastapi import Security, HTTPException, status
 
KC_SERVER_URL = os.getenv('KC_SERVER_URL')
KC_AUTH_URL   = os.getenv('KC_AUTH_URL')
KC_TOKEN_URL  = os.getenv('KC_TOKEN_URL')
KC_REALM_NAME = os.getenv('KC_REALM_NAME')
KC_CLIENT_ID  = os.getenv('KC_CLIENT_ID')
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET')
 
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl = KC_AUTH_URL,
    tokenUrl = KC_TOKEN_URL
)
 
# This actually does the auth checks
# client_secret_key is not mandatory if the client is public on keycloak
keycloak_openid = KeycloakOpenID(
    server_url = KC_SERVER_URL,
    client_id = KC_CLIENT_ID,
    realm_name = KC_REALM_NAME,
    client_secret_key = KC_CLIENT_SECRET,
    verify=True
)
 
 
def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )
 
# Get the payload/token from keycloak and vaildate it
def get_auth(token: str = Security(oauth2_scheme)) -> dict:
    try:
        introspection_result = keycloak_openid.introspect(token)
        if not introspection_result.get('active'):
            raise_unauthorized_exception("Token is not active")
            
        return keycloak_openid.decode_token(
            token,
            key= get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
    except Exception as e:
        raise_unauthorized_exception(str(e))
    
def raise_unauthorized_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )











# import logging

# from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from fastapi.middleware.cors import CORSMiddleware
# import os
# # Keycloak setup
# from keycloak import KeycloakOpenID



# keycloak_openid = KeycloakOpenID(
#     server_url=os.getenv("KC_SERVER_URL"),
#     # client_id=os.getenv("KC_CLIENT_ID"), web_app [public client], private clinet []
#     realm_name=os.getenv("KC_REALM_NAME"),
#     verify=True
# )
# router = APIRouter(
#     prefix='/posts',
#     tags=['Posts']
# )
# app = FastAPI()

# oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl=os.getenv("KC_AUTH_URL"), tokenUrl=os.getenv("KC_TOKEN_URL"))


# async def get_auth(token: str = Depends(oauth2_scheme)):
#     print(os.getenv("KC_REALM_NAME"))
#     try:
#         KEYCLOAK_PUBLIC_KEY = (
          
#             "-----BEGIN PUBLIC KEY-----\n"
#             + keycloak_openid.public_key()
#             + "\n-----END PUBLIC KEY-----"
#         )
#         # this only does the decode of tocken, 
#         return keycloak_openid.decode_token(
#             token,
#             key=KEYCLOAK_PUBLIC_KEY,
#             options={"verify_signature": True, "verify_aud": False, "exp": True},
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials ||" + e ,
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# @router.get("/user")
# async def get_user():
#     logging.info("Log relevant information here")
#     return "uhfuihf"
