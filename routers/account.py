from flask import Blueprint, jsonify, request
from views.account import get_all_accounts, create_account, update_account, get_account_by_id, delete_account
from auth.login import login_required


account_router = Blueprint("account_router", __name__, url_prefix="/api/v1/accounts")

@account_router.route("", methods=["GET", "POST"])
@login_required
def get_accounts():
     match request.method.lower():
        case "get":
            return get_all_accounts()     
        case "post":
            return create_account(request.json)
        case default:
            return jsonify({"message": "Invalid request method", "success": False, "status": 405})

@account_router.route("/<int:account_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def get_detail_account(account_id):
    match request.method.lower():
        case "get":
            return get_account_by_id(account_id)
        case "put":
            return update_account(account_id)
        case "delete":
            return delete_account(account_id)
        case default:
            return jsonify({"message": "Invalid request method", "success": False, "status": 405})