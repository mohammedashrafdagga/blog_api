from fastapi import APIRouter, Depends, HTTPException, status
from init_db import get_db
from schema import PostModel, CommentModel
from models import User, Post, Comment
from typing import Annotated, List
from authentication.jwt import get_current_active_user
from sqlalchemy.orm import Session


# instance form APIRouter
router = APIRouter(
    prefix='/api/comment',
    tags=['comments']
)


# Working With Comment

# adding Comment For Post
@router.post('/post/{blog_slug}/add', response_model=PostModel)
async def add_comment(blog_slug:str,request:CommentModel, user:Annotated[User, Depends(get_current_active_user)], db:Session = Depends(get_db)):
    # get post
    post =  db.query(Post).filter(Post.slug == blog_slug).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post Not Founded'
        )
    
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
    comment: Comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id:
        raise HTTPException(status_code=400, detail="You not allowed to delete comment")
    
    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted"}


@router.put("/update/{comment_id}", response_model=CommentModel)
def update_comment(comment_id: int, request:CommentModel, user:Annotated[User, Depends(get_current_active_user)],db:Session = Depends(get_db)):

    # Check if the comment exists
    comment: Comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id:
        raise HTTPException(status_code=400, detail="You not allowed to delete comment")
    
    if request.content:
        comment.content = request.content 
   
    db.commit()
    db.refresh(comment)
    return comment
