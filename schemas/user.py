from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    name: str
    email: str


class UserResponseModel(BaseModel):
    id: int
    username: str
    name: str
    email: str
    class Config:
        orm_mode= True
