from ..routers.user import get_db, get_current_user
from starlette import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_user_info(test_user):
    response = client.get("/user/info")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "mmtest"
    assert response.json()["email"] == "mm@email.com"
    assert response.json()["first_name"] == "mmtest1"
    assert response.json()["last_name"] == "mmtest1"
    assert response.json()["role"] == "admin"
    assert response.json()["is_active"] == True
    assert response.json()["phone_number"] == "1111111111"

    
def test_update_user_password(test_user):
    pass_req = {"oldpassword":"test1234", "newpassword":"test12345"}
    
    response = client.put("/user/update_password", json=pass_req)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_update_user_password_invalid_current_password(test_user):
    pass_req = {"oldpassword":"test12345", "newpassword":"test123456"}
    
    response = client.put("/user/update_password", json=pass_req)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail":"Password mismatch"}
    
def test_update_user_info(test_user):
    info_req = {"newphone":"2222222222"}
    
    response = client.put("/user/update_info", json=info_req)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    
    assert model.phone_number == info_req.get("newphone")



