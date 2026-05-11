import attrs

from sqlalchemy.orm import Session

from db.daos.user_profile_dao import UserProfileDAO


@attrs.define
class UserProfileService:
    session: Session
    user_profile_dao: UserProfileDAO

    def create_new_user(self):
        pass
