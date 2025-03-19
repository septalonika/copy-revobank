from auth.login import get_token
from models.user import list_user_db


def user_login(email, password) -> str:
    user = next((user for user in list_user_db["users"] if user["email"] == email), None)
    assert user["password"] == password, "Password is incorrect"
    token = get_token(user)
    return token