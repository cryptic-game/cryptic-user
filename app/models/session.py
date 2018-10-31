from objects import db
from uuid import uuid4
from datetime import datetime, timedelta

EXPIRE_TIME: dict = {
    "days": 2
}  # time after the token gets invalid


class SessionModel(db.Model):
    __tablename__: str = "session"

    token: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    owner: db.Column = db.Column(db.String(32), nullable=False)
    created: db.Column = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires: db.Column = db.Column(db.DateTime, nullable=False)

    @property
    def serialize(self) -> dict:
        valid = datetime.utcnow() <= self.expires
        _ = self.token
        return {**self.__dict__, "valid": valid}

    @staticmethod
    def create(user: str) -> 'SessionModel':
        """
        Creates a new sessions for a specified user.

        :param user: The owner's id
        :return: New session
        """

        # Create a new Session instance
        session: SessionModel = SessionModel(
            token=str(uuid4()).replace("-", ""),
            owner=user,
            expires=datetime.utcnow() + timedelta(**EXPIRE_TIME)
        )

        # Add the new session to the db
        db.session.add(session)
        db.session.commit()

        return session
