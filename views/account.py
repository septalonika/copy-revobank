from flask import jsonify, request
from models.account import list_account_db
from auth.login import claim_user
from repositories.user import all_users_repository

def create_account(incoming_payload: dict):
    authorization_token = request.headers.get("Authorization")
    email = claim_user(authorization_token)
    list_user = all_users_repository()
    user = next((user for user in list_user["users"] if user["email"] == email), None)
    account_payload = {
        "id": incoming_payload.get('id'),
        "card_product": incoming_payload.get("card_product"),
        "card_number": incoming_payload.get("card_number"),
        "type": incoming_payload.get("type"),
        "balance": incoming_payload.get("balance")
    }
    existing_account = next((account for account in list_account_db["accounts"][user["id"]] if account["id"] == account_payload["id"]), None)
    if not existing_account:
        list_account_db["accounts"][user["id"]].append(account_payload)
        return jsonify({"message": "Account created successfully"}), 201

    return jsonify({"error": "Account already exists"}), 409

def get_all_accounts():
    authorization_token = request.headers.get("Authorization")
    email = claim_user(authorization_token)
    list_user = all_users_repository()
    user = next((user for user in list_user["users"] if user["email"] == email), None)
    accounts = list_account_db["accounts"][user["id"]] if user else []
    return jsonify({
        "data": accounts,
        "message": "Accounts retrieved successfully",
        "success": True,
        "status": 200
    })

def get_account_by_id(account_id):
    authorization_token = request.headers.get("Authorization")
    list_user = all_users_repository()
    email = claim_user(authorization_token)
    user = next((user for user in list_user["users"] if user["email"] == email), None)
    account = next((account for account in list_account_db["accounts"][user["id"]] if account["id"] == account_id), None)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"data": account}), 200

def update_account(account_id):
    authorization_token = request.headers.get("Authorization")
    list_user = all_users_repository()
    email = claim_user(authorization_token)
    user = next((user for user in list_user["users"] if user["email"] == email), None)

    incoming_payload = request.get_json()
    new_balance = incoming_payload.get('balance')
    new_card_number = incoming_payload.get('card_number')
    new_card_product = incoming_payload.get('card_product')
    new_type = incoming_payload.get('type')

    new_account_data = {
        "id": account_id,
        "card_product": new_card_product,
        "card_number": new_card_number,
        "type": new_type,
        "balance": new_balance,
    }

    account = next((account for account in list_account_db["accounts"][user["id"]] if account["id"] == account_id), None)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    account.update(new_account_data)
    return jsonify({"message": "Account update successfully"}), 201

def delete_account( account_id):
    authorization_token = request.headers.get("Authorization")
    list_user = all_users_repository()
    email = claim_user(authorization_token)
    user = next((user for user in list_user["users"] if user["email"] == email), None)
    account = next((account for account in list_account_db["accounts"][user['id']] if account["id"] == account_id), None)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    list_account_db["accounts"][user['id']].remove(account)
    return jsonify({"message": "Account deleted successfully"}), 200
    

