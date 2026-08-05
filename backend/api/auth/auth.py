from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import UserRegister, UserLogin
from database.crud import create_user, get_user_by_email

from utils.security import verify_password
from utils.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    if get_user_by_email(db, user.email):
        raise HTTPException(400, "Email already exists")

    create_user(db, user)

    return {"message": "Registration Successful"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(401, "Invalid Email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(401, "Invalid Password")

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }