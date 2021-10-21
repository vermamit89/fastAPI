from logging import raiseExceptions
from fastapi import FastAPI,Depends,status ,HTTPException
from.import schemas,model
from .database  import engine,sessionlocal
from sqlalchemy.orm import Session

app=FastAPI()


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
def update(id,req:schemas.Blog,db:Session=Depends(get_db)):
    blog_update=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog_update.first():
        raise HTTPException(status_code=404, detail=f'blog with the id {id} not found to update')
    blog_update.update(req, synchronize_session=False)
    db.commit()
    return 'updated'


@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs=db.query(model.Blog).all()
    return blogs

@app.get('/blog/{id}')
def show_1(id,db:Session=Depends(get_db)):
    blog_1=db.query(model.Blog).filter(model.Blog.id==id).first()
    if not blog_1:
        raise HTTPException(status_code=404,detail=f'blog with the id {id} not found')

    return blog_1


