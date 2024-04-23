from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import Field, BaseModel
from models import sqlm
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated, Optional


router = APIRouter()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]

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

@router.get("/", status_code=status.HTTP_200_OK)
def welcome_msg():
    return {"Greet": "Welcome! This is your todo app."}

@router.get("/todos", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    return db.query(sqlm).all()

@router.get("/todos/{data_id}", status_code=status.HTTP_200_OK)
def read_todos(db: db_dependency, data_id: int = Path(gt=0)):
    data_model =  db.query(sqlm).filter(sqlm.id == data_id).first()
    if data_model:
        return data_model
    else:
        raise HTTPException(status_code=404, detail="Data not Found")
    
@router.post("/todos/new_todo",status_code=status.HTTP_201_CREATED)
def create_todos(db: db_dependency, newdata1: newdata):
    data_model = sqlm(**newdata1.model_dump())
    
    db.add(data_model)
    db.commit()
    
@router.put("/todos/update_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_todos(db: db_dependency, data_id: int, newdata1: newdata):
    data_model = db.query(sqlm).filter(sqlm.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=404, detail="Data not Found")
    
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
    

@router.delete("/todos/delete_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todos(db: db_dependency, data_id: int = Path(gt=0)):
    data_model = db.query(sqlm).filter(sqlm.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    db.query(sqlm).filter(sqlm.id == data_id).delete()
    db.commit()