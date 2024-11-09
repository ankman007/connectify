from fastapi import APIRouter
from app.models.auth import Auth
from app.schemas.auth import AuthResponse, SignUp, Login

router = APIRouter()

# user sign up
@router.post('/sign-up', response_model=AuthResponse)
async def sign_up(user: SignUp): 
    print(Auth.sign_up(user))
    return Auth.sign_up(user)

# user login
@router.post('/login', response_model=AuthResponse)
async def login(user: Login):
    print(Auth.login(user))
    return Auth.login(user)

