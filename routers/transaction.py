from flask import Blueprint, request
from auth.login import login_required
from views.transaction import get_transactions, get_transaction_by_id, create_transaction

transaction_router = Blueprint("transaction_router", __name__, url_prefix="/api/v1/transactions")

@transaction_router.route("", methods=["GET", "POST"])
@login_required
def get_all_transactions():
    match request.method.lower():
        case "get":
            return get_transactions()
        case "post":
            return create_transaction(request.json)
        
@transaction_router.route("/<int:account_id>", methods=["GET"])
@login_required
def get_detail_transaction(account_id):
    match request.method.lower():
        case "get":
            return get_transaction_by_id(account_id)
