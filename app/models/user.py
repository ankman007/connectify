from psycopg2 import DatabaseError
from app.database import get_db_connection
from fastapi import HTTPException
from app.schemas.user import User
from psycopg2.extras import RealDictCursor

class UserModel():
    @classmethod
    def get_user(cls, id: int):
        try:
            query = """
            SELECT id, email, username, created_at, password 
            FROM users 
            WHERE id = %s
            """
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, (id,))
                    user = cursor.fetchone()
                    
                    if user is None:
                        raise HTTPException(status_code=404, detail="User not found.")
                    
                    return User(**user)
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
    @classmethod
    def get_users(cls, limit: int = 10):
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                    SELECT * FROM users
                    LIMIT %s
                    """
                    cursor.execute(query, (limit,))
                    users = cursor.fetchall()
                    return users
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")