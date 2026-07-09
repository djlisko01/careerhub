"""Service layer for managing user profiles in the CareerHub database.

This module provides the ``UserService`` class, which encapsulates all database
operations related to user profile lifecycle management, including creation,
retrieval, updates, and activation state changes.

It also defines ``InactiveUserError``, a custom exception raised when a mutation
is attempted on an inactive user profile.

Classes:
    UserService: Database service for CRUD and lifecycle operations on user profiles.

Exceptions:
    InactiveUserError: Raised when a mutation is attempted on an inactive user profile.
"""

from __future__ import annotations

import attrs

from sqlalchemy.orm import Session
from datetime import datetime, timezone as tz

from db.models import UserProfile, Principal
from db.models.principals import PrincipalType

import schemas.users as user_schemas


class InactiveUserError(Exception):
    """Exception raised when attempting to perform an action on an inactive user profile."""

    pass


@attrs.define
class UserService:
    """Database service for managing ``UserProfile`` records.

    Provides methods for creating, retrieving, updating, and toggling the
    activation state of user profiles. Each instance is bound to a SQLAlchemy
    ``Session``, which is used to execute all database operations.

    Attributes:
        db (Session): The SQLAlchemy database session used to execute queries
            and persist changes.

    Public Methods:
        create_user_profile: Create a new user profile and its associated principal.
        get_user_profile_by_id: Fetch a user profile by its primary key ID.
        update_user_profile: Update fields on an existing active user profile.
        deactivate_user: Mark a user profile as inactive.
        reactivate_user: Restore a previously deactivated user profile to active.
    """

    db: Session

    def deactivate_user(self, user_id: int) -> None:
        """Deactivate a user profile by setting its `active` field to `False`.

        Args:
            user_id: The primary key ID of the user profile to deactivate.

        Raises:
            NoResultFound: If no user profile is found with the given `user_id`.
        """
        user_profile = self.db.query(UserProfile).filter(UserProfile.id == user_id).one()

        if not user_profile.active:
            return 

        user_profile.active = False
        user_profile.principal.soft_delete()
        self.db.commit()

    def reactivate_user(self, user_id: int) -> None:
        """Reactivate a user profile by setting its `active` field to `True`.

        Args:
            user_id: The primary key ID of the user profile to reactivate.

        Raises:
            NoResultFound: If no user profile is found with the given `user_id`.
        """
        user_profile = self.db.query(UserProfile).filter(UserProfile.id == user_id).one()

        if user_profile.active:
            return

        user_profile.active = True
        user_profile.principal.updated_at = datetime.now(tz=tz.utc)
        user_profile.principal.deleted_at = None
        self.db.commit()

    def update_user_profile(self, user_id: int, **kwargs) -> UserProfile:
        """Update a user profile with the given data.

        Args:
            user_id: The primary key ID of the user profile to update.
            **kwargs: The fields to update, passed as keyword arguments. Only fields
                defined in `UserUpdateSchema` will be updated.

        Returns:
            The updated `UserProfile` model instance.

        Raises:
            NoResultFound: If no user profile is found with the given `user_id`.
            InactiveUserError: If the user profile with the given `user_id` is inactive.
            ValidationError: If any of the fields in `kwargs` are not valid according to
                `UserUpdateSchema`.
        """
        payload = user_schemas.UserUpdateSchema.model_validate(kwargs)

        user = self.db.query(UserProfile).filter(UserProfile.id == user_id).one()

        if not user.active:
            raise InactiveUserError("Cannot update an inactive user profile.")

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        user.principal.updated_at = datetime.now(tz=tz.utc)
        self.db.commit()
        return user

    def create_user_profile(
        self, user_data: user_schemas.UserCreateSchema
    ) -> UserProfile:
        """Create a new user profile with the given data"""
        principal = Principal(principal_type=PrincipalType.HUMAN)

        # Add principal to generate an fk ID for the user profile
        self.db.add(principal)
        self.db.flush()

        # Create the user profile with the generated principal ID
        user_profile = UserProfile(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            linkedin_url=user_data.linkedin_url,
            github_url=user_data.github_url,
            principal_id=principal.id,
        )
        self.db.add(user_profile)
        self.db.flush()
        self.db.commit()

        return user_profile

    def get_user_profile_by_id(
        self, user_id: int, raise_err: bool = True
    ) -> UserProfile | None:
        """Fetches a user profile by its primary key ID.

        Args:
            user_id: The primary key ID of the user profile to fetch.
            raise_err: If True, raises an exception if the user profile is not found.

        Returns:
            The `UserProfile` model instance if found, or `None` if not found and
            `raise_err` is `False`.

        Raises:
            sqlalchemy.orm.exc.NoResultFound: If `raise_err` is `True` and no
                user profile is found with the given `user_id`.
        """

        if raise_err:
            return self.db.query(UserProfile).filter(UserProfile.id == user_id).one()

        return (
            self.db.query(UserProfile)
            .filter(UserProfile.id == user_id)
            .one_or_none()
        )
        
    def get_user_profile_by_email(self, email: str, raise_err: bool = True) -> UserProfile | None:
        """Fetches a user profile by its email address.

        Args:
            email: The email address of the user profile to fetch.
            raise_err: If True, raises an exception if the user profile is not found.

        Returns:
            The `UserProfile` model instance if found, or `None` if not found and
            `raise_err` is `False`.

        Raises:
            sqlalchemy.orm.exc.NoResultFound: If `raise_err` is `True` and no
                user profile is found with the given `email`.
        """
        
        # Mock User for now
        user = UserProfile(
            id=1,
            first_name="Mock",
            last_name="User",
            email=email,
            active=True,
            linkedin_url=None,
            github_url=None,
            principal_id=1,
        )
        return user

        # if raise_err:
        #     return self.db.query(UserProfile).filter(UserProfile.email == email).one()

        # return (
        #     self.db.query(UserProfile)
        #     .filter(UserProfile.email == email)
        #     .one_or_none()
        # )   
