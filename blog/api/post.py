from fastapi import status, APIRouter, HTTPException
from blog.database import SessionLocal
from blog.schema.posts import PostBase
from blog.database.models.posts import Post
from sqlalchemy import select

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

@post_router.get("/get/{post_id}", status_code = status.HTTP_200_OK)
async def get_post(post_id: int):
    with SessionLocal() as session:
        stmt = select(Post).where(Post.post_id == post_id)
        result = session.execute(stmt)

        if result is None:
            raise HTTPException(status_code = 404, detail="Post doesn't exist.")
        
        return result.scalars().all()
    
