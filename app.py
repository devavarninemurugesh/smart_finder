import os
from flask import Flask, send_from_directory, jsonify
from backend.database import init_db, DB_PATH, reset_demo_db
from backend.routes_auth import auth_bp
from backend.routes_items import items_bp
from backend.routes_claims import claims_bp
from backend.routes_notifs import notifs_bp
from backend.routes_stats import stats_bp

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
WEBSITE_DIR = os.path.join(PROJECT_ROOT, "website")
UPLOADS_DIR = os.path.join(PROJECT_ROOT, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

app = Flask(__name__, static_folder=WEBSITE_DIR)
app.secret_key = "findit_campus_flask_session_secret_2026"
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024  # 6 MB

# Register API blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(claims_bp)
app.register_blueprint(notifs_bp)
app.register_blueprint(stats_bp)


# Serve Static Website Files
@app.route("/")
def index():
    return send_from_directory(WEBSITE_DIR, "index.html")


@app.route("/<path:path>")
def serve_website_files(path):
    if os.path.exists(os.path.join(WEBSITE_DIR, path)):
        return send_from_directory(WEBSITE_DIR, path)
    return send_from_directory(WEBSITE_DIR, "index.html")


# Serve Uploaded Images
@app.route("/uploads/<path:filename>")
def serve_uploads(filename):
    return send_from_directory(UPLOADS_DIR, filename)


# Global Error Handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify({"error": "File size exceeds 5MB limit. Please upload a smaller file."}), 413


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error occurred."}), 500


def create_app():
    if not os.path.exists(DB_PATH):
        init_db()
        reset_demo_db()
    else:
        init_db()
    return app


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        reset_demo_db()
    else:
        init_db()
    print("=" * 60)
    print("  FindIt – Smart Lost & Found Management Portal")
    print("  Serving at: http://127.0.0.1:5000")
    print("  Database:   SQLite (findit.db)")
    print("  Demo Users: student@campus.edu   / Student@123")
    print("              moderator@campus.edu / Mod@123")
    print("              admin@campus.edu     / Admin@123")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
