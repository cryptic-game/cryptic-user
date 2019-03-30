from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import Column, String, DateTime

import objects_db as db

EXPIRE_TIME: dict = {
    "days": 2
}  # time after the token gets invalid


class Session(db.base):
    __tablename__: str = "session"

    token: Column = Column(String(32), primary_key=True, unique=True)
    owner: Column = Column(String(32), nullable=False)
    created: Column = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires: Column = Column(DateTime, nullable=False)

    @property
    def serialize(self) -> dict:
        valid = datetime.utcnow() <= self.expires
        _ = self.token
        return {**self.__dict__, "valid": valid}

    @staticmethod
    def create(user: str) -> dict:
        """
        Creates a new sessions for a specified user.

        :param user: The owner's id
        :return: dict with status
        """

        # Create a new Session instance

        session: Session = Session(
            token=str(uuid4()).replace("-", ""),
            owner=user,
            expires=datetime.utcnow() + timedelta(**EXPIRE_TIME)
        )

        # Add the new session to the db
        db.session.add(session)
        db.session.commit()

        return {"success": "Session has been created. ", "token": session.token, "expires": session.expires}
