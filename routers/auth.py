from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from models import Users
from pydantic import BaseModel
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        

form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]      
db_dependency = Annotated[Session, Depends(get_db)]



class newuser(BaseModel):
    
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


def authenticate_user(username:str, password:str, db: db_dependency):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post("/users/create_user", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, newuser1: newuser):
    user_model = Users(
                    email = newuser1.email,
                    username = newuser1.username,
                    first_name = newuser1.first_name,
                    last_name = newuser1.last_name,
                    hashed_password = bcrypt_context.hash(newuser1.password),
                    role = newuser1.role,
                    is_active=True
                )
    
    db.add(user_model)
    db.commit()
    
@router.post("/users/token", status_code=status.HTTP_201_CREATED)
def auth_user_login(form_data: form_dependency, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    return "Successful Authentication"
    