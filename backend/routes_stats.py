import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.database import get_db_connection, reset_demo_db, DEFAULT_CATEGORIES
from backend.auth import get_current_user, role_required

stats_bp = Blueprint("stats", __name__, url_prefix="/api")


@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    total_lost = cursor.execute("SELECT COUNT(*) FROM items WHERE type = 'lost'").fetchone()[0]
    total_found = cursor.execute("SELECT COUNT(*) FROM items WHERE type = 'found'").fetchone()[0]
    total_recovered = cursor.execute("SELECT COUNT(*) FROM items WHERE status = 'recovered'").fetchone()[0]
    active_cases = cursor.execute("SELECT COUNT(*) FROM items WHERE status IN ('active', 'claim_pending')").fetchone()[0]
    pending_claims = cursor.execute("SELECT COUNT(*) FROM claims WHERE status = 'pending'").fetchone()[0]
    total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    # Category distribution
    cat_rows = cursor.execute("""
    SELECT category, COUNT(*) as cnt FROM items GROUP BY category ORDER BY cnt DESC
    """).fetchall()
    category_distribution = {r["category"]: r["cnt"] for r in cat_rows}

    # Status distribution
    status_rows = cursor.execute("""
    SELECT status, COUNT(*) as cnt FROM items GROUP BY status
    """).fetchall()
    status_distribution = {r["status"]: r["cnt"] for r in status_rows}

    # Recent activity logs
    logs_rows = cursor.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 10").fetchall()
    recent_activity = [dict(r) for r in logs_rows]

    conn.close()

    return jsonify({
        "totalLost": total_lost,
        "totalFound": total_found,
        "totalRecovered": total_recovered,
        "activeCases": active_cases,
        "pendingClaims": pending_claims,
        "totalUsers": total_users,
        "categoryDistribution": category_distribution,
        "statusDistribution": status_distribution,
        "recentActivity": recent_activity,
    })


@stats_bp.route("/categories", methods=["GET"])
def get_categories():
    conn = get_db_connection()
    rows = conn.execute("SELECT name FROM categories ORDER BY id ASC").fetchall()
    conn.close()
    return jsonify([r["name"] for r in rows])


@stats_bp.route("/categories", methods=["POST"])
@role_required("admin")
def add_category():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Category name is required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    existing = cursor.execute("SELECT id FROM categories WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"error": f"Category '{name}' already exists."}), 409

    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

    current_u = get_current_user()
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        current_u["name"],
        "ADD_CATEGORY",
        name,
        f"Created new item category '{name}'.",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": f"Category '{name}' added successfully.", "name": name}), 201


@stats_bp.route("/logs", methods=["GET"])
@role_required("admin", "moderator")
def get_audit_logs():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@stats_bp.route("/reset-demo", methods=["POST"])
def reset_demo():
    reset_demo_db()
    return jsonify({"message": "Application demo data reset to clean state successfully."})
