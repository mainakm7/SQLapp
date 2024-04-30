from ..routers.todos import get_db, get_current_user
from starlette import status
from ..models import Todos
from .utils import *



app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user



def test_read_all_authenticated(test_todo):
    response = client.get("/todos/all")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete": False, "title": "App", "description": "testing apps", "id":1, "priority": 5, "owner_id": 1}]
    
def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"complete": False, "title": "App", "description": "testing apps", "id":1, "priority": 5, "owner_id": 1}
    
def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Data not Found"}
    
def test_create_todos(test_todo):
    request_todo = {
                    "title": "New_todo",
                    "description": "Creating new todo",
                    "priority": 5,
                    "complete": False
                }
    response = client.post("/todos/new_todo", json=request_todo)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_todo.get("title")
    assert model.description == request_todo.get("description")
    assert model.priority == request_todo.get("priority")
    assert model.complete == request_todo.get("complete")
    
def test_update_todos(test_todo):
    request_todo = {
                    "title": "change_todo",
                    "description": "Updating todo",
                    "priority": 5,
                    "complete": False
                }
    response = client.put("/todos/update_todo/1", json=request_todo)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model.title == request_todo.get("title")
    assert model.description == request_todo.get("description")
    assert model.priority == request_todo.get("priority")
    assert model.complete == request_todo.get("complete")
    
def test_update_todos_not_found(test_todo):
    request_todo = {
                    "title": "change_todo",
                    "description": "Updating todo",
                    "priority": 5,
                    "complete": False
                }
    response = client.put("/todos/update_todo/999", json=request_todo)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Data not Found"}
    
    

def test_delete_todos(test_todo):
    response = client.delete("/todos/delete_todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model == None
    
    
def test_delete_todos_not_found(test_todo):
    response = client.delete("/todos/delete_todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Data not Found"}