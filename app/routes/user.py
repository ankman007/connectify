from fastapi import APIRouter
from app.models.user import UserModel
from app.schemas.user import User
from typing import List

router = APIRouter()

@router.get('/{id}', response_model=User)
def get_user(id: int):
    user = UserModel.get_user(id)
    return user 

@router.get('/', response_model=List[User])
def get_users():
    users = UserModel.get_users()
    return users 
