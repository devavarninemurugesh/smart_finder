import re
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import get_db_connection
from backend.auth import create_token, get_current_user, login_required, role_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    campus_id = (data.get("campus_id") or data.get("campusId") or "").strip()
    department = (data.get("department") or "Computer Science").strip()
    password = data.get("password") or ""
    role = (data.get("role") or "student").strip().lower()

    if not name:
        return jsonify({"error": "Full name is required."}), 400
    if not email or not EMAIL_REGEX.match(email):
        return jsonify({"error": "Please enter a valid campus email address."}), 400
    if not campus_id:
        return jsonify({"error": "Campus student/staff ID is required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400
    if role not in ["student", "moderator", "admin"]:
        role = "student"

    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"error": f"An account with email '{email}' already exists."}), 409

    user_id = f"usr-{uuid.uuid4().hex[:8]}"
    initials = "".join([part[0].upper() for part in name.split()[:2]]) or "U"
    hashed = generate_password_hash(password)
    now_iso = datetime.utcnow().isoformat() + "Z"

    cursor.execute("""
    INSERT INTO users (id, name, email, password_hash, role, campus_id, department, phone, contact_pref, notif_pref, avatar, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        name,
        email,
        hashed,
        role,
        campus_id,
        department,
        data.get("phone", ""),
        data.get("contact_pref", "email"),
        1,
        initials,
        now_iso,
    ))

    # Send welcome notification
    cursor.execute("""
    INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"notif-{uuid.uuid4().hex[:8]}",
        user_id,
        "🎉 Welcome to FindIt Portal",
        f"Welcome {name}! Your account has been registered with {role.upper()} privileges.",
        "success",
        0,
        now_iso,
    ))

    # Log audit
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        name,
        "USER_REGISTER",
        email,
        f"Registered new {role} account.",
        now_iso,
    ))

    conn.commit()
    conn.close()

    user_data = {
        "id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "campusId": campus_id,
        "department": department,
        "phone": data.get("phone", ""),
        "avatar": initials,
    }

    session["user"] = user_data
    token = create_token(user_data)

    return jsonify({
        "message": "Account registered successfully!",
        "user": user_data,
        "token": token,
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email:
        return jsonify({"error": "Please enter your campus email."}), 400
    if not password:
        return jsonify({"error": "Please enter your password."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password."}), 401

    user_data = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "campusId": user["campus_id"],
        "department": user["department"],
        "phone": user["phone"] or "",
        "contact_pref": user["contact_pref"] or "email",
        "avatar": user["avatar"] or "U",
    }

    session["user"] = user_data
    token = create_token(user_data)

    return jsonify({
        "message": f"Welcome back, {user['name']}!",
        "user": user_data,
        "token": token,
    })


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Signed out successfully."})


@auth_bp.route("/auth/me", methods=["GET"])
def me():
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False, "user": None})

    conn = get_db_connection()
    db_user = conn.execute("SELECT * FROM users WHERE id = ?", (user["id"],)).fetchone()
    conn.close()

    if not db_user:
        return jsonify({"authenticated": False, "user": None})

    return jsonify({
        "authenticated": True,
        "user": {
            "id": db_user["id"],
            "name": db_user["name"],
            "email": db_user["email"],
            "role": db_user["role"],
            "campusId": db_user["campus_id"],
            "department": db_user["department"],
            "phone": db_user["phone"] or "",
            "contact_pref": db_user["contact_pref"] or "email",
            "notif_pref": db_user["notif_pref"],
            "avatar": db_user["avatar"] or "U",
        },
    })


@auth_bp.route("/auth/profile", methods=["PUT"])
@login_required
def update_profile():
    current_u = get_current_user()
    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    department = (data.get("department") or "").strip()
    phone = (data.get("phone") or "").strip()
    contact_pref = (data.get("contact_pref") or "email").strip()
    notif_pref = 1 if data.get("notif_pref", True) else 0

    if not name:
        return jsonify({"error": "Full name cannot be empty."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET name = ?, department = ?, phone = ?, contact_pref = ?, notif_pref = ?
    WHERE id = ?
    """, (name, department, phone, contact_pref, notif_pref, current_u["id"]))

    conn.commit()

    updated = cursor.execute("SELECT * FROM users WHERE id = ?", (current_u["id"],)).fetchone()
    conn.close()

    user_data = {
        "id": updated["id"],
        "name": updated["name"],
        "email": updated["email"],
        "role": updated["role"],
        "campusId": updated["campus_id"],
        "department": updated["department"],
        "phone": updated["phone"] or "",
        "contact_pref": updated["contact_pref"],
        "avatar": updated["avatar"] or "U",
    }
    session["user"] = user_data

    return jsonify({
        "message": "Profile updated successfully!",
        "user": user_data,
    })


@auth_bp.route("/users", methods=["GET"])
@role_required("admin")
def list_users():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, email, role, campus_id, department, phone, created_at FROM users ORDER BY created_at DESC").fetchall()
    conn.close()

    users_list = [dict(r) for r in rows]
    return jsonify(users_list)


@auth_bp.route("/users/<user_id>/role", methods=["PUT"])
@role_required("admin")
def update_user_role(user_id):
    data = request.get_json() or {}
    new_role = (data.get("role") or "").strip().lower()
    if new_role not in ["student", "moderator", "admin"]:
        return jsonify({"error": "Invalid role. Must be 'student', 'moderator', or 'admin'."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    target = cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
    if not target:
        conn.close()
        return jsonify({"error": "User not found."}), 404

    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))

    current_u = get_current_user()
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        current_u["name"],
        "ROLE_CHANGE",
        target["name"],
        f"Updated role to {new_role.upper()}",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": f"Role updated to {new_role.upper()} successfully."})
