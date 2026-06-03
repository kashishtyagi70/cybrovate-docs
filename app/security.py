from datetime import UTC, datetime, timedelta
import base64
import hashlib
import hmac
from typing import Any

import bcrypt
import jwt
from fastapi import Request

from app.database import SECRET_KEY


SESSION_COOKIE_NAME = "docs_portal_session"
SESSION_MAX_AGE_SECONDS = 60 * 60 * 8
JWT_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return False
    if password_hash.startswith("$2"):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except ValueError:
            return False
    if password_hash.startswith("pbkdf2_sha256$"):
        return verify_django_pbkdf2_sha256(password, password_hash)
    if password_hash.startswith("pbkdf2:sha256:"):
        return verify_werkzeug_pbkdf2_sha256(password, password_hash)
    return False


def verify_django_pbkdf2_sha256(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, encoded_hash = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iterations))
        calculated_hash = base64.b64encode(digest).decode("ascii").strip()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(calculated_hash, encoded_hash)


def verify_werkzeug_pbkdf2_sha256(password: str, password_hash: str) -> bool:
    try:
        method, salt, encoded_hash = password_hash.split("$", 2)
        _, digest_name, iterations = method.split(":", 2)
        if digest_name != "sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iterations))
        calculated_hash = digest.hex()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(calculated_hash, encoded_hash)


def create_access_token(user_id: int, role: str, expires_delta: timedelta | None = None) -> str:
    expires_at = datetime.now(UTC) + (expires_delta or timedelta(seconds=SESSION_MAX_AGE_SECONDS))
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


def read_session_user_id(request: Request) -> int | None:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None

    payload = decode_access_token(token)
    if payload is None:
        return None

    subject = payload.get("sub")
    return int(subject) if subject is not None else None
