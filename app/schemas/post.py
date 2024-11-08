from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None
    
class PostCreate(Post):
    pass

class PostUpdate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
