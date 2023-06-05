from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from authentication.schema import Token
from authentication.jwt import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from sqlalchemy.orm import Session
from init_db import get_db
from datetime import timedelta


router = APIRouter(prefix='/api/auth', tags=['authentication'])


@router.post('/login', response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'Could not Validate Credential'},
        headers={'WWW_Authenticate': 'Bearer'}
    )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_delete=access_token_expire)
    return Token(access_token=access_token, token_type='bearer')