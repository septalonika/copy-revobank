from flask import Blueprint, jsonify, request
from auth.login import login_required
from views.user import get_all_users, create_user, get_user, update_user, delete_user,get_me, update_me

user_router = Blueprint("user_router", __name__, url_prefix="/api/v1/users")

@user_router.route("", methods=["GET", "POST"])
def get_users():
     match request.method.lower():
        case "get":
            return get_all_users()     
        case "post":
            return create_user()
        case default:
            return jsonify({"message": "Invalid request method", "success": False, "status": 405})

@user_router.route("/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def get_user_by_id(user_id):
    match request.method.lower():
        case "get":
            return get_user(user_id)
        case "put":
            return update_user(user_id)
        case "delete":
            return delete_user(user_id)
        case default:
            return jsonify({"message": "Invalid request method", "success": False, "status": 405})
        
@user_router.route("/me", methods=["GET", "PUT"])
@login_required
def get_my_profile():
    match request.method.lower():
        case "get":
            return get_me()
        case "put":
            return update_me()