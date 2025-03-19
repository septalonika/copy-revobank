import copy

from models.transaction import list_transaction_db

def all_transactions_repository():
    return copy.deepcopy(list_transaction_db)