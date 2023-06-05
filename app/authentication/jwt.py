from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schema import TokenData
from .hash import  verify_password
from init_db import get_db
from sqlalchemy.orm import Session
from models import User
from dotenv import load_dotenv
from typing import Annotated
import os

# loading evn
load_dotenv()

# define Variable
SECRET_KEY = os.environ.get('SECRET_KEY')  # Replace with your own secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Get User
def get_user(username:str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'Could not Validate Credential'},
        headers={'WWW_Authenticate': 'Bearer'}
    )
    return user
    
# authentication for user
def authenticate_user( username: str, password: str, db:Session = Depends(get_db)):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# Now creating access token
def create_access_token(data: dict, expires_delete: timedelta | None = None):
    to_encode = data.copy()
    if expires_delete:
        expire = datetime.utcnow() + expires_delete
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# create an access token based in login data
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user