from __future__ import annotations

import attrs

from sqlalchemy.orm import Session

from db.models.applications import Application
from schemas.applications import ApplicationResponseSchema


@attrs.define
class ApplicationService:
    session: Session
    
    def create(self, user_id: int, job_post_id: int, preference_level: str | None = None, current_location_id: int | None = None) -> ApplicationResponseSchema:
        application = Application(
            user_id=user_id,
            preference_level=preference_level,
            job_post_id=job_post_id,
            current_location_id=current_location_id,
        )
        self.session.add(application)
        self.session.flush()
        self.session.commit()
        
        return ApplicationResponseSchema.model_validate(application)
        
    