from sqlalchemy import exists
from os import urandom
from hashlib import sha512

from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)  # max length defiend by RFC 5321

    def delete(self) -> None:
        """
        Deletes this user.

        # TODO delete foreign key relationships before

        :return:
        """

        db.session.delete(self)
        db.session.commit()

    def commit(self) -> None:
        """
        Commits changes to the database.

        :return: None
        """

        db.session.commit()

    def as_private_simple_dict(self) -> dict:
        """
        Returns a dictionary with basic PRIVATE information about this user.

        :return: dictionary with basic information
        """

        return {
            "username": self.username,
            "email": self.email
        }

    def as_public_simple_dict(self) -> dict:
        """
        Returns a dictionary with basic PUBLIC information about this user.

        :return: dictionary with basic information
        """

        return {
            "username": self.username
        }

    @staticmethod
    def create(username: str, password: str, email: str) -> 'User':
        """
        Creates a new user based on the username, password and email.

        :param username: The username
        :param password: The raw password
        :param email: The email address
        :return: The newly created user
        """

        salt = urandom(128).hex()

        user = User(
            username=username,
            password=User._hash(password, salt),
            salt=salt,
            email=email
        )

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def _hash(password: str, salt: str) -> str:
        """
        Hashes a password with a given salt with the sha512-algorithm.

        :return: Hashed password
        """

        return sha512(password.encode("utf-8") + salt.encode("utf-8")).hexdigest()

    @staticmethod
    def get(username: str) -> 'User':
        """
        This function finds a user based on their unique username.

        :return: A user based on a username
        """

        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(id: int) -> 'User':
        """
        This function finds a user based on their unique id.

        :param id: The id
        :return: The user
        """

        return User.query.filter_by(id=id).first()

    @staticmethod
    def exists_username(username: str):
        """
        Checks if a user with given username exists.

        :return: True if there is a user with given username.
        """

        return db.session.query(exists().where(User.username == username))[0][0]

    @staticmethod
    def exists_email(email: str):
        """
        Checks if a email with given username exists.

        :return: True if there is a user with given email address.
        """

        return db.session.query(exists().where(User.email == email))[0][0]

    def validate_password(self, password):
        return self._hash(password, self.salt) == self.password