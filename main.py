from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None
    
post_db = [
    {'id': 1, 'title': 'First Post', 'content': 'This is the content of the first post.', 'published': True, 'rating': 5},
    {'id': 2, 'title': 'Second Post', 'content': 'Content for the second post goes here.', 'published': False, 'rating': 3},
    {'id': 3, 'title': 'Third Post', 'content': 'Here is the content of the third post.', 'published': True, 'rating': 4}
]

def get_post_by_id(id):
    for post in post_db:
        if post['id'] == id:
            return post 
    return None 

# index 
@app.get('/')
def index():
    return {"message": "Generic Social Media App"}

# get single post
@app.get('/posts/{id}')
def get_posts(id: int):
    post = get_post_by_id(id)
    if post is None:
        return HTTPException(status_code=404, detail="Post not found in the db.")
    return {"message": post}

# get all posts
@app.get('/posts')
def get_posts():
    return {"message": post_db}

# publish a post
@app.post('/posts')
def publish_posts(post: Post):
    try:
        post_db.append(post)
        print("New post_db: ", post_db)
        return {"message": "Posts published successfully"}
    except Exception as e:
        return HTTPException(status_code=404, detail=f"Encountered error when publishing the post: {e}")

# update a post
@app.put('/posts/{id}')
def update_post(id: int, updated_post: Post):        
    for post in post_db:
        if post['id'] == id:
            post.update(updated_post.dict())
            print("New post_db: ", post_db)        
            return {"message": f"Post updated: {updated_post.dict()}"}
        else:
            return HTTPException(status_code=404, detail="Post not found.")

# delete a post
@app.delete('/posts/{id}')
def delete_post(id: int):
    try:
        global post_db
        post_db = [post for post in post_db if post['id'] != id]
        print("New post_db: ", post_db)
        return {"message": "Post deleted"}
    except Exception as e: 
        return HTTPException(status_code=404, detail=f"Encountered error when publishing the post: {e}")
