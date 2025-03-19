import uuid
from flask import Flask, render_template, request
from auth.login import claim_user
from views.user import get_all_users
from routers.account import account_router
from routers.user import user_router
from routers.auth import auth_router
from routers.transaction import transaction_router

app = Flask(__name__)
app.register_blueprint(user_router)

app.register_blueprint(auth_router)

app.register_blueprint(account_router)

app.register_blueprint(transaction_router)

@app.before_request
def before_request():
    authorization_token = request.headers.get("Authorization")
    if authorization_token:
        user = claim_user(authorization_token)
        request.user = user

@app.after_request
def after_request(response):
    request_id = str(uuid.uuid4())
    response.headers["X-Request-ID"] = request_id
    return response

@app.route('/')
def index():
    list_account = get_all_users().get_json()
    formatted_account_list = []
    for account in list_account["data"]:
        formatted_account_list.append(
            {
                "id": account["id"],
                "email": account["email"],
                "full_name": account["full_name"]
            }
        )
    if len(formatted_account_list) < 1:
        return render_template('index.html', list_user=[])
    return render_template('index.html', list_user=formatted_account_list)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def main():
    index()

if __name__ == "__main__":
    main()
