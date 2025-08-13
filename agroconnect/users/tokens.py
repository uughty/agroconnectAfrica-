# users/tokens.py
from django.core import signing
from time import time

SIGNING_SALT = "users.email.verify"

def make_email_token(user_id: int) -> str:
    data = {"uid": user_id, "ts": int(time())}
    return signing.dumps(data, salt=SIGNING_SALT)

def read_email_token(token: str, max_age_seconds: int = 60 * 60 * 24 * 3) -> int | None:
    try:
        data = signing.loads(token, salt=SIGNING_SALT, max_age=max_age_seconds)
        return int(data["uid"])
    except Exception:
        return None
