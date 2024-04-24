from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/", status_code=status.HTTP_200_OK)
def welcome_msg():
    return {"Greet": "Welcome! This is your todo app."}