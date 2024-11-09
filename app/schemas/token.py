from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    id: Optional[str] = None 
    