from psycopg2 import DatabaseError
from app.database import get_db_connection
from fastapi import HTTPException
from app.schemas.auth import Login, SignUp, AuthResponse
from psycopg2.extras import RealDictCursor
import bcrypt
from app.utils import hash_password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
                    hashed_password = pwd_context.hash(user.password)
                    cursor.execute(query, (user.email, user.username, hashed_password))
                    registered_user = cursor.fetchone()
                    conn.commit()
                    if registered_user is None:
                        raise HTTPException(status_code=404, detail="Error registering user.")

                    return AuthResponse(**registered_user)
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
    @classmethod
    def login(cls, user: Login):
        try:
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
                    
                    print(f"Entered password: {user.password}")  
                    print(f"Stored password hash: {stored_password}")  

                    # Ensure no hidden characters or mismatches
                    is_correct = pwd_context.verify(user.password, stored_password)
                    print(f"Password match result: {is_correct}")
                    
                    if not pwd_context.verify(user.password, stored_password):
                        raise HTTPException(status_code=401, detail="Incorrect password.")
                    
                    return AuthResponse(**logged_in_user)
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")