from fastapi import APIRouter, HTTPException
from loguru import logger
from psycopg2 import DatabaseError
from app.database import get_db_connection
from psycopg2.extras import RealDictCursor
from app.models.post import Post

router = APIRouter()

# get single post
@router.get('/{id}')
def get_post(id: int):
    post = Post.get_post(id)
    if post is None:
        raise HTTPException("Post not found.")
    return post

# get all posts
@router.get('/')
def get_posts():
    posts = Post.get_posts()
    return posts    

# publish a post
@router.post('/')
def create_post(post: Post):
    published_post = Post.create_post(post)
    return published_post

# update a post
@router.put('/{id}')
def update_post(id: int, post: Post):
    updated_post = Post.update_post(id, post)
    return updated_post

# delete a post
@router.delete('/{id}')
def delete_post(id: int):
    return Post.delete_post(id)

