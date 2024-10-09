from fastapi import status, APIRouter, HTTPException
from blog.database import SessionLocal
from blog.schema.users import UserBase
from blog.database.models.users import User
from sqlalchemy import select, update, delete 

user_router = APIRouter(
    prefix = "/users",
    tags=["users"],
    responses={
        401:{"user" : "Not Found"}
    }
)

@user_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase):
    with SessionLocal() as session:
        db_user = User(**user.model_dump())

        session.add(db_user)
        session.commit()
        return f"Created {repr(db_user)}"
    
@user_router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    with SessionLocal() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = session.execute(stmt)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result.scalars().all()

@user_router.put("/update", status_code=status.HTTP_200_OK)
async def update_post(user : UserBase):
    user_id = user.user_id
    with SessionLocal() as session:
        stmt = select(User.user_id).where(User.user_id == user_id)
        result = session.execute(stmt).scalars().all()

        if result is None:
            HTTPException(status_code=404, detail="Post doesn't exist.")
        
    
    updated_post = user.model_dump(exclude_unset=True)

    with SessionLocal() as session:
        stmt = update(User)
        session.execute(stmt, updated_post)
        session.commit()

@user_router.get("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(user_id: int):
    with SessionLocal() as session:
        try:
            stmt = delete(User).where(User.user_id == user_id)
            session.execute(stmt)
        except:
            session.rollback()
            raise
        else:
            session.commit()