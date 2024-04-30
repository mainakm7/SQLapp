from ..routers.auth import get_db, get_current_user, authenticate_user, creat_access_token, SECRET_KEY, ALGORITHM, get_current_user
from starlette import status
from ..models import Users
from .utils import *
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user

def test_authenticate_users(test_user: Users):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpass", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    
    non_user = authenticate_user("wrong_user", "testpass", db)
    assert non_user is None
    
    wrong_pass_user = authenticate_user(test_user.username, "testpass1", db)
    assert wrong_pass_user is None

def test_create_access_token():
    username = "testuser"
    userid = 1
    role = "user"
    expires_delta = timedelta(days=1)
    
    token = creat_access_token(username, userid, role, expires_delta)
    decoded_token = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM, options={"verify_signature":False})
    
    assert decoded_token.get("sub") == username
    assert decoded_token.get("id") == userid
    assert decoded_token.get("role") == role
    
@pytest.mark.asyncio
async def test_get_current_user_authenticated():
    
    encode = {"sub":"testuser","id":1, "role": "user"}
    token = jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)
    
    current_user = await get_current_user(token)
    
    assert current_user.get("username") == encode.get("sub")
    assert current_user.get("id") == encode.get("id")
    assert current_user.get("role") == encode.get("role")
    
@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excp:
        await get_current_user(token)
    
    assert excp.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excp.value.detail == "Couldn't validate credentials"
    
def test_create_new_user(test_user):
    user_req = {
                "email":"mm5@email.com",
                "username":"mmtest5",
                "first_name":"mmtest2",
                "last_name":"mmtest2",
                "password":"testpass2",
                "is_active":True,
                "role":"user",
                "phone_number":"2222222222"
            }
    
    response = client.post("/auth/create_user", json=user_req)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    user2 = db.query(Users).filter(Users.id == 2).first()
    
    assert user2.username == user_req.get("username")

    