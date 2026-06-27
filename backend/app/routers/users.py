from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.services.user_profile_service import UserService

from db.connectors import sqlalchemy_conn

from schemas.users import UserCreateSchema, UserReponseSchema

def get_service(db: Session = Depends(sqlalchemy_conn.get_db)) -> UserService:
    return UserService(db)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(new_user: UserCreateSchema, service=Depends(get_service)) -> UserReponseSchema:
    return service.create_user_profile(new_user)