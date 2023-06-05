from fastapi import APIRouter, Depends, status, HTTPException
from init_db import get_db
from schema import PostModel, PostUpdateModel, PostCreateModel
from typing import Annotated, List
from sqlalchemy.orm import Session
from models import User, Post
from authentication.jwt import get_current_active_user
from utils import user_is_staff, post_is_exist, post_is_not_exist

router = APIRouter(
    prefix='/api/post',
    tags=['posts']
)

@router.post('/', status_code=status.HTTP_201_CREATED,response_model=PostModel)
async def create_post(post_model: PostCreateModel,user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    # only staff user can create post
    user_is_staff(user)
    
    # check about slug
    slug = post_model.title.lower().replace(" ", "-")  # Generate slug from title
    
    # check if post exists raise Error
    post_is_exist(post_slug=slug)
    
    post = Post(**post_model.dict(), slug=slug, user=user)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# Getting all post in blog
@router.get("/", response_model=List[PostModel])
def get_all_posts(db:Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts



# Getting all post in blog
@router.get("/{post_slug}", response_model=PostModel)
def get_post(post_slug:str, db:Session = Depends(get_db)):
    post = post_is_not_exist(post_slug = post_slug)
    return post

@router.put('/update/{blog_slug}', response_model=PostModel)
async def update_post(blog_slug:str, request:PostUpdateModel, user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    user_is_staff(user)
    # check about slug
    post = post_is_not_exist(post_slug = blog_slug)
    
    if request.title:
        post.title = request.title
        
    if request.description:
        post.description = request.description
        
    db.commit()
    db.refresh(post)
    return post    


@router.delete('/delete/{blog_slug}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(blog_slug:str, user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    user_is_staff(user)
    # check about slug
    post = post_is_not_exist(post_slug = blog_slug)
    db.delete(post)
    db.commit()
    return {'detail': 'Successfully Delete Post'}    
