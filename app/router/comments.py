from fastapi import APIRouter, Depends, HTTPException, status
from init_db import get_db
from schema import PostModel, CommentModel
from models import User, Post, Comment
from typing import Annotated, List
from authentication.jwt import get_current_active_user
from sqlalchemy.orm import Session
from utils import post_is_not_exist, get_comment, is_owner_comment


# instance form APIRouter
router = APIRouter(
    prefix='/api/comment',
    tags=['comments']
)


# Working With Comment

# adding Comment For Post
@router.post('/post/{post_slug}/add', response_model=PostModel)
async def add_comment(post_slug:str,request:CommentModel, user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    # get post
    post =  post_is_not_exist(post_slug=post_slug)
    
    comment = Comment(
        post_id=post.id,
        user_id=user.id,
        content=request.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return post





# delete Comment
@router.delete("/delete/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, user:Annotated[User, Depends(get_current_active_user)],db:Session = Depends(get_db)):

    # Check if the comment exists
    comment: Comment = get_comment(comment_id=comment_id)
    is_owner_comment(user=user, comment=comment)
    
    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted"}


@router.put("/update/{comment_id}", response_model=CommentModel)
def update_comment(comment_id: int, request:CommentModel, user:Annotated[User, Depends(get_current_active_user)],db:Session = Depends(get_db)):

    # Check if the comment exists
    comment: Comment = get_comment(comment_id=comment_id)
    is_owner_comment(user=user, comment=comment)
    
    if request.content:
        comment.content = request.content 
   
    db.commit()
    db.refresh(comment)
    return comment
