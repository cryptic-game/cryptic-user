import re
from typing import Optional

from flask_bcrypt import check_password_hash

import objects_db as db
from models.session import Session
from models.user import User


def handle(endpoint: list, data: dict) -> dict:
    """
    The handle method to get data from server to know what to do
    :param endpoint: the action of the server 'get', 'register', 'login', 'logout'
    :param data: source_uuid, key, send_amount, destination_uuid ...
    :return: user response for actions
    """
    # endpoint[0] will be the action what to do in an array ['get', ...]
    if endpoint[0] == "register":
        if "username" not in data:
            return {"user_response": {"error": "Key 'username' has to be set for endpoint register."}}
        if type(data["username"]) is not str:
            return {"user_response": {"error": "Key 'username' has to be string for endpoint register."}}
        if "password" not in data:
            return {"user_response": {"error": "Key 'password' has to be set for endpoint register."}}
        if type(data["password"]) is not str:
            return {"user_response": {"error": "Key 'password' has to be string for endpoint register."}}
        if "email" not in data:
            return {"user_response": {"error": "Key 'email' has to be set for endpoint register."}}
        if type(data["email"]) is not str:
            return {"user_response": {"error": "Key 'email' has to be string for endpoint register."}}
        username: str = data["username"]
        password: str = data["password"]
        email: str = data["email"]

        if len(username) < 3:
            return {"user_response": {"error": "Username has to be longer than 2."}}

        if len(password) < 9:
            return {"user_response": {"error": "Password has to be longer than 8."}}

        if not bool(re.search(r'\d', password)):
            return {"user_response": {"error": "Password has to contain at least one digit."}}

        found_lower: bool = False
        found_upper: bool = False

        for c in password:
            if found_lower and found_upper:
                break
            if c.islower():
                found_lower: bool = True
            elif c.isupper():
                found_upper: bool = True

        if not (found_upper and found_lower):
            return {"user_response": {"error": "Password has to contain lower and uppercase letters."}}

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return {"user_response": {"error": "Invalid email address."}}

        if db.session.query(User).filter(User.username == username).first() is not None:
            return {"user_response": {"error": "Username already used."}}

        if db.session.query(User).filter(User.email == email).first() is not None:
            return {"user_response": {"error": "Email address already used."}}

        user: User = User.create(username, password, email)

        session: Session = Session.create(user.uuid)

        # API ???
        # # Create device
        # device_response: Response = put(api.app.config["DEVICE_API"] + "device/private", headers={
        #     "Token": session.token
        # })
        #
        # if device_response.status_code != 200:
        #     # Rollback
        #     db.session.delete(session)
        #     db.session.delete(user)
        #     db.session.commit()
        #     try:
        #         msg: str = device_response.json()["message"]
        #         abort(400, "Nested error from device api:" + msg)
        #     except Exception:
        #         abort(400, "error in device api")
        #
        # device_response: dict = device_response.json()
        #
        # # Create wallet
        # currency_response: Response = put(api.app.config["CURRENCY_API"] + "wallet", headers={
        #     "Token": session.token
        # })
        #
        # if currency_response.status_code != 200:
        #     # Rollback
        #     db.session.delete(session)
        #     db.session.delete(user)
        #     db.session.commit()
        #     try:
        #         msg: str = currency_response.json()["message"]
        #         abort(400, "Nested error from currency api:" + msg)
        #     except Exception:
        #         abort(400, "error in currency api")
        #
        # currency_response: dict = currency_response.json()
        #
        # # Create file on device
        # file_response: Response = put(api.app.config["DEVICE_API"] + "file/" + device_response["uuid"], headers={
        #     "Token": session.token,
        #     "Content-Type": "application/json"
        # }, json={
        #     "filename": "first.wallet",
        #     "content": "UUID:" + currency_response["uuid"] +
        #                "\nKEY:" + currency_response["key"]
        # })
        #
        # if file_response.status_code != 200:
        #     # Rollback
        #     db.session.delete(session)
        #     db.session.delete(user)
        #     db.session.commit()
        #     try:
        #         msg: str = file_response.json()["message"]
        #         abort(400, "Nested error from file api:" + msg)
        #     except Exception:
        #         abort(400, "error in file api")

        db.session.delete(session)
        db.session.commit()

        response: dict = {"success": "User has been created", "username": username}
    elif endpoint[0] == "login":
        if "username" not in data:
            return {"user_response": {"error": "Key 'username' has to be set for endpoint login."}}
        if type(data["username"]) is not str:
            return {"user_response": {"error": "Key 'username' has to be string for endpoint login."}}
        if "password" not in data:
            return {"user_response": {"error": "Key 'password' has to be set for endpoint login."}}
        if type(data["password"]) is not str:
            return {"user_response": {"error": "Key 'password' has to be string for endpoint login."}}

        username: str = data["username"]
        password: str = data["password"]

        result: Optional[User] = db.session.query(User).filter(User.username == username).first()

        if result is None:
            return {"user_response": {"error": "Invalid username."}}

        if not check_password_hash(result.password, password):
            return {"user_resonse": {"error": "Invalid password."}}

        session: Session = Session.create(result.uuid)

        response = {
            "success": "Session has been created.",
            "created": session.created,
            "expires": session.expires
        }
    elif endpoint[0] == "logout":
        # db.session.delete(session)
        # db.session.commit()
        response = {"success": "Logged out successfully."}
    elif endpoint[0] == "get":
        # return session.serialize
        response = {}
    else:
        response: dict = {"error": "Endpoint is not supported."}
    return {"user_response": response}


def handle_ms(data: dict) -> dict:
    return data
