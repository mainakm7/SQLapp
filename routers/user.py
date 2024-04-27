from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pydantic import Field, BaseModel
from ..models import Users
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(prefix="/user", tags=["User"])



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class userverification(BaseModel):
    oldpassword: str
    newpassword: str = Field(min_length=6)
    
class usernewinfo(BaseModel):
    newemail: Optional[str] = Field(None, min_length=3)
    newphone: Optional[str] = Field(None, min_length=3, max_length=20)

@router.get("/info", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/update_password", status_code=status.HTTP_200_OK)
async def update_password(passreq: userverification, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not Found")
    
    if not bcrypt_context.verify(passreq.oldpassword, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password mismatch") 
    
    user_model.hashed_password = bcrypt_context.hash(passreq.newpassword)
    
    db.add(user_model)
    db.commit()
    
@router.put("/update_info", status_code=status.HTTP_200_OK)
async def update_info(newinforeq: usernewinfo, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not Found")

    user_model.email = newinforeq.newemail
    user_model.phone_number = newinforeq.newphone
    
    db.add(user_model)
    db.commit()
    