from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, ConfigDict

from db.models.applications import ApplicationStatus, PreferenceLevel


class UpdateApplicationSchema(BaseModel):
    status: ApplicationStatus | None = None
    preference_level: PreferenceLevel | None = None
    job_post_id: int | None = None
    current_location_id: int | None = None
    applied_at: dt.datetime | None = None

    model_config = ConfigDict(extra="forbid")


class ApplicationResponseSchema(BaseModel):
    id: int
    user_id: int
    status: ApplicationStatus
    preference_level: PreferenceLevel | None = None
    job_post_id: int
    current_location_id: int | None = None
    applied_at: dt.datetime | None = None
    updated_at: dt.datetime
    closed_at: dt.datetime | None = None
    
    # Pull from attributes
    model_config = ConfigDict(from_attributes=True)

    
