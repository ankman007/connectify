from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    password: str

class UserLogin(User):
    pass

class UserSignUp(User):
    email: str
    
class UserResponse(UserSignUp):
    id: int
    created_at: datetime
    
    # class Config:
    #     orm_mode = True
    #     fields = {'password': {'exclude': True}}
