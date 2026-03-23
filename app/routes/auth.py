from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import User
from app.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(email: str, password: str):
    db = SessionLocal()

    try:
        user = User(email=email, password=hash_password(password))

        db.add(user)
        db.commit()
        return {"message": "User created successfully"}
    finally:
        db.close()

@router.post("/login")
def login(email: str, password: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.password):
            return {"error": "Invalid username or password"}

        token = create_access_token({"sub": user.email})

        return {"access_token": token}
    finally:
        db.close()