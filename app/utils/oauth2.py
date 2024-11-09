import jwt 
from app.schemas.token import Token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

from app.models.user import UserModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
    
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def verify_access_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        return Token(id=id, email=payload.get("email"), exp=payload.get("exp"))

    except jwt.PyJWTError: 
        raise credentials_exception
    
    except jwt.ExpiredSignatureError:
        raise credentials_exception

        
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)
    if not token_data.id:
        raise credentials_exception
    
    user = UserModel.get_user(token_data.id)
    if user is None:
        raise credentials_exception
    
    return user
