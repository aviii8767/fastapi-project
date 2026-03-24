# This file contains All path routes/operation dealing with user 
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, utils
from ..database import engine, get_db

router = APIRouter(
    prefix = '/users',
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Check if user already exists
    user_query = db.query(models.User).filter(models.User.email ==  user.email)

    if user_query.first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail = f"user with email '{user.email}' already exist")


    # Hash the password - user.password, before storing
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) # **to unwind that post data as same above
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id:{id} does not exist")
    return user