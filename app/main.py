from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings

# print(settings.database_username)

# models.Base.metadata.create_all(bind=engine) this is now no more needed due to alembic
# This command told sqlalchemy to run the create statement so that it will generate all tables when it first started up


app = FastAPI()

origins = ["https://www.google.com", "https://www.youtube.com"]
#origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)# i want to include post.routers
app.include_router(user.router)# if we change sequence here that also reflect in documentation
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my api-world!! - by Avishkar Gaware"}
