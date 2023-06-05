from fastapi import HTTPException, status, Depends
from database import SessionLocal
from models import User, Post, Comment

db = SessionLocal()
# check if user os staff or nor
def user_is_staff(user:User) -> None:
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not allowed to create post '
        )
# get post
async def get_post_by_slug(post_slug):
    return db.query(Post).filter(Post.slug == post_slug).first()

# For Post is existing raise HTTP
async def post_is_exist(post_slug):
    post = get_post_by_slug(post_slug)
    if post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the post we create with title is already have, change title'
        )
    
    
# For Post is existing raise HTTP
async def post_is_not_exist(post_slug):
    post = get_post_by_slug(post_slug)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post Not Founded'
        )
    return post_slug
    
 
async def get_comment(comment_id:int):
    comment: Comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
    
def is_owner_comment(user:User, comment:Comment):
    if user.id != comment.user_id:
        raise HTTPException(status_code=400, detail="You not allowed to delete comment")