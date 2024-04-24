from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import Field, BaseModel
from models import Todos, Users
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from .auth import get_current_user


router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency):
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin authentication failed")
    return db.query(Todos).all()

@router.delete("/delete_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, data_id: int = Path(gt=0)):
    
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin authentication failed")
    
    data_model = db.query(Todos).filter(Todos.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    db.query(Todos).filter(Todos.id == data_id).delete()
    db.commit()
    