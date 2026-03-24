from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import psycopg2
from psycopg2.extras import RealDictCursor
import time


#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Adminpass%40123@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# responsible for talking with DB's

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# whenever you want to interact with DB you have to pass it to the path operation function
# db: Session = Depends(get_db)



#Old snippit we used to connect to DB -> now we are using sqlAlchemy
#Database connection

# while True:

#     try:
#         conn = psycopg2.connect(host='localhost' ,database='fastapi', user='postgres',
#                                 password= 'Adminpass@123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sucessful!")
#         break
#     except Exception as error:
#         print("Connecting to DB failed")
#         print("Error: ", error)
#         time.sleep(2)
