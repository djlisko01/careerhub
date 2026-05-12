from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    linkedin_url: str | None = None
    github_url: str | None = None


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None


class UserReponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    linkedin_url: str | None = None
    github_url: str | None = None
    active: bool = True
