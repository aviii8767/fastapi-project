from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings

# print(settings.database_username)

# models.Base.metadata.create_all(bind=engine) this is now no more needed due to alembic
# This command told sqlalchemy to run the create statement so that it will generate all tables when it first started up


app = FastAPI()

app.include_router(post.router)# i want to include post.routers
app.include_router(user.router)# if we change sequence here that also reflect in documentation
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my api- by Avishkar Gaware"}
