from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from schemas.users import UserReponseSchema

from db.services.user_profile_service import UserService
from db.connectors import sqlalchemy_conn

from security.authentication import decode_access_token, AuthenticationError

# Singleton to use accross the app
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenDependency = Annotated[str, Depends(oauth2_scheme)]

def get_user_service(db: Session = Depends(sqlalchemy_conn.get_db)) -> UserService:
    return UserService(db)


def get_current_user(access_token: TokenDependency):
    payload = decode_access_token(access_token)
    username = payload.get("sub")
    
    if username is None:
        raise AuthenticationError("Could not validate credentials")
    
    return UserReponseSchema(
        id=payload.get("id", 1),
        first_name=payload.get("first_name", "John"),
        last_name=payload.get("last_name", "Doe"),
        active=payload.get("active", True)
    )