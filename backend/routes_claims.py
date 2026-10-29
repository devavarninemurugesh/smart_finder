import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.database import get_db_connection
from backend.auth import get_current_user, login_required, role_required

claims_bp = Blueprint("claims", __name__, url_prefix="/api")


@claims_bp.route("/claims", methods=["GET"])
def get_claims():
    current_u = get_current_user()
    conn = get_db_connection()

    if current_u and current_u.get("role") in ["admin", "moderator"]:
        rows = conn.execute("SELECT * FROM claims ORDER BY created_at DESC").fetchall()
    elif current_u:
        rows = conn.execute("SELECT * FROM claims WHERE claimant_id = ? ORDER BY created_at DESC", (current_u["id"],)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM claims ORDER BY created_at DESC").fetchall()

    conn.close()

    claims_list = []
    for r in rows:
        d = dict(r)
        d["itemId"] = d["item_id"]
        d["itemName"] = d["item_name"]
        d["claimantId"] = d["claimant_id"]
        d["claimantName"] = d["claimant_name"]
        d["claimantEmail"] = d["claimant_email"]
        d["claimantPhone"] = d["claimant_phone"]
        d["adminNotes"] = d["admin_notes"]
        d["createdAt"] = d["created_at"]
        claims_list.append(d)

    return jsonify(claims_list)


@claims_bp.route("/claims", methods=["POST"])
def submit_claim():
    data = request.get_json() or {}

    item_id = (data.get("itemId") or data.get("item_id") or "").strip()
    claimant_name = (data.get("claimantName") or data.get("claimant_name") or "").strip()
    claimant_email = (data.get("claimantEmail") or data.get("claimant_email") or "").strip().lower()
    claimant_phone = (data.get("claimantPhone") or data.get("claimant_phone") or "").strip()
    proof = (data.get("proof") or "").strip()

    if not item_id:
        return jsonify({"error": "Item ID is required."}), 400
    if not claimant_name:
        return jsonify({"error": "Claimant full name is required."}), 400
    if not claimant_email:
        return jsonify({"error": "Claimant email is required."}), 400
    if not claimant_phone:
        return jsonify({"error": "Claimant phone number is required."}), 400
    if not proof:
        return jsonify({"error": "Please provide proof of ownership and identifying clues."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    item = cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if not item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    # Prevent claiming an already recovered or closed item
    if item["status"] in ["recovered", "closed"]:
        conn.close()
        return jsonify({"error": f"Cannot submit a claim for an item that is already {item['status']}."}), 400

    current_u = get_current_user()
    claimant_id = current_u["id"] if current_u else "usr-student-01"

    claim_id = f"claim-{uuid.uuid4().hex[:8]}"
    now_iso = datetime.utcnow().isoformat() + "Z"

    # Insert claim
    cursor.execute("""
    INSERT INTO claims (
        id, item_id, item_name, claimant_id, claimant_name, claimant_email,
        claimant_phone, proof, status, admin_notes, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        claim_id,
        item_id,
        item["name"],
        claimant_id,
        claimant_name,
        claimant_email,
        claimant_phone,
        proof,
        "pending",
        "",
        now_iso,
    ))

    # Update item status to claim_pending if active
    cursor.execute("UPDATE items SET status = 'claim_pending' WHERE id = ?", (item_id,))

    # Notify finder / reporter
    if item["reported_by"]:
        cursor.execute("""
        INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"notif-{uuid.uuid4().hex[:8]}",
            item["reported_by"],
            "📬 New Ownership Claim Received",
            f"Someone has filed an ownership claim for your found report '{item['name']}'. It is currently under administrator review.",
            "info",
            0,
            now_iso,
        ))

    # Notify claimant
    cursor.execute("""
    INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"notif-{uuid.uuid4().hex[:8]}",
        claimant_id,
        "⏳ Claim Submitted Successfully",
        f"Your ownership claim for '{item['name']}' has been registered and sent to campus administration for verification.",
        "success",
        0,
        now_iso,
    ))

    # Audit log
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        claimant_name,
        "CLAIM_SUBMIT",
        item["name"],
        f"Filed verification claim with {len(proof)} chars of proof.",
        now_iso,
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Claim for '{item['name']}' submitted successfully! Awaiting administrator verification.",
        "claim": {
            "id": claim_id,
            "itemId": item_id,
            "itemName": item["name"],
            "claimantId": claimant_id,
            "claimantName": claimant_name,
            "claimantEmail": claimant_email,
            "claimantPhone": claimant_phone,
            "proof": proof,
            "status": "pending",
            "createdAt": now_iso,
        },
    }), 201


@claims_bp.route("/claims/<claim_id>/approve", methods=["POST"])
@role_required("admin")
def approve_claim(claim_id):
    data = request.get_json() or {}
    notes = data.get("adminNotes") or data.get("admin_notes") or "Verified successfully. Please collect item at Campus Security."

    conn = get_db_connection()
    cursor = conn.cursor()

    claim = cursor.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
    if not claim:
        conn.close()
        return jsonify({"error": "Claim not found."}), 404

    now_iso = datetime.utcnow().isoformat() + "Z"
    current_u = get_current_user()

    # Update claim
    cursor.execute("UPDATE claims SET status = 'approved', admin_notes = ? WHERE id = ?", (notes, claim_id))

    # Update corresponding item to recovered
    cursor.execute("UPDATE items SET status = 'recovered' WHERE id = ?", (claim["item_id"],))

    # Send in-app notification to claimant
    cursor.execute("""
    INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"notif-{uuid.uuid4().hex[:8]}",
        claim["claimant_id"],
        "🎉 Ownership Claim Approved!",
        f"Your claim for '{claim['item_name']}' has been approved! {notes}",
        "success",
        0,
        now_iso,
    ))

    # Audit log
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        current_u["name"],
        "CLAIM_APPROVE",
        claim["item_name"],
        f"Approved claim {claim_id}: {notes}",
        now_iso,
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Claim for '{claim['item_name']}' approved! Item marked as recovered and claimant notified.",
        "status": "approved",
    })


