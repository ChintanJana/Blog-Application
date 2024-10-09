from fastapi import status, APIRouter, HTTPException
from blog.database import SessionLocal
from blog.schema.posts import PostCreate, PostUpdate
from blog.database.models.posts import Post
from sqlalchemy import select, update, delete

post_router = APIRouter(
    prefix = "/posts",
    tags=["posts"],
    responses={
        401:{"post" : "Not Found"}
    }
)

@post_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    with SessionLocal() as session:
        db_post = Post(**post.model_dump())
        session.add(db_post)
        session.commit()
        return f"Created {repr(db_post)}"

@post_router.get("/get/{post_id}", status_code = status.HTTP_200_OK)
async def get_post(post_id: int):
    with SessionLocal() as session:
        stmt = select(Post).where(Post.post_id == post_id)
        result = session.execute(stmt).scalars().all()

        if result is None:
            raise HTTPException(status_code = 404, detail="Post doesn't exist.")
        
        return result
    
@post_router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post : PostUpdate):
    post_id = post.post_id
    with SessionLocal() as session:
        stmt = select(Post.post_id).where(Post.post_id == post_id)
        result = session.execute(stmt).scalars().all()

        if result is None:
            HTTPException(status_code=404, detail="Post doesn't exist.")
        
    
    updated_post = post.model_dump(exclude_unset=True)

    with SessionLocal() as session:
        stmt = update(Post)
        session.execute(stmt, updated_post)
        session.commit()

@post_router.get("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    with SessionLocal() as session:
        try:
            stmt = delete(Post).where(Post.post_id == post_id)
            session.execute(stmt)
        except:
            session.rollback()
            raise
        else:
            session.commit()