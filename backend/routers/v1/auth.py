from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from backend.core.security import create_access_token
from backend.db.connectors.sqlalchemy_conn import get_db
from backend.db.services.user_profile_service import UserService
from backend.schemas.users import TokenSchema, UserCreateSchema, UserReponseSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix="/", tags=["auth"])


def get_user_service(db=Depends(get_db)) -> UserService:
    """Dependency function to provide a `UserService` instance with a database session."""
    return UserService(db=db)


@router.post("/register", status_code=201)
def register_user(
    user_data: UserCreateSchema, user_service: UserService = Depends(get_user_service)
) -> TokenSchema:
    if user_service.username_exists(user_data.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    user = user_service.create_user_profile(user_data)
    return TokenSchema(access_token=create_access_token(subject=user.id))


@router.post("/login", response_model=TokenSchema, status_code=201)
def get_token(
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
