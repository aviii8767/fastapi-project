from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth
from .config import settings

# print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)# i want to include post.routers
app.include_router(user.router)# if we change sequence here that also reflect in documentation
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my api"}
