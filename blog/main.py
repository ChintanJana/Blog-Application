from fastapi import FastAPI
from blog.database import Base, engine
from blog.api.users import user_router
from blog.api.post import post_router

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
async def root_route():
    return {"data" : "main.py in blog"}



app.include_router(post_router)
app.include_router(user_router)

