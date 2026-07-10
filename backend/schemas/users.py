from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    linkedin_url: str | None = None
    github_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LocalUserCreateSchema(UserCreateSchema):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = None
    last_name: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    active: bool = True
    
    model_config = ConfigDict(from_attributes=True, extra="forbid")