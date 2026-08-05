from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token


class AuthService:

    @staticmethod
    def register(db: Session, username, email, password):

        user = UserRepository.get_by_email(db, email)

        if user:

            raise Exception("Email already exists.")

        hashed = hash_password(password)

        return UserRepository.create(db, username, email, hashed)

    @staticmethod
    def login(db: Session, email, password):

        user = UserRepository.get_by_email(db, email)

        if user is None:

            raise Exception("Invalid Credentials")

        if not verify_password(password, user.password):

            raise Exception("Invalid Credentials")

        token = create_access_token({"user_id": user.id, "email": user.email})

        return token
