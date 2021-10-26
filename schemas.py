from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str

class UserCreation(BaseModel):
    name:str
    email:str
    password:str