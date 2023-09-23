import pydantic


class User(pydantic.BaseModel):
    id: int
    username: str
    password: str
    created_at: str
    updated_at: str


class Booking(pydantic.BaseModel):
    id: int
    user_id: str
    start_time: str
    end_time: str
    comment: str
