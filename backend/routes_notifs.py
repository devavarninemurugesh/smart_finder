from flask import Blueprint, request, jsonify
from backend.database import get_db_connection
from backend.auth import get_current_user

notifs_bp = Blueprint("notifications", __name__, url_prefix="/api")


@notifs_bp.route("/notifications", methods=["GET"])
def get_notifications():
    current_u = get_current_user()
    conn = get_db_connection()

    if current_u:
        rows = conn.execute(
            "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC",
            (current_u["id"],),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM notifications ORDER BY created_at DESC"
        ).fetchall()

    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        d["userId"] = d["user_id"]
        d["isRead"] = bool(d["is_read"])
        d["createdAt"] = d["created_at"]
        result.append(d)

    return jsonify(result)


@notifs_bp.route("/notifications/<notif_id>/read", methods=["POST"])
def mark_notification_read(notif_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Notification marked as read."})


@notifs_bp.route("/notifications/read-all", methods=["POST"])
def mark_all_read():
    current_u = get_current_user()
    conn = get_db_connection()
    cursor = conn.cursor()

    if current_u:
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (current_u["id"],))
    else:
        cursor.execute("UPDATE notifications SET is_read = 1")

    conn.commit()
    conn.close()
    return jsonify({"message": "All notifications marked as read."})
