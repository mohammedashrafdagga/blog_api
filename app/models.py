'''
    Building Database
'''
from .database import Base
from sqlalchemy import Column, String, Integer, Text, Boolean


# UserTable
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(Text)
    is_active=Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"{self.username}"