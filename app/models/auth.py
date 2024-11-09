from psycopg2 import DatabaseError
from app.database import get_db_connection
from fastapi import Depends, HTTPException
from app.schemas.auth import Login, SignUp, LoginResponse, SignupResponse
from psycopg2.extras import RealDictCursor
from app.utils.hashing import hash, verify
from app.utils.oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

class Auth():
    @classmethod
    def sign_up(cls, user: SignUp): 
        try:
            query = """
            INSERT INTO users (email, username, password)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) 
            DO UPDATE SET 
                username = EXCLUDED.username,  
                password = EXCLUDED.password   
            RETURNING id, email, username, created_at;
            """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    hashed_password = hash(user.password)
                    cursor.execute(query, (user.email, user.username, hashed_password))
                    registered_user = cursor.fetchone()
                    conn.commit()
                    if registered_user is None:
                        raise HTTPException(status_code=404, detail="Error registering user.")

                    return SignupResponse(**registered_user)
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
    @classmethod
    def login(cls, user: OAuth2PasswordRequestForm = Depends()):
        try:
            print(user)
            query = """
            SELECT id, email, username, created_at, password 
            FROM users 
            WHERE username = %s
            """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, (user.username,))
                    logged_in_user = cursor.fetchone()
                    
                    if logged_in_user is None:
                        raise HTTPException(status_code=404, detail="User not found.")
                    stored_password = logged_in_user['password']
                    
                    if not verify(user.password, stored_password):
                        raise HTTPException(status_code=401, detail="Incorrect password.")
                    
                    access_token = create_access_token(data={"email": logged_in_user['email'], "id": logged_in_user['id']})
                    
                    return LoginResponse(
                        **logged_in_user,
                        access_token=access_token,
                        token_type="bearer"
                    )
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")