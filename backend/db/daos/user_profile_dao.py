import attrs
from sqlalchemy.orm import Session


@attrs.define
class UserProfileDao:
    session: Session

    def create_new_user(self):
        pass

    def get_user_by_id(self, user_id: int):
        pass

    def update_user_profile(self, user_id: int, **kwargs):
        pass
