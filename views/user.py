from datetime import datetime
from flask import jsonify, request
from repositories.user import all_users_repository
from models.user import list_user_db
from auth.login import claim_user

def find_user_by_id(_id: int):
    user = all_users_repository()["users"]

    for user in user:
        if user["id"] == _id:
            return {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"]
            }
    return None

def get_all_users():
    list_user =  all_users_repository()["users"]
    formatted_users = []

    for user in list_user:
        formatted_users.append(
            {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"]
            }
        )

    if len(formatted_users) < 1:
        return jsonify({"data": [], "message": "No Data!", "success": True, "status": 204})
    return jsonify({"data": formatted_users, "message": "User data retrieved successfully", "success": True, "status": 200})

def get_user(user_id):
    user = find_user_by_id(user_id)
    if not user:
        return jsonify({"data": {"message": "User not found"}, "success": False}), 404

    return jsonify({"data": user, "success": True}), 200

def update_user(user_id):
    
    user = next((user for user in list_user_db["users"] if user["id"] == user_id), None)
    if user is None:
        return jsonify({"data": [], "message": "User not found", "success": False, "status": 404}), 404

    update_data = request.json
    email = update_data.get("email")
    password = update_data.get("password")
    first_name = update_data.get("first_name")
    last_name = update_data.get("last_name")
    full_name = f"{first_name} {last_name}"

    user["email"] = email
    user["password"] = password
    user["first_name"] = first_name
    user["last_name"] = last_name
    user["full_name"] = full_name

    formatted_user = {
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    }

    return jsonify({"data": formatted_user, "message": "User updated successfully", "success": True}), 200


def create_user():
    try:
        register_data = request.json
        email = register_data.get("email")
        password = register_data.get("password")
        first_name = register_data.get("first_name")
        last_name = register_data.get("last_name")
        full_name = f"{first_name} {last_name}"

        list_users = get_all_users().get_json()
        if any(user["email"] == email for user in list_users["data"]):
            return jsonify({"message": "Email already registered", "success": False, "status": 409}), 409
        if not first_name:
            return jsonify({"message": "First name is required", "success": False, "status": 400}), 400
        if not last_name:
            return jsonify({"message": "Last name is required", "success": False, "status": 400}), 400
        if not email:
            return jsonify({"message": "Email is required", "success": False, "status": 400}), 400
        if not password:
            return jsonify({"message": "Password is required", "success": False, "status": 400}), 400
        if len(password) < 8:
            return jsonify({"message": "Password must be at least 8 characters long", "success": False, "status": 400}), 400
        
        user_id = max(list(list_users["data"]), key=lambda x: x['id'])['id'] + 1 if list_users["data"] else 1

        user_data = {
            "id": user_id,
            "email": email,     
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "created_at": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }
        list_user_db["users"].append(user_data)
        formatted_user_list = {
            "id": user_data["id"],
            "email": user_data["email"],
            "full_name": user_data["full_name"]
        }
        return jsonify({"data": formatted_user_list, "message": f"User {formatted_user_list['full_name']} created", "success": True, "status": 201})

    except:
        return jsonify({"data": [], "message": "user failed to create", "success": False, "status": 500})

def delete_user(user_id):
    user = next((user for user in list_user_db["users"] if user["id"] == user_id), None)
    if user is None:
        return jsonify({"data": [], "message": "User not found", "success": False, "status": 404}), 404
    list_user_db["users"].remove(user)
    list_user = list_user_db["users"].copy()
    formatted_user_list = []
    for user in list_user:
        formatted_user_list.append(
            {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"]
            }
        )
    return jsonify({"data": formatted_user_list, "message": f"user {user['full_name']} has been deleted", "success": True, "status": 202})

def get_me():
    authorization_token = request.headers.get("Authorization")
    email = claim_user(authorization_token)
    user = next((user for user in list_user_db["users"] if user["email"] == email), None)
    if user is None:
        return jsonify({"data": {"message": "User not found"}, "success": False}), 404
    formatted_user = {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "created_at": user["created_at"]
    }
    return jsonify({"data": formatted_user, "success": True}), 200

def update_me():
    try:
        authorization_token = request.headers.get("Authorization")
        email = claim_user(authorization_token)
        user = next((user for user in list_user_db["users"] if user["email"] == email), None)
        if user is None:
            return jsonify({"data": {"message": "User not found"}, "success": False}), 404
        update_data = request.json
        email = update_data.get("email")
        password = update_data.get("password")
        user_id = update_data.get("user_id")
        first_name = update_data.get("first_name")
        last_name = update_data.get("last_name")
        full_name = f"{first_name} {last_name}"

        user_data = {
            "id": user_id,
            "email": email,     
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "created_at": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        user["email"] = email
        user["password"] = password
        user["first_name"] = first_name
        user["last_name"] = last_name
        user["full_name"] = full_name
        user["created_at"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        return jsonify({ "message": f"User {user_data['full_name']} updated", "success": True, "status": 201})

    except:
        return jsonify({"message": "user failed to edit", "success": False, "status": 401})