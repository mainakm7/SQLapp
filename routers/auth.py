from fastapi import APIRouter

router = APIRouter()

@router.get("/todos/auth/")
def get_user():
    return {"user":"authenticated"}