from fastapi import APIRouter
from Models import user_model

router = APIRouter(prefix="/user")

@router.post("/register")
async def login(user: user_model):
    try:
        # zweryfikuj dane
        print("a")
        # jeżeli nie poprawne zwróć wyjątek

        # jeżeli poprawne dodaj do bazy danych
    except Exception as e:
        print(e)
        