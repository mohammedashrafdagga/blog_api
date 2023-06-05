'''
    Building Database
'''
from database import Base
from sqlalchemy import Column, String, Integer, Text, Boolean,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


# UserTable
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(Text)
    is_active=Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    

# Define the Post model
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    slug = Column(String, unique=True, index=True)
    create_at =  Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")
    comments = relationship('Comment', back_populates='post')


# Comment Model
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    content = Column(String)
    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')
    