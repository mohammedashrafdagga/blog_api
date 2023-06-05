from pydantic import BaseModel
from typing import List

class PostCreateModel(BaseModel):
    title:str
    description: str
    class Config:
        orm_mode = True

class PostUpdateModel(BaseModel):
    title:str or None= None
    description: str or None = None
    class Config:
        orm_mode = True
        
# Comment
class CommentModel(BaseModel):
    id:int or None = None
    content: str
    class Config:
        orm_mode = True
        
    
class PostModel(PostCreateModel):
    comments: List[CommentModel] or None = []
    class Config:
        orm_mode = True
        