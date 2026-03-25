from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
# format for post create user input
class PostCreate(PostBase):
    pass

#this is output format for response
class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool <-- these three comes by extending PostBase class
    
    created_at: datetime
    owner_id: int
    owner: User # returns pydantic model User


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    #id: Optional[str] = None
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir:Literal[0, 1]
    #direction of vote