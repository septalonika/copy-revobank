import copy

from models.account import list_account_db

def all_accounts_repository():
    return copy.deepcopy(list_account_db)
