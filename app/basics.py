from flask_restplus import fields, abort
from flask_restplus.model import Model
from models.session import SessionModel
from objects import api
from functools import wraps
from flask import request
from typing import Optional

ErrorSchema: Model = api.model("Error", {
    "message": fields.String(readOnly=True)
})


def require_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'Token' in request.headers:
            token = request.headers["Token"]

            session: Optional[SessionModel] = SessionModel.query.filter_by(token=token).first()

            if session is None:
                abort(400, "invalid token")

            kwargs["session"] = session

            return f(*args, **kwargs)
        else:
            abort(400, "token required")

    return wrapper
