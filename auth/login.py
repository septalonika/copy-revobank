import base64
from functools import wraps
from flask import jsonify, request
from models.user import list_user_db


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = getattr(request, "user", None)
        if user is None:
            return jsonify({"message": "Unauthorized", "success": False}), 401
        return f(*args, **kwargs)

    return decorated_function


def claim_user(token):
    user_data = base64.b64decode(token).decode().split(":")
    email = user_data[0]
    return email


def get_token(user_data):
    email = user_data["email"]
    user_id = user_data["id"]
    return base64.b64encode(f"{email}:{user_id}".encode()).decode()
