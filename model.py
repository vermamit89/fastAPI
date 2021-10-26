
from sqlalchemy import Integer,String,Column
from database import Base


class Blog(Base):
    __tablename__='Blog'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)

class User(Base):
    __tablename__='user'

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)

