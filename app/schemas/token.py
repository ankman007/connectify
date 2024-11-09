from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    id: int
    email: str
    exp: int
    