from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection
from psycopg2 import DatabaseError
from loguru import logger
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None

# index 
@app.get('/')
def index():
    return {"message": "Generic Social Media App"}

# get single post
@app.get('/posts/{id}')
def get_post_by_id(id: int):
    try: 
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT * FROM post
                WHERE id = %s
                """
                cursor.execute(query, (id, ))
                post = cursor.fetchone()
                if post is None:
                    raise HTTPException(status_code=404, detail="Post not found in the db.")
                return {"data": post}
            
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# get all posts
@app.get('/posts')
def get_posts_all_posts():
    try: 
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM post
                """
                cursor.execute(query)
                posts = cursor.fetchall()
                return {"data": posts}
            
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    

# publish a post
@app.post('/posts')
def publish_post(post: Post):
    try: 
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                INSERT INTO post (title, content, published, rating)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
                """
                
                cursor.execute(query, (post.title, post.content, post.published, post.rating))
                published_post = cursor.fetchone()
                conn.commit()
                print(published_post)
                if published_post is None:
                    raise HTTPException(status_code=404, detail="Error publishing the post.")
                return {"data": published_post}
            
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    

# update a post
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    try: 
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                UPDATE post
                SET title = %s, content = %s, published = %s, rating = %s
                WHERE id = %s
                RETURNING *;
                """
                cursor.execute(query, (post.title, post.content, post.published, post.rating, id))
                updated_post = cursor.fetchone()
                conn.commit()
                
                if updated_post is None:
                    raise HTTPException(status_code=404, detail="Error publishing the post.")
                else:
                    return {"data": updated_post}
            
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# delete a post
@app.delete('/posts/{id}')
def delete_post(id: int):
    try: 
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                DELETE FROM post
                WHERE id = %s
                """
                cursor.execute(query, (id, ))
                conn.commit()
                return {"message": f"Post with id {id} deleted successfully."}
            
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

