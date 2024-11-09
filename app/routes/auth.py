from fastapi import APIRouter, Depends
from app.models.auth import Auth
from app.schemas.auth import SignUp, Login, LoginResponse, SignupResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter()

# user sign up
@router.post('/sign-up', response_model=SignupResponse)
async def sign_up(user: SignUp): 
    return Auth.sign_up(user)

# user login
@router.post('/login', response_model=LoginResponse)
async def login(user: OAuth2PasswordRequestForm = Depends(Auth.login)):
    return user

