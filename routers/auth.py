from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from starlette import status
from ..models import Users
from pydantic import BaseModel
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
import json


router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


with open(r".\secrets.json", "r") as f:
    secrets = json.load(f)
#Secret key generated with rand hex32
SECRET_KEY = secrets.get("SECRET_KEY")
ALGORITHM = secrets.get("ALGORITHM")

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
    phone_number: str

class Token(BaseModel):
    access_token:str
    token_type:str

def authenticate_user(username:str, password:str, db: db_dependency):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def creat_access_token(username:str, userid:int, role:str, expires_delta: timedelta):
    encode = {"sub":username, "id":userid, "role":role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        userid = payload.get("id")
        role = payload.get("role")
        if not username or not userid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")
        else:
            return {"username":username,"id":userid, "role":role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, newuser1: newuser):
    user_model = Users(
                    email = newuser1.email,
                    username = newuser1.username,
                    first_name = newuser1.first_name,
                    last_name = newuser1.last_name,
                    hashed_password = bcrypt_context.hash(newuser1.password),
                    role = newuser1.role,
                    is_active=True,
                    phone_number=newuser1.phone_number
                )
    
    db.add(user_model)
    db.commit()
    
@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def auth_user_token(form_data: form_dependency, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")
    token = creat_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token":token, "token_type": "Bearer"}
    