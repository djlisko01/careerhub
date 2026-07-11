from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from db.services.user_profile_service import UserService

from app.dependencies import get_current_user, get_user_service
from security import authentication as authn
from schemas.users import UserResponseSchema


router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(email: str, password: str, user_service: UserService) -> UserResponseSchema:
    user = user_service.get_user_profile_by_email(email, raise_err=False)
    username_password_invalid = "Invalid email or password"
    
    if not user:
        raise HTTPException(status_code=401, detail=username_password_invalid)

    if not authn.verify_password(password, user.password or ""):
        raise HTTPException(status_code=401, detail=username_password_invalid)

    return UserResponseSchema.model_validate(user)
    
    

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> dict:
    user = authenticate_user(form_data.username, form_data.password, user_service)
    access_token = authn.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(current_user: UserResponseSchema = Depends(get_current_user)) -> UserResponseSchema:
    return current_user

    