from __future__ import annotations

import attrs

from sqlalchemy.orm import Session

from db.models.applications import Application
from schemas.applications import UpdateApplicationSchema



@attrs.define
class ApplicationService:
    session: Session
    
    def create(self, user_id: int, job_post_id: int, preference_level: str | None = None, current_location_id: int | None = None) -> Application:
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
        application = self.session.get(Application, application_id)
        if not application and raise_not_found:
            raise ValueError(f"Application with id {application_id} not found")
        return application
    
    def get_applications_for_user(self, user_id: int) -> list[Application]:
        return self.session.query(Application).filter(Application.user_id == user_id).all()
    
    def update_application(self, application_id: int, payload: UpdateApplicationSchema) -> Application:
        application = self.get_application_by_id(application_id)
        
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(application, field, value)
        self.session.commit()
        return application
    