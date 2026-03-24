from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


#Database connection
while True:

    try:
        conn = psycopg2.connect(host='localhost' ,database='fastapi', user='postgres',
                                password= 'Adminpass@123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was sucessful!")
        break
    except Exception as error:
        print("Connecting to DB failed")
        print("Error: ", error)
        time.sleep(2)




my_posts = [
    {
        "title": "tile of post 1", 
        "content": "content of post 1", 
        "id": 1
    }, 
    {
        "title": "favorite foods", 
        "content": "I like pizza",
        "id": 2
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts) :
        if p["id"] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "Welcome to my api"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    #we have to pass specific model from model.py for the table we want to query
    posts = db.query(models.Post).all() #like .all method need to to run the query
    return {"data": posts}


#GET ALL POSTS
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data":posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']} content: {payload['content']}"}



#CREATE POST
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # post: Post
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000000000)
    # my_posts.append(post_dict)
    # return {"data": post_dict}

    # cursor.execute("""INSERT INTO posts(title,content,published) 
    #                VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.model_dump()) # **to unwind that post data as same above
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# GET POST BY ID
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} was not found")
    return {"post_details": post}



#DELETE POST
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    # index = find_index_post(id)
    # if index is None:
    #     raise HTTPException(status_code=404, 
    #                         detail = f"Post with id {id} does not exist")
    # my_posts.pop(index)
    # return Response(status_code = status.HTTP_204_NO_CONTENT)
    # No return needed; FastAPI will send 204 automatically

    # SQL code
    # cursor.execute("""DELETE FROM posts where id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #SQLAlchemy code
    post_queryObj = db.query(models.Post).filter(models.Post.id == id)
    if post_queryObj.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id {id} does not exist")
    
    post_queryObj.delete(synchronize_session = False)
    db.commit()




# UPDATE POST
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) # it only stores the query

    post = post_query.first() # it runs the query
    if post is None:
        raise HTTPException(status_code=404, 
                            detail = f"Post with id {id} does not exist")
    

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}