from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from app.dependencies import get_current_user, get_user_service

from db.services.user_profile_service import UserService
from schemas.users import LocalUserCreateSchema, UserResponseSchema


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(new_user: LocalUserCreateSchema, service: UserService = Depends(get_user_service)) -> UserResponseSchema:
    
    user_exist = service.get_user_profile_by_email(new_user.email, raise_err=False)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    
    user = service.create_user_profile(new_user)
    return UserResponseSchema.model_validate(user)


@router.get("/me")
def read_current_user(current_user: UserResponseSchema = Depends(get_current_user)) -> UserResponseSchema:
    return current_user


