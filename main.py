from typing import List
from logging import raiseExceptions
from fastapi import FastAPI,Depends,status ,HTTPException
from passlib.utils.decor import deprecated_function
import schemas,model
from database  import engine,sessionlocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext

app=FastAPI()


class Blog(BaseModel):
    title:str
    body:str

class Showblog(BaseModel):
   
    body:str   
    class Config():
        orm_mode=True

model.Base.metadata.create_all(engine)


def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def creat_blog(req:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=model.Blog(title=req.title,body=req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=204)
def destroy(id,db:Session=Depends(get_db)):
    blog_delete=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog_delete.first():
        raise HTTPException(status_code=404, detail=f'blog with the id {id} not found to delete')
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,req:Blog,db:Session=Depends(get_db)):
    blog_update=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog_update.first():
        raise HTTPException(status_code=404, detail=f'blog with the id {id} not found to update')
    
    blog_update.update(req.dict())
    db.commit()
    return 'updated'


@app.get('/blog',response_model=List[Showblog])
def all(db:Session=Depends(get_db)):
    blogs=db.query(model.Blog).all()
    return blogs

@app.get('/blog/{id}',response_model=Showblog)
def show_1(id,db:Session=Depends(get_db)):
    blog_1=db.query(model.Blog).filter(model.Blog.id==id).first()
    if not blog_1:
        raise HTTPException(status_code=404,detail=f'blog with the id {id} not found')

    return blog_1

pwd_cntxt=CryptContext(schemes=['bcrypt'],deprecated='auto')

@app.post('/user')
def create_user(req:schemas.UserCreation,db:Session=Depends(get_db)):
    hashed_pass=pwd_cntxt.hash(req.password)
    new_user=model.User(name=req.name,email=req.email,password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


