from database import db
from time import time
from uuid import uuid4


EXPIRE_TIME = 172800  # time after the token gets invalid (2 days)


class Session(db.Model):
    token = db.Column(db.String(32), primary_key=True, unique=True)
    owner = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, nullable=False)
    expire = db.Column(db.Integer, nullable=False)

    def delete(self) -> None:
        """
        Deletes this session.

        :return: None
        """

        db.session.delete(self)
        db.session.commit()

    def commit(self) -> None:
        """
        Commits changes to the database.

        :return: None
        """

        db.session.commit()

    def as_simple_dict(self) -> dict:
        """
        This function returns a basic dictionary with the basic information of this session

        :return: simplified version dict version of this
        """

        return {
            "token": self.token,
            "created": self.created,
            "expire": self.expire
        }

    def is_valid(self):
        return self.expire >= time()

    @staticmethod
    def create(user: int) -> 'Session':
        """
        Creates a new sessions for a specified user.

        :param user: The owner's id
        :return: New session
        """

        current_time = int(time())

        # Create a new Session instance
        session = Session(
            token=str(uuid4()).replace("-", ""),
            owner=user,
            created=current_time,
            expire=current_time+EXPIRE_TIME
        )

        # Add the new session to the db
        db.session.add(session)
        db.session.commit()

        return session

    @staticmethod
    def find(token: str) -> 'Session':
        """
        Finds a session by a token.

        :return: A session
        """

        return Session.query.filter_by(token=token).first()
