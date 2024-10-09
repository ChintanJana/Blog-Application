from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    post_id : int
    title: str
    content: str
    user_id: int
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title : Optional[str]
    content : Optional[str]
    published : Optional[bool]