import pydantic
from pydantic.fields import Field


class User(pydantic.BaseModel):
    id: int = Field(ge=0)
    username: str
    password: str
    created_at: str
    updated_at: str


class Booking(pydantic.BaseModel):
    id: int = Field(ge=0)
    user_id: int = Field(ge=0)
    start_time: str
    end_time: str
    comment: str
