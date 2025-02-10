import hashlib
from uuid import uuid4

from fastapi import HTTPException

from config import SECRET_KEY


def generate_signature(data: dict):
    concat_data = f"{data['account_id']}{data['amount']}{data['transaction_id']}{data['user_id']}{SECRET_KEY}"
    signature = hashlib.sha256(concat_data.encode()).hexdigest()
    return signature


def check_signature(data: dict):
    expected_signature = generate_signature(data)

    if data["signature"] != expected_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")


def generate_random_transaction_id():
    return str(uuid4())
