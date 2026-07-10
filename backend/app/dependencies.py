from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from jwt import ExpiredSignatureError, InvalidTokenError, InvalidSignatureError

from sqlalchemy.orm import Session

from db.models.users import UserProfile

from db.services.user_profile_service import UserService
from db.connectors import sqlalchemy_conn

from security.authentication import decode_access_token

AuthException = HTTPException(status_code=401, detail="Could not validate credentials")

# Singleton to use accross the app
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TokenDependency = Annotated[str, Depends(oauth2_scheme)]

def get_user_service(db: Session = Depends(sqlalchemy_conn.get_db)) -> UserService:
    return UserService(db)


def get_current_user(access_token: TokenDependency, user_service: UserService = Depends(get_user_service)) -> UserProfile:
    
    try:
        payload = decode_access_token(access_token)
    except (ExpiredSignatureError, InvalidTokenError, InvalidSignatureError):
        raise AuthException
    
    username = payload.get("sub")
    if username is None:
        raise AuthException
    
    user = user_service.get_user_profile_by_email(username, raise_err=False)
    if user is None or not user.active:
        raise AuthException
    
    return user