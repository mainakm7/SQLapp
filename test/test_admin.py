from ..routers.admin import get_db, get_current_user
from starlette import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_todos(test_todo):
    response = client.get("/admin/todo")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete": False, "title": "App", "description": "testing apps", "id":1, "priority": 5, "owner_id": 1}]
    
    
def test_delete_todos(test_todo):
    response = client.delete("/admin/delete_todo/1")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model == None
    
def test_delete_todos_not_found(test_todo):
    response = client.delete("/admin/delete_todo/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Data not Found"}