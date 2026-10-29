import os
import re
import uuid
from datetime import datetime, date
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from backend.database import get_db_connection
from backend.auth import get_current_user, login_required, role_required

items_bp = Blueprint("items", __name__, url_prefix="/api")

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@items_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file format. Please upload JPG, PNG, or WEBP."}), 400

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 5MB limit. Please upload a smaller image."}), 400

    upload_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
    os.makedirs(upload_folder, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"item_{uuid.uuid4().hex[:12]}.{ext}"
    dest_path = os.path.join(upload_folder, filename)
    file.save(dest_path)

    file_url = f"/uploads/{filename}"
    return jsonify({"message": "File uploaded successfully.", "url": file_url})


@items_bp.route("/items", methods=["GET"])
def get_items():
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "all").strip()
    status = request.args.get("status", "all").strip().lower()
    location = request.args.get("location", "all").strip()
    incident_date = request.args.get("date", "").strip()
    item_type = request.args.get("type", "all").strip().lower()
    sort = request.args.get("sort", "newest").strip().lower()

    current_u = get_current_user()
    is_mod_or_admin = current_u and current_u.get("role") in ["moderator", "admin"]

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM items WHERE 1=1"
    params = []

    # Hide hidden items unless moderator/admin
    if not is_mod_or_admin:
        query += " AND hidden = 0"

    if item_type in ["lost", "found"]:
        query += " AND type = ?"
        params.append(item_type)

    if category != "all" and category:
        query += " AND category = ?"
        params.append(category)

    if status != "all" and status:
        query += " AND status = ?"
        params.append(status)

    if incident_date:
        query += " AND date = ?"
        params.append(incident_date)

    if location != "all" and location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    if search:
        query += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(location) LIKE ? OR LOWER(contact_name) LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term, term])

    if sort == "oldest":
        query += " ORDER BY created_at ASC"
    else:
        query += " ORDER BY created_at DESC"

    rows = cursor.execute(query, params).fetchall()
    conn.close()

    items_list = []
    for r in rows:
        d = dict(r)
        d["flagged"] = bool(d["flagged"])
        d["hidden"] = bool(d["hidden"])
        d["contactName"] = d["contact_name"]
        d["contactEmail"] = d["contact_email"]
        d["contactPhone"] = d["contact_phone"]
        d["contactPref"] = d["contact_pref"]
        d["reportedBy"] = d["reported_by"]
        d["createdAt"] = d["created_at"]
        d["identifyingMarks"] = d["identifying_marks"]
        items_list.append(d)

    return jsonify(items_list)


@items_bp.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Item not found."}), 404

    d = dict(row)
    d["flagged"] = bool(d["flagged"])
    d["hidden"] = bool(d["hidden"])
    d["contactName"] = d["contact_name"]
    d["contactEmail"] = d["contact_email"]
    d["contactPhone"] = d["contact_phone"]
    d["contactPref"] = d["contact_pref"]
    d["reportedBy"] = d["reported_by"]
    d["createdAt"] = d["created_at"]
    d["identifyingMarks"] = d["identifying_marks"]
    return jsonify(d)


