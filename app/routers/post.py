# This file contains All path routes/operation dealing with post 

from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from .. import models,schemas, oauth2
from ..database import engine, get_db


router = APIRouter(
    prefix = '/posts',
    tags=['Posts']
)



#GET ALL POSTS
#@router.get("/", response_model = List[schemas.Post])
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user),
    Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(Limit)
    print(search)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    return posts

#get user specif or own posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

#CREATE POST
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    # current_user: models.User = Depends(oauth2.get_current_user)):


    # cursor.execute("""INSERT INTO posts(title,content,published) 
    #                VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    print("current user id *************------->",current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # **to unwind that post data as same above
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# GET INDIVIDUAL POST
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",str(id))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} was not found")
    
    return post

# To get owner specific individual post, add following snippt after above if condition
"""
if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to perform this action"
        )
"""

#DELETE POST
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # due to above current_user only authorized person can delete
    # SQL code
    # cursor.execute("""DELETE FROM posts where id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #SQLAlchemy code
    post_queryObj = db.query(models.Post).filter(models.Post.id == id)
    post = post_queryObj.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to perform this action"
        )
    post_queryObj.delete(synchronize_session = False)
    db.commit()



# UPDATE POST
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
        # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) # it only stores the query
    post = post_query.first() # it runs the query
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to perform this action"
        )
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    return post_query.first()