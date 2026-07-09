from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_user_service

from db.services.user_profile_service import UserService
from schemas.users import UserCreateSchema, UserReponseSchema


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(new_user: UserCreateSchema, service: UserService = Depends(get_user_service)) -> UserReponseSchema:
    return service.create_user_profile(new_user)


@router.get("/me")
def read_current_user(current_user: UserReponseSchema = Depends(get_current_user)) -> UserReponseSchema:
    return current_user


