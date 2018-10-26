from flask_bcrypt import generate_password_hash
from objects import db
from uuid import uuid4
from datetime import datetime


class UserModel(db.Model):
    __tablename__: str = "user"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    username: db.Column = db.Column(db.String(50), nullable=False, unique=True)
    password: db.Column = db.Column(db.String(128), nullable=False)
    email: db.Column = db.Column(db.String(191), nullable=False, unique=True)  # max length is 255 defined by RFC 5321
    created: db.Column = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def serialize(self) -> dict:
        _ = self.id
        return self.__dict__

    @staticmethod
    def create(username: str, password: str, email: str) -> 'UserModel':
        """
        Creates a new user based on the username, password and email.

        :param username: The username
        :param password: The raw password
        :param email: The email address
        :return: The newly created user
        """

        uuid: str = str(uuid4()).replace("-", "")

        user: UserModel = UserModel(
            uuid=uuid,
            username=username,
            password=generate_password_hash(password),
            email=email
        )

        db.session.add(user)
        db.session.commit()

        return user
