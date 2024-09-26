from fastapi import status, APIRouter
from blog.database import SessionLocal
from blog.schema.posts import PostBase
from blog.database.models.posts import Post

post_router = APIRouter(
    prefix = "/posts",
    tags=["posts"],
    responses={
        401:{"post" : "Not Found"}
    }
)

@post_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase):
    with SessionLocal() as session:
        db_post = Post(**post.model_dump())
        session.add(db_post)
        session.commit()
        return f"Created {repr(db_post)}"


    