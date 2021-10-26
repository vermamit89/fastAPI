from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str

class UserCreation(BaseModel):
    name:str
    email:str
    password:str

class Showuser(BaseModel):
   
    name:str 
    email:str  
    class Config():
        orm_mode=True