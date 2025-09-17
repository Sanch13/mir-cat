from fastapi import APIRouter

router = APIRouter(tags=["First chapter"])


@router.get("/hello")  # простой URL
def greet():
    return "Hello? World?"