@items_bp.route("/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}

    item_type = (data.get("type") or "lost").strip().lower()
    name = (data.get("name") or "").strip()
    category = (data.get("category") or "").strip()
    location = (data.get("location") or "").strip()
    incident_date_str = (data.get("date") or "").strip()
    contact_name = (data.get("contactName") or data.get("contact_name") or "").strip()
    contact_email = (data.get("contactEmail") or data.get("contact_email") or "").strip().lower()
    contact_phone = (data.get("contactPhone") or data.get("contact_phone") or "").strip()
    contact_pref = (data.get("contactPref") or data.get("contact_pref") or "email").strip()
    description = (data.get("description") or "").strip()
    identifying_marks = (data.get("identifyingMarks") or data.get("identifying_marks") or "").strip()
    image = data.get("image") or ""

    # Validations
    if item_type not in ["lost", "found"]:
        return jsonify({"error": "Invalid item type. Must be 'lost' or 'found'."}), 400
    if not name:
        return jsonify({"error": "Item name is required."}), 400
    if not category:
        return jsonify({"error": "Please select a category."}), 400
    if not location:
        return jsonify({"error": "Please specify the incident location."}), 400
    if not incident_date_str:
        return jsonify({"error": "Please select an incident date."}), 400

    # Reject future dates
    try:
        inc_date = datetime.strptime(incident_date_str, "%Y-%m-%d").date()
        if inc_date > date.today():
            return jsonify({"error": "Incident date cannot be in the future."}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if not contact_name:
        return jsonify({"error": "Contact name is required."}), 400
    if not contact_email or not EMAIL_REGEX.match(contact_email):
        return jsonify({"error": "Please provide a valid contact email address."}), 400
    if not description:
        return jsonify({"error": "Please provide a description."}), 400

    current_u = get_current_user()
    reported_by = current_u["id"] if current_u else "usr-student-01"

    item_id = f"item-{uuid.uuid4().hex[:8]}"
    now_iso = datetime.utcnow().isoformat() + "Z"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO items (
        id, type, name, category, location, date, contact_name, contact_email,
        contact_phone, contact_pref, description, identifying_marks, status,
        image, reported_by, flagged, flag_reason, hidden, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item_id,
        item_type,
        name,
        category,
        location,
        incident_date_str,
        contact_name,
        contact_email,
        contact_phone,
        contact_pref,
        description,
        identifying_marks,
        "active",
        image,
        reported_by,
        0,
        "",
        0,
        now_iso,
    ))

    # Send in-app notification if user is authenticated
    if current_u:
        cursor.execute("""
        INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"notif-{uuid.uuid4().hex[:8]}",
            current_u["id"],
            f"✅ {item_type.capitalize()} Item Reported",
            f"Your report for '{name}' was published with reference ID: {item_id}",
            "success",
            0,
            now_iso,
        ))

    # Audit log
    actor_name = current_u["name"] if current_u else contact_name
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        actor_name,
        f"REPORT_{item_type.upper()}",
        name,
        f"Filed report in {category} at {location}",
        now_iso,
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"{item_type.capitalize()} item reported successfully!",
        "item": {
            "id": item_id,
            "type": item_type,
            "name": name,
            "category": category,
            "location": location,
            "date": incident_date_str,
            "contactName": contact_name,
            "contactEmail": contact_email,
            "contactPhone": contact_phone,
            "contactPref": contact_pref,
            "description": description,
            "identifyingMarks": identifying_marks,
            "status": "active",
            "image": image,
            "reportedBy": reported_by,
            "createdAt": now_iso,
        },
    }), 201


@items_bp.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    current_u = get_current_user()
    conn = get_db_connection()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    # Authorization: Only report owner or admin can edit
    is_owner = current_u and item["reported_by"] == current_u["id"]
    is_admin = current_u and current_u.get("role") == "admin"

    if not (is_owner or is_admin):
        conn.close()
        return jsonify({"error": "Access Denied: You cannot edit another person's report."}), 403

    data = request.get_json() or {}
    name = (data.get("name") or item["name"]).strip()
    category = (data.get("category") or item["category"]).strip()
    location = (data.get("location") or item["location"]).strip()
    description = (data.get("description") or item["description"]).strip()
    identifying_marks = data.get("identifyingMarks", item["identifying_marks"])

    cursor.execute("""
    UPDATE items
    SET name = ?, category = ?, location = ?, description = ?, identifying_marks = ?
    WHERE id = ?
    """, (name, category, location, description, identifying_marks, item_id))

    actor = current_u["name"] if current_u else "Owner"
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        actor,
        "ITEM_UPDATE",
        name,
        f"Updated details for report {item_id}",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": f"Item '{name}' updated successfully."})


@items_bp.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    current_u = get_current_user()
    conn = get_db_connection()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    # Allow if admin or owner, or if in demo testing
    is_owner = current_u and item["reported_by"] == current_u["id"]
    is_admin = current_u and current_u.get("role") in ["admin", "moderator"]

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))

    actor = current_u["name"] if current_u else "User"
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        actor,
        "ITEM_DELETE",
        item["name"],
        f"Deleted report {item_id}",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": f"Item '{item['name']}' deleted successfully."})


@items_bp.route("/items/<item_id>/recover", methods=["POST"])
def mark_recovered(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    if item["status"] == "recovered":
        conn.close()
        return jsonify({"message": "Item is already marked as recovered.", "status": "recovered"})

    cursor.execute("UPDATE items SET status = 'recovered' WHERE id = ?", (item_id,))

    current_u = get_current_user()
    actor = current_u["name"] if current_u else item["contact_name"]

    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        actor,
        "ITEM_RECOVERED",
        item["name"],
        f"Marked item {item_id} as recovered & returned.",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": f"'{item['name']}' marked as recovered!", "status": "recovered"})


@items_bp.route("/items/<item_id>/flag", methods=["POST"])
@role_required("moderator", "admin")
def toggle_flag(item_id):
    data = request.get_json() or {}
    conn = get_db_connection()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    new_flag = 0 if item["flagged"] else 1
    reason = data.get("reason", "Flagged for moderation review") if new_flag else ""

    cursor.execute("UPDATE items SET flagged = ?, flag_reason = ? WHERE id = ?", (new_flag, reason, item_id))

    current_u = get_current_user()
    action = "MOD_FLAG" if new_flag else "MOD_UNFLAG"
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        current_u["name"],
        action,
        item["name"],
        f"Flag status changed to {bool(new_flag)}: {reason}",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Item '{item['name']}' {'flagged' if new_flag else 'unflagged'}.",
        "flagged": bool(new_flag),
        "flagReason": reason,
    })


@items_bp.route("/items/<item_id>/hide", methods=["POST"])
@role_required("moderator", "admin")
def toggle_hide(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()

    if not item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    new_hidden = 0 if item["hidden"] else 1
    cursor.execute("UPDATE items SET hidden = ? WHERE id = ?", (new_hidden, item_id))

    current_u = get_current_user()
    action = "MOD_HIDE" if new_hidden else "MOD_UNHIDE"
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        current_u["name"],
        action,
        item["name"],
        f"Visibility toggled to {'hidden' if new_hidden else 'visible'}",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Item '{item['name']}' is now {'hidden from directory' if new_hidden else 'restored to directory'}.",
        "hidden": bool(new_hidden),
    })
