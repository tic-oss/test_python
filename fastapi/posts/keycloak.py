from fastapi.security import OAuth2PasswordBearer

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8080/realms/djangorealm/protocol/openid-connect/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8080/realms/python/protocol/openid-connect/token")
                                     #"http://localhost:8080/realms/python/protocol/openid-connect/token")

                                     #"http://localhost:8080/realms/djangorealm/protocol/openid-connect/token")