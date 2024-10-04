from fastapi import APIRouter, status, Depends, HTTPException
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

# custom imports
from schemas.user import CreateUserRequest
from models.user import User
from dependencies.auth_dependencies import pwd_context, oauth2_bearer, Token, authenticate_user, create_access_token
from dependencies.db_dependency import get_db

# auth imports
from passlib.context import CryptContext
from jose import jwt, JWTError

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/users/register', status_code=status.HTTP_201_CREATED)
def register_user(create_user_request: CreateUserRequest, db: db_dependency):
    try:
        # create a user in db and hash the password before storing in db
        create_user_model = User(username=create_user_request.username,
                                 hashed_password=pwd_context.hash(create_user_request.password),
                                 name=create_user_request.name, email=create_user_request.email)

        # add the user
        db.add(create_user_model)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e


@router.post('/users/login', response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    try:
        # authenticate the user
        # auth = Auth()
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user.")

        token = create_access_token(user.username, user.id, timedelta(minutes=20))

        return {'access_token': token, "token_type": "bearer"}

    except Exception as e:
        raise e
