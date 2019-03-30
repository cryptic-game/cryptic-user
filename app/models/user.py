from datetime import datetime
from uuid import uuid4

from flask_bcrypt import generate_password_hash
from sqlalchemy import Column, String, DateTime

import objects_db as db


class User(db.base):
    __tablename__: str = "user"

    uuid: Column = Column(String(32), primary_key=True, unique=True)
    username: Column = Column(String(50), nullable=False, unique=True)
    password: Column = Column(String(128), nullable=False)
    email: Column = Column(String(191), nullable=False, unique=True)  # max length is 255 defined by RFC 5321
    created: Column = Column(DateTime, nullable=False, default=datetime.utcnow)

    @property
    def serialize(self) -> dict:
        _ = self.uuid
        return {**self.__dict__}

    @staticmethod
    def create(username: str, password: str, email: str) -> dict:
        """
        Creates a new user based on the username, password and email.

        :param username: The username
        :param password: The raw password
        :param email: The email address
        :return: dict with status
        """

        uuid: str = str(uuid4()).replace("-", "")

        user: User = User(
            uuid=uuid,
            username=username,
            password=generate_password_hash(password),
            email=email
        )

        db.session.add(user)
        db.session.commit()

        return {"success": "Account has been created. ", "uuid": uuid}
