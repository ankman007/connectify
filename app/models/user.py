from psycopg2 import DatabaseError
from app.database import get_db_connection
from fastapi import HTTPException
from app.schemas.user import UserLogin, UserSignUp
from psycopg2.extras import RealDictCursor

class User():
    @classmethod
    def user_signup(cls, user: UserSignUp):
        try:
            query = """
            INSERT INTO users (email, username, password)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) 
            DO UPDATE SET 
                username = EXCLUDED.username,  
                password = EXCLUDED.password   
            RETURNING id, email, username, created_at, password;
            """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, (user.email, user.username, user.password))
                    registered_user = cursor.fetchone()
                    conn.commit()
                    if registered_user is None:
                        raise HTTPException(status_code=404, detail="Error registering user.")
                    registered_user_dict = dict(registered_user)  
                    registered_user_dict.pop('password', None)  

                    return registered_user
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
    @classmethod
    def user_login(cls, user: UserLogin):
        try:
            query = """
            SELECT * FROM users 
            WHERE username = %s AND password = %s
            """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, (user.username, user.password))
                    logged_in_user = cursor.fetchone()
                    if logged_in_user is None:
                        raise HTTPException(status_code=404, detail="User not found.")
                    logged_in_user_dict = dict(logged_in_user)  
                    logged_in_user_dict.pop('password', None)
                    return logged_in_user
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")