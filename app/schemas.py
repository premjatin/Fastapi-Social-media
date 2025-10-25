from pydantic import BaseModel, EmailStr, Field, conint
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

class Post(BaseModel):
    id: int
    title:str
    content:str
    published: bool
    user_id:int
    owner: UserOut

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode=True


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id: int
    direction: int = Field(..., ge=0, le=1)






