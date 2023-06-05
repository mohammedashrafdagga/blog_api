from pydantic import BaseModel


# Token Model
class Token(BaseModel):
    access_token :str
    token_type: str
    
    
# Token Data Model
class TokenData(BaseModel):
    username: str or None = None
    

# User Model
class User(BaseModel):
    username: str
    email:str or None = None
    name:str or None = None
    is_active:bool or None =  True
    
    
# UserInDB with hash password
class UserInDB(User):
    password:str