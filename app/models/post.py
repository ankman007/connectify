from psycopg2 import DatabaseError
from app.database import get_db_connection
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from app.schemas.post import PostCreate, PostUpdate

class Post():
    @classmethod
    def get_post(cls, id: int):
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                    SELECT * FROM entry
                    WHERE id = %s
                    """
                    cursor.execute(query, (id, ))
                    post = cursor.fetchone()
                    if post is None:
                        raise HTTPException(status_code=404, detail="Post not found in the db.")
                    return post
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
    @classmethod
    def get_posts(cls):
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                    SELECT * FROM entry
                    """
                    cursor.execute(query)
                    posts = cursor.fetchall()
                    return posts
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
        
    @classmethod
    def create_post(cls, post: PostCreate):
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                    INSERT INTO entry (title, content, published, rating)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *;
                    """
                    print(post)
                    
                    cursor.execute(query, (post['title'], post['content'], post['published'], post['rating']))
                    published_post = cursor.fetchone()
                    conn.commit()
                    if published_post is None:
                        raise HTTPException(status_code=404, detail="Error publishing the post.")
                    return published_post
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
        
    @classmethod
    def update_post(cls, id: int, post: PostUpdate):
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                    UPDATE entry
                    SET title = %s, content = %s, published = %s, rating = %s
                    WHERE id = %s
                    RETURNING *;
                    """
                    cursor.execute(query, (post['title'], post['content'], post['published'], post['rating'], id))
                    updated_post = cursor.fetchone()
                    conn.commit()
                    
                    if updated_post is None:
                        raise HTTPException(status_code=404, detail="Error publishing the post.")
                    else:
                        return updated_post
                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
    @classmethod
    def delete_post(cls, id: int):
        try: 
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    query = """
                    DELETE FROM entry
                    WHERE id = %s
                    """
                    cursor.execute(query, (id, ))
                    conn.commit()
                    if cursor.rowcount == 0: 
                        raise HTTPException(status_code=404, detail="Post not found.")

                
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

