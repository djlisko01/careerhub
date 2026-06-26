from __future__ import annotations

import attrs

from sqlalchemy.orm import Session

from db.models.applications import Application
from schemas.applications import UpdateApplicationSchema



@attrs.define
class ApplicationService:
    """Service for managing job applications."""

    session: Session

    def create(self, user_id: int, job_post_id: int, preference_level: str | None = None, current_location_id: int | None = None) -> Application:
        """Create and persist a new job application for a user.

        Args:
            user_id: ID of the user submitting the application.
            job_post_id: ID of the job post being applied to.
            preference_level: Optional preference ranking for this application.
            current_location_id: Optional ID of the user's current location.

        Returns:
            The newly created Application instance.
        """
        application = Application(
            user_id=user_id,
            preference_level=preference_level,
            job_post_id=job_post_id,
            current_location_id=current_location_id,
        )
        self.session.add(application)
        self.session.flush()
        self.session.commit()

        return application

    def get_application_by_id(self, application_id: int, raise_not_found: bool = True) -> Application | None:
        """Fetch a single application by its primary key.

        Args:
            application_id: Primary key of the application to retrieve.
            raise_not_found: If True, raises ValueError when the application does not exist.

        Returns:
            The matching Application, or None if not found and raise_not_found is False.

        Raises:
            ValueError: If no application exists with the given ID and raise_not_found is True.
        """
        application = self.session.get(Application, application_id)
        if not application and raise_not_found:
            raise ValueError(f"Application with id {application_id} not found")
        return application

    def get_applications_for_user(self, user_id: int) -> list[Application]:
        """Return all non-deleted applications belonging to a user.

        Args:
            user_id: ID of the user whose applications to retrieve.

        Returns:
            List of Application instances that have not been soft-deleted.
        """
        return (
            self.session.query(Application)
            .filter(Application.user_id == user_id, Application.deleted_at.is_(None))
            .all()
        )

    def update_application(self, application_id: int, payload: UpdateApplicationSchema) -> Application:
        """Apply a partial update to an existing application.

        Args:
            application_id: ID of the application to update.
            payload: Schema containing only the fields to change.

        Returns:
            The updated Application instance.
        """
        application = self.get_application_by_id(application_id)

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(application, field, value)
        self.session.commit()
        return application

    def delete(self, application_id: int) -> Application:
        """Soft-delete an application so it is excluded from active queries.

        Args:
            application_id: ID of the application to delete.

        Returns:
            The soft-deleted Application instance.
        """
        application = self.get_application_by_id(application_id)
        application.soft_delete()
        self.session.commit()
        return application
    