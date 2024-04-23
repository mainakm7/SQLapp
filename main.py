from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from pydantic import Field, BaseModel
import models
from models import Todos
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

app = FastAPI()

models.Base.metadata.create_all(bind = engine)



def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]

class newtodo(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete:bool
    

@app.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model =  db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not Found")
    
@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, newtodo1: newtodo):
    todo_model = Todos(**newtodo1.model_dump())
    
    db.add(todo_model)
    db.commit()
    
@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, todo_id: int, newtodo1: newtodo):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not Found")
    
    todo_model.title = newtodo1.title
    todo_model.description = newtodo1.description
    todo_model.priority = newtodo1.priority
    todo_model.complete = newtodo1.complete
    
    db.add(todo_model)
    db.commit()      
    

@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not Found")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()