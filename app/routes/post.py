from fastapi import APIRouter, Depends, HTTPException
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from typing import List

router = APIRouter()

# get single post
@router.get('/{id}', response_model=PostResponse)
async def get_post(id: int):
    post = Post.get_post(id)
    if post is None:
        raise HTTPException("Post not found.")
    return post

# get all posts
@router.get('/', response_model=List[PostResponse])
async def get_posts():
    posts = Post.get_posts()
    posts_dict = [dict(post) for post in posts]
    return posts_dict

# publish a post
@router.post('/', response_model=PostResponse)
async def create_post(post: PostCreate):
    published_post = Post.create_post(post.model_dump())
    return published_post

# update a post
@router.put('/{id}', response_model=PostResponse)
async def update_post(id: int, post: PostUpdate):
    updated_post = Post.update_post(id, post.model_dump())
    return updated_post

# delete a post
@router.delete('/{id}', status_code=204)
async def delete_post(id: int):
    Post.delete_post(id)
    return

