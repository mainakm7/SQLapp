from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from pydantic import Field, BaseModel
import models
from models import sqlm
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]

class newdata(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete:bool
    
#REST APIs for table: todos in the sqlmdb database

@app.get("/", status_code=status.HTTP_200_OK)
def welcome_msg():
    return {"Greet": "Welcome! This is your todo app."}

@app.get("/todos", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    return db.query(sqlm).all()

@app.get("/todos/{data_id}", status_code=status.HTTP_200_OK)
def read_todos(db: db_dependency, data_id: int = Path(gt=0)):
    data_model =  db.query(sqlm).filter(sqlm.id == data_id).first()
    if data_model:
        return data_model
    else:
        raise HTTPException(status_code=404, detail="Data not Found")
    
@app.post("/todos/new_todo",status_code=status.HTTP_201_CREATED)
def create_todos(db: db_dependency, newdata1: newdata):
    data_model = sqlm(**newdata1.model_dump())
    
    db.add(data_model)
    db.commit()
    
@app.put("/todos/update_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_todos(db: db_dependency, data_id: int, newdata1: newdata):
    data_model = db.query(sqlm).filter(sqlm.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    data_model.title = newdata1.title
    data_model.description = newdata1.description
    data_model.priority = newdata1.priority
    data_model.complete = newdata1.complete
    
    db.add(data_model)
    db.commit()      
    

@app.delete("/todos/delete_todo/{data_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todos(db: db_dependency, data_id: int = Path(gt=0)):
    data_model = db.query(sqlm).filter(sqlm.id == data_id).first()
    if not data_model:
        raise HTTPException(status_code=404, detail="Data not Found")
    
    db.query(sqlm).filter(sqlm.id == data_id).delete()
    db.commit()