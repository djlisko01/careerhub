import attrs
from attr import Factory

from sqlalchemy.orm import Session

from db.models import UserProfile

import schemas.users as user_schemas


@attrs.define
class UserService:
    db: Session

    def create_user_profile(
        self, user_data: user_schemas.UserCreateSchema
    ) -> user_schemas.UserReponseSchema:
        pass

    def get_user_profile_by_id(
        self, user_id: int, raise_err: bool = True
    ) -> user_schemas.UserReponseSchema | None:
        """Fetches a user profile by its primary key ID.

        Args:
            user_id: The primary key ID of the user profile to fetch.
            raise_err: If True, raises an exception if the user profile is not found.

        Returns:
            user_schema: A `UserReponseSchema` instance if the user profile is found,
                or` None` if not found and `raise_err` is `False`.

        Raises:
            sqlalchemy.orm.exc.NoResultFound: If `raise_err` is `True` and no
                user profile is found with the given `user_id`.
        """

        if raise_err:
            user_profile = (
                self.db.query(UserProfile).filter(UserProfile.id == user_id).one()
            )
        else:
            user_profile = (
                self.db.query(UserProfile)
                .filter(UserProfile.id == user_id)
                .one_or_none()
            )

        return (
            user_schemas.UserReponseSchema.model_validate(user_profile)
            if user_profile
            else None
        )
