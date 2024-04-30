from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..models import Todos, Users
import pytest
from ..routers.auth import bcrypt_context


SQL_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQL_TEST_URL, connect_args={"check_same_thread":False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()
        

def override_get_current_user():
    return {"username":"mainak123","id":1, "role":"admin"}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "App",
        description = "testing apps",
        priority = 5,
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    
    yield todo
    
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
        

@pytest.fixture
def test_user():
    user = Users(
        email = "mm@email.com",
        username = "mmtest",
        first_name = "mmtest1",
        last_name = "mmtest1",
        hashed_password = bcrypt_context.hash("testpass"),
        is_active = True,
        role = "admin",
        phone_number = "1111111111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    
    yield user
    
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
