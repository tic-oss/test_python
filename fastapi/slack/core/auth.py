import os
from fastapi import HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak.keycloak_openid import KeycloakOpenID
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











