from fastapi import status, APIRouter, HTTPException
from blog.database import SessionLocal
from blog.schema.users import UserBase
from blog.database.models.users import User
from sqlalchemy import select
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

@user_router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase):
    with SessionLocal() as session:
        db_user = session.get(User, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update the fields
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)

        session.commit()
        return f"Updated {repr(db_user)}"