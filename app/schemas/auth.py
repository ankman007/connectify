from pydantic import BaseModel, EmailStr
from datetime import datetime

class Auth(BaseModel):
    username: str
    password: str

class Login(Auth):
    pass

class SignUp(Auth):
    email: EmailStr
    
class AuthResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime 

