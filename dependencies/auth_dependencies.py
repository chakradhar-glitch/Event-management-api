# auth imports
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import os
from datetime import timedelta, datetime

# custom imports
from dependencies.db_dependency import get_db
from models.user import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')

# password context to hash password
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Oauth2 password bearer that extracts password and verifies
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/login')

# db_dependency = Annotated[Session, Depends(get_db)]


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username, password, db):

    try:

        user = db.query(User).filter_by(username=username).first()
        if not user:
            return False

        if not pwd_context.verify(password, user.hashed_password):
            return False
        return user
    except Exception as e:
        raise e


def create_access_token(username, user_id, expire_delta: timedelta):
    try:
        encode = {'sub': username, "id": user_id}
        expires = datetime.now() + expire_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise e


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_name = payload.get('sub')
        user_id = payload.get('id')

        if not user_name:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user_name.')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user_id.')
        return {'username': user_name, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user due to jwterror.')
