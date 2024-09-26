from pydantic import BaseModel

class PostBase(BaseModel):
    post_id : int
    title: str
    content: str
    user_id: int
    published: bool = False