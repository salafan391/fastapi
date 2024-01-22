from pydantic import BaseModel,EmailStr,ValidationError,conint
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title:str
    content:str
    published:bool=True

class UserResponse(BaseModel):
    email:EmailStr
    created_at:datetime
class PostResponse(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime
    owner:UserResponse


    class Config:
        from_attributes=True

class PostOut(BaseModel):
    post:Post
    vote:int
    class Config:
        from_attributes=True

class CreateUser(BaseModel):
    email: EmailStr
    password:str
    
    class Config:
        from_attributes=True


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    token_id:Optional[int]


class Vote(BaseModel):
    post_id:int
    post_dir:conint(le=1)