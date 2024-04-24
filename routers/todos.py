from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import Field, BaseModel
from models import Todos, Users
from database import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from .auth import get_current_user


router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class newdata(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3, max_length=100)
    priority: Optional[int] = Field(None, ge=1, le=5)
    complete: Optional[bool] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Job",
                "description": "Details",
                "priority": 5,
                "complete": False
            }
        }
    
#REST APIs for table: todos in the sqlmdb database



@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

@router.get("/{data_id}", status_code=status.HTTP_200_OK)
async def read_todos(user: user_dependency, db: db_dependency, data_id: int = Path(gt=0)):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    data_model =  db.query(Todos).filter(Todos.owner_id == user.get("id"), Todos.id == data_id).first()
    if data_model:
        return data_model
    else:
        raise HTTPException(status_code=404, detail="Data not Found")
    
@router.post("/new_todo",status_code=status.HTTP_201_CREATED)
async def create_todos(user: user_dependency, db: db_dependency, newdata1: newdata):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    data_model = Todos(**newdata1.model_dump(),owner_id = user.get("id"))
    
    db.add(data_model)
    db.commit()
    
@router.put("/update_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(user: user_dependency, db: db_dependency, data_id: int, newdata1: newdata):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    data_model = db.query(Todos).filter(Todos.owner_id == user.get("id"), Todos.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not Found")
    
    if newdata1.title:
        data_model.title = newdata1.title
    if newdata1.description:
        data_model.description = newdata1.description
    if newdata1.priority:
        data_model.priority = newdata1.priority
    if newdata1.complete:
        data_model.complete = newdata1.complete
    
    db.add(data_model)
    db.commit()      
    

@router.delete("/delete_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user: user_dependency, db: db_dependency, data_id: int = Path(gt=0)):
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    
    data_model = db.query(Todos).filter(Todos.owner_id == user.get("id"), Todos.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    db.query(Todos).filter(Todos.owner_id == user.get("id"), Todos.id == data_id).delete()
    db.commit()