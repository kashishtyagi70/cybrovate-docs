import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Any

from fastapi import Request


SESSION_COOKIE_NAME = "docs_portal_session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 8
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-for-local-development")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 260_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False

    try:
        algorithm, salt, expected_hash = password_hash.split("$", 2)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 260_000)
    return hmac.compare_digest(digest.hex(), expected_hash)


def _sign(payload: str) -> str:
    return hmac.new(SECRET_KEY.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()


def create_session_token(user_id: int) -> str:
    payload: dict[str, Any] = {
        "user_id": user_id,
        "expires_at": int(time.time()) + SESSION_MAX_AGE_SECONDS,
    }
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8")).decode("utf-8")
    return f"{encoded_payload}.{_sign(encoded_payload)}"


def read_session_user_id(request: Request) -> int | None:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token or "." not in token:
        return None

    encoded_payload, signature = token.rsplit(".", 1)
    if not hmac.compare_digest(_sign(encoded_payload), signature):
        return None

    try:
        payload = json.loads(base64.urlsafe_b64decode(encoded_payload.encode("utf-8")))
    except (ValueError, json.JSONDecodeError):
        return None

    if int(payload.get("expires_at", 0)) < int(time.time()):
        return None

    user_id = payload.get("user_id")
    return int(user_id) if user_id is not None else None
