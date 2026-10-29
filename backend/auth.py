import base64
import json
import hmac
import hashlib
import time
from functools import wraps
from flask import request, jsonify, session
from backend.database import get_db_connection

SECRET_KEY = "findit_campus_super_secret_key_2026"


def create_token(user_data):
    """Creates a lightweight, signed tamper-proof token containing user info."""
    payload = {
        "id": user_data["id"],
        "email": user_data["email"],
        "name": user_data["name"],
        "role": user_data["role"],
        "exp": int(time.time()) + 86400 * 7,  # 7 days
    }
    payload_str = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(SECRET_KEY.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
    return f"{payload_str}.{signature}"


def verify_token(token_str):
    """Verifies the signature and expiration of the token."""
    try:
        parts = token_str.split(".")
        if len(parts) != 2:
            return None
        payload_str, signature = parts
        expected_sig = hmac.new(SECRET_KEY.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(payload_str.encode()).decode())
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None


def get_current_user():
    """Extracts the authenticated user from the session, header, or query param."""
    # 1. Check Flask session
    if "user" in session:
        return session["user"]

    # 2. Check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if payload:
            return payload

    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required. Please sign in."}), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({"error": "Authentication required. Please sign in."}), 401
            if user.get("role") not in allowed_roles:
                return jsonify({
                    "error": f"Access Denied: Requires one of [{', '.join(allowed_roles)}] privileges."
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
