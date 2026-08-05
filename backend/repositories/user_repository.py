from sqlalchemy.orm import Session

from models.user import User



class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):

        return db.query(User).filter(
            User.email == email
        ).first()

    @staticmethod
    def create(

        db: Session,

        username: str,

        email: str,

        password: str

    ):

        user = User(

            username=username,

            email=email,

            password=password

        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user