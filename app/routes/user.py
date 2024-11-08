from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.schemas.user import UserResponse, UserSignUp, UserLogin
from typing import List

router = APIRouter()

# user sign up
@router.post('/sign-up', response_model=UserResponse)
async def sign_up(user: UserSignUp):
    return User.user_signup(user)

# user login
@router.post('/login', response_model=UserResponse)
async def login(user: UserLogin):
    print(User.user_login(user))

    return User.user_login(user)

