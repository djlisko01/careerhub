from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from core.security import create_access_token, decode_access_token
from db.connectors.sqlalchemy_conn import get_db
from db.services.user_profile_service import UserService
from schemas.users import TokenSchema, UserCreateSchema, UserReponseSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(tags=["auth"])


def get_user_service(db=Depends(get_db)) -> UserService:
    """Dependency function to provide a `UserService` instance with a database session."""
    return UserService(db=db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> UserReponseSchema:
    """Dependency function to retrieve the current authenticated user based on the provided token."""
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

    user = user_service.get_user_profile_by_id(int(user_id), raise_err=False)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/register", status_code=201)
def register_user(
    user_data: UserCreateSchema, user_service: UserService = Depends(get_user_service)
) -> TokenSchema:
    if user_service.username_exists(user_data.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    user = user_service.create_user_profile(user_data)
    return TokenSchema(access_token=create_access_token(subject=user.id))


@router.post("/login", response_model=TokenSchema, status_code=201)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> TokenSchema:
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenSchema(access_token=create_access_token(subject=user.id))


@router.get("/me", response_model=UserReponseSchema)
def get_me(current_user: UserReponseSchema = Depends(get_current_user)):
    return current_user
