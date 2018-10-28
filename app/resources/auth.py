from flask_restplus import Namespace, Resource, fields, abort
from models.user import UserModel
from models.session import SessionModel
from basics import ErrorSchema, require_session
from objects import api, db
from flask import request
from flask_bcrypt import check_password_hash
import re

LoginRequestSchema = api.model("Login Request", {
    "username": fields.String(required=True,
                              example="FooBar",
                              description="the user's username"),
    "password": fields.String(required=True,
                              example="foo@bar.tld",
                              description="the user's password")
})

LoginResponseSchema = api.model("Login Response", {
    "token": fields.String(example="12abc34d-5efg-67hi-89j1-klm2nop3pqrs",
                           description="a login token"),
})

RegisterRequestSchema = api.model("Register Request", {
    "username": fields.String(required=True,
                              example="FooBar",
                              description="the user's username"),
    "email": fields.String(required=True,
                           example="foo@bar.tld",
                           description="the user's email address"),
    "password": fields.String(required=True,
                              example="secretpassword1234",
                              description="the user's password")
})

RegisterResponseSchema = api.model("Register Response", {
    "ok": fields.Boolean(description="was successfully registered")
})

LogoutResponseSchema = api.model("Logout Response", {
    "ok": fields.Boolean(description="was successfully logged out")
})

SessionResponseSchema = api.model("Session Response", {
    "token": fields.String(example="secretpassword1234",
                           description="session token"),
    "created": fields.DateTime(description="the datetime the session was created"),
    "expires": fields.DateTime(description="the datetime the session will expire")
})

auth_api = Namespace('auth')


@auth_api.route('/')
@auth_api.doc("Authentication Application Programming Interface")
class AuthAPI(Resource):

    @auth_api.doc("Information", security="token")
    @auth_api.marshal_with(SessionResponseSchema)
    @auth_api.response(400, "Invalid Input", ErrorSchema)
    @require_session
    def get(self, session):
        return session.serialize

    @auth_api.doc("Login")
    @auth_api.expect(LoginRequestSchema, validate=True)
    @auth_api.marshal_with(LoginResponseSchema)
    @auth_api.response(400, "Invalid Input", ErrorSchema)
    def post(self):
        username = request.json["username"]
        password = request.json["password"]

        result = UserModel.query.filter_by(username=username).first()

        if result is None:
            abort(400, "invalid username")

        if not check_password_hash(result.password, password):
            abort(400, "invalid password")

        session = SessionModel.create(result.id)

        return session.serialize

    @auth_api.doc("Register")
    @auth_api.expect(RegisterRequestSchema, validate=True)
    @auth_api.marshal_with(RegisterResponseSchema)
    @auth_api.response(400, "Invalid Input", ErrorSchema)
    def put(self):
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]

        if len(username) < 3:
            abort(400, "username has to be longer than 2")

        if len(password) < 9:
            abort(400, "password has to be longer than 8")

        if not bool(re.search(r'\d', password)):
            abort(400, "password has to contain at least one number")

        found_lower = False
        found_upper = False

        for c in password:
            if found_lower and found_upper:
                break
            if c.islower():
                found_lower = True
            elif c.isupper():
                found_upper = True

        if not (found_upper and found_lower):
            abort(400, "password has to contain lower and uppercase letters")

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            abort(400, "invalid email address")

        if UserModel.query.filter_by(username=username).first() is not None:
            abort(400, "username already used")

        if UserModel.query.filter_by(email=email).first() is not None:
            abort(400, "email address already used")

        UserModel.create(username, password, email)

        return {
            "ok": True
        }

    @auth_api.doc("Logout", security="token")
    @auth_api.marshal_with(LogoutResponseSchema)
    @auth_api.response(400, "Invalid Input", ErrorSchema)
    @require_session
    def delete(self, session):
        db.session.delete(session)
        db.session.commit()

        return {
            "ok": True
        }
