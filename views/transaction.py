from datetime import datetime
from flask import jsonify, request
from repositories.transaction import all_transactions_repository
from repositories.user import all_users_repository
from repositories.account import all_accounts_repository
from auth.login import claim_user
from models.account import list_account_db


def get_transactions():
    authorization_token = request.headers.get("Authorization")
    email = claim_user(authorization_token)
    list_transactions = all_transactions_repository()
    user = next((user for user in all_users_repository()["users"] if user["email"] == email), None)
    transactions = list_transactions["transactions"][user["id"]] if user else []

    return jsonify({
        "data": transactions,
        "message": "Accounts retrieved successfully",
        "success": True,
        "status": 200
    })

def get_transaction_by_id(transaction_id):
    authorization_token = request.headers.get("Authorization")
    list_transactions = all_transactions_repository()
    email = claim_user(authorization_token)
    user = next((user for user in all_users_repository()["users"] if user["email"] == email), None)
    transaction = next((account for account in list_transactions["transactions"][user["id"]] if user["id"] == transaction_id), None)
    if transaction is None:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"data": transaction}), 200

def create_transaction(incoming_payload: dict):
    account_id = incoming_payload.get('id')
    amount = incoming_payload.get("amount")
    recepient_card_number = incoming_payload.get("recepient")["card_number"]
    recepient_email = incoming_payload.get("recepient")["email"]
    recepient_fullname = incoming_payload.get("recepient")["full_name"]
    transaction_type = incoming_payload.get("transaction_type")

    authorization_token = request.headers.get("Authorization")
    email = claim_user(authorization_token)
    list_users = all_users_repository()
    list_transactions = all_transactions_repository()
    list_accounts = all_accounts_repository()

    user_data = next((user for user in list_users["users"] if user["email"] == email), None)
    account_data = next((account for account in list_accounts["accounts"] if account == user_data["id"]), None)
    account = list_accounts["accounts"][user_data["id"]]
    balance = next((account_balance["balance"] for account_balance in account if account_balance["balance"] > 0), 0)

    transaction_id = len(list_transactions["transactions"][account_data]) + 1 if user_data else 1
    
    transaction_payload = {
        "account_id": account_id,
        "transaction_id": transaction_id,
        "transaction_date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "amount": amount,
        "transaction_type": incoming_payload.get("transaction_type")
    }
    
    match transaction_type:
        case "transfer":
            if balance < amount:
                return jsonify({"error": "Insufficient balance"}), 400
            recepient = {
                "user_id": user_data["id"],
                "full_name": recepient_fullname,
                "email": recepient_email,
                "card_number": recepient_card_number,
            }
            transaction_payload["recepient"] = recepient
            for account_balance in list_account_db["accounts"][user_data["id"]]:
                print("cugud account_balance", account_balance["id"])
                print("cugud account", account_data)
                if account_balance["id"] == account_data:
                    account_balance["balance"] -= amount
                    break
        case "deposit":
            account["balance"] += amount
        case "withdrawal":
            if balance < amount:
                return jsonify({"error": "Insufficient balance"}), 400
            account["balance"] -= amount

    return jsonify({"message": "Transaction created successfully"}), 201






    