@claims_bp.route("/claims/<claim_id>/reject", methods=["POST"])
@role_required("admin")
def reject_claim(claim_id):
    data = request.get_json() or {}
    notes = data.get("adminNotes") or data.get("admin_notes") or "Insufficient identifying proof provided."

    conn = get_db_connection()
    cursor = conn.cursor()

    claim = cursor.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
    if not claim:
        conn.close()
        return jsonify({"error": "Claim not found."}), 404

    now_iso = datetime.utcnow().isoformat() + "Z"
    current_u = get_current_user()

    # Update claim
    cursor.execute("UPDATE claims SET status = 'rejected', admin_notes = ? WHERE id = ?", (notes, claim_id))

    # Reset item back to active if no other pending claims
    pending = cursor.execute("SELECT COUNT(*) FROM claims WHERE item_id = ? AND status = 'pending' AND id != ?", (claim["item_id"], claim_id)).fetchone()[0]
    if pending == 0:
        cursor.execute("UPDATE items SET status = 'active' WHERE id = ? AND status = 'claim_pending'", (claim["item_id"],))

    # Send in-app notification to claimant
    cursor.execute("""
    INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        f"notif-{uuid.uuid4().hex[:8]}",
        claim["claimant_id"],
        "❌ Ownership Claim Rejected",
        f"Your claim for '{claim['item_name']}' was reviewed and rejected. Reason: {notes}",
        "error",
        0,
        now_iso,
    ))

    # Audit log
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        f"log-{uuid.uuid4().hex[:8]}",
        current_u["name"],
        "CLAIM_REJECT",
        claim["item_name"],
        f"Rejected claim {claim_id}: {notes}",
        now_iso,
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Claim for '{claim['item_name']}' rejected.",
        "status": "rejected",
    })
