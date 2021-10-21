from sqlalchemy import Integer,String,Column
from .database import Base


class Blog(Base):
    __tablename__='My Blog'

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)