import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "findit.db"))

DEFAULT_CATEGORIES = [
    "ID Cards",
    "Mobile Phones",
    "Laptops",
    "Bags",
    "Books",
    "Keys",
    "Water Bottles",
    "Watches",
    "Accessories",
    "Other",
]


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('student', 'moderator', 'admin')),
        campus_id TEXT,
        department TEXT,
        phone TEXT,
        contact_pref TEXT DEFAULT 'email',
        notif_pref INTEGER DEFAULT 1,
        avatar TEXT,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL CHECK(type IN ('lost', 'found')),
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        location TEXT NOT NULL,
        date TEXT NOT NULL,
        contact_name TEXT NOT NULL,
        contact_email TEXT NOT NULL,
        contact_phone TEXT,
        contact_pref TEXT DEFAULT 'email',
        description TEXT NOT NULL,
        identifying_marks TEXT,
        status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'claim_pending', 'recovered', 'closed')),
        image TEXT,
        reported_by TEXT NOT NULL,
        flagged INTEGER DEFAULT 0,
        flag_reason TEXT DEFAULT '',
        hidden INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (reported_by) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS claims (
        id TEXT PRIMARY KEY,
        item_id TEXT NOT NULL,
        item_name TEXT NOT NULL,
        claimant_id TEXT NOT NULL,
        claimant_name TEXT NOT NULL,
        claimant_email TEXT NOT NULL,
        claimant_phone TEXT NOT NULL,
        proof TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
        admin_notes TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE,
        FOREIGN KEY (claimant_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS notifications (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT DEFAULT 'info',
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS audit_logs (
        id TEXT PRIMARY KEY,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        target TEXT NOT NULL,
        details TEXT,
        created_at TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()


def reset_demo_db():
    """Resets the SQLite database to clean, realistic Indian college campus demo data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables
    cursor.executescript("""
    DROP TABLE IF EXISTS audit_logs;
    DROP TABLE IF EXISTS notifications;
    DROP TABLE IF EXISTS claims;
    DROP TABLE IF EXISTS items;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS users;
    """)
    conn.commit()
    conn.close()

    init_db()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Seed Categories
    for cat in DEFAULT_CATEGORIES:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (cat,))

    # Seed Predefined Users with PBKDF2 Hashes
    users_data = [
        (
            "usr-student-01",
            "Dev Anand",
            "student@campus.edu",
            generate_password_hash("Student@123"),
            "student",
            "22BCS108",
            "Computer Science",
            "+91 98765 43210",
            "email",
            1,
            "DA",
            "2026-09-01T08:00:00.000Z",
        ),
        (
            "usr-mod-01",
            "Prof. Sarah Jenkins",
            "moderator@campus.edu",
            generate_password_hash("Mod@123"),
            "moderator",
            "FAC-SAFE-04",
            "Campus Safety & Discipline",
            "+91 98451 22334",
            "phone",
            1,
            "SJ",
            "2026-08-15T09:30:00.000Z",
        ),
        (
            "usr-admin-01",
            "Chief Administrator",
            "admin@campus.edu",
            generate_password_hash("Admin@123"),
            "admin",
            "ADM-DIR-01",
            "Campus Administration & Registry",
            "+91 98111 00223",
            "email",
            1,
            "CA",
            "2026-08-01T10:00:00.000Z",
        ),
    ]

    cursor.executemany("""
    INSERT INTO users (id, name, email, password_hash, role, campus_id, department, phone, contact_pref, notif_pref, avatar, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, users_data)

    # Realistic Sample SVG images for campus items
    sample_images = {
        "laptop": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%231e293b"/%3E%3Crect x="60" y="30" width="280" height="155" rx="8" fill="%230f172a" stroke="%2338bdf8" stroke-width="4"/%3E%3Crect x="75" y="45" width="250" height="125" rx="4" fill="%230284c7" fill-opacity="0.2"/%3E%3Cpath d="M185 95 L215 95 L200 125 Z" fill="%2338bdf8"/%3E%3Ctext x="200" y="150" fill="%23ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle"%3EDell XPS 15 (Silver)%3C/text%3E%3Cpath d="M40 190 L360 190 L380 205 L20 205 Z" fill="%2364748b"/%3E%3Crect x="170" y="192" width="60" height="6" rx="3" fill="%2394a3b8"/%3E%3C/svg%3E',
        "phone": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%230f172a"/%3E%3Crect x="140" y="15" width="120" height="210" rx="20" fill="%231e293b" stroke="%236366f1" stroke-width="3"/%3E%3Crect x="148" y="25" width="104" height="190" rx="14" fill="%23312e81" fill-opacity="0.3"/%3E%3Ccircle cx="200" cy="35" r="4" fill="%2394a3b8"/%3E%3Ctext x="200" y="125" fill="%23e0e7ff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle"%3EOnePlus 11 5G%3C/text%3E%3Ctext x="200" y="145" fill="%23a5b4fc" font-family="sans-serif" font-size="10" text-anchor="middle"%3EEmerald Green%3C/text%3E%3C/svg%3E',
        "idcard": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%231e1e24"/%3E%3Crect x="80" y="30" width="240" height="170" rx="10" fill="%23ffffff" stroke="%233b82f6" stroke-width="4"/%3E%3Crect x="80" y="30" width="240" height="40" rx="10" fill="%231d4ed8"/%3E%3Ctext x="200" y="55" fill="%23ffffff" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle"%3ERATHINAM CAMPUS ID%3C/text%3E%3Crect x="100" y="85" width="55" height="70" rx="4" fill="%23cbd5e1" stroke="%2394a3b8"/%3E%3Ccircle cx="127" cy="110" r="16" fill="%2364748b"/%3E%3Cpath d="M107 148 C107 130, 147 130, 147 148 Z" fill="%2364748b"/%3E%3Ctext x="175" y="105" fill="%230f172a" font-family="sans-serif" font-size="14" font-weight="bold"%3ERahul Verma%3C/text%3E%3Ctext x="175" y="125" fill="%23475569" font-family="sans-serif" font-size="11"%3EDept: B.Tech CSE%3C/text%3E%3Ctext x="175" y="145" fill="%23475569" font-family="sans-serif" font-size="11"%3EID: 22BCS108%3C/text%3E%3Crect x="100" y="170" width="200" height="15" fill="%230f172a"/%3E%3C/svg%3E',
        "wallet": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%231c1917"/%3E%3Crect x="90" y="45" width="220" height="145" rx="14" fill="%2378350f" stroke="%2392400e" stroke-width="4"/%3E%3Cpath d="M90 100 Q200 120 310 100" stroke="%23b45309" stroke-width="2" stroke-dasharray="6,4" fill="none"/%3E%3Crect x="250" y="90" width="60" height="40" rx="8" fill="%2392400e" stroke="%23f59e0b" stroke-width="2"/%3E%3Ccircle cx="265" cy="110" r="6" fill="%23f59e0b"/%3E%3Ctext x="170" y="150" fill="%23fef3c7" font-family="sans-serif" font-size="13" font-weight="bold"%3EWildcraft Wallet%3C/text%3E%3C/svg%3E',
        "watch": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%230f172a"/%3E%3Crect x="175" y="10" width="50" height="220" rx="8" fill="%2378350f"/%3E%3Ccircle cx="200" cy="120" r="60" fill="%231e293b" stroke="%2338bdf8" stroke-width="5"/%3E%3Ccircle cx="200" cy="120" r="50" fill="%230f172a"/%3E%3Cline x1="200" y1="120" x2="200" y2="85" stroke="%23ffffff" stroke-width="3" stroke-linecap="round"/%3E%3Cline x1="200" y1="120" x2="225" y2="120" stroke="%2338bdf8" stroke-width="3" stroke-linecap="round"/%3E%3Ccircle cx="200" cy="120" r="4" fill="%2338bdf8"/%3E%3Ctext x="200" y="150" fill="%2394a3b8" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle"%3ETITAN NEO%3C/text%3E%3C/svg%3E',
        "bottle": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%23042f2e"/%3E%3Crect x="160" y="20" width="80" height="200" rx="20" fill="%230f766e" stroke="%232dd4bf" stroke-width="3"/%3E%3Crect x="175" y="10" width="50" height="20" rx="6" fill="%23134e4a" stroke="%232dd4bf" stroke-width="2"/%3E%3Ctext x="200" y="125" fill="%23ccfbf1" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle"%3EMILTON 750ml%3C/text%3E%3Ctext x="200" y="145" fill="%2399f6e4" font-family="sans-serif" font-size="10" text-anchor="middle"%3EThermosteel Silver%3C/text%3E%3C/svg%3E',
        "calculator": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%230f172a"/%3E%3Crect x="130" y="20" width="140" height="200" rx="12" fill="%231e293b" stroke="%23f59e0b" stroke-width="3"/%3E%3Crect x="145" y="35" width="110" height="40" rx="4" fill="%2378350f" fill-opacity="0.3" stroke="%23d97706"/%3E%3Ctext x="200" y="60" fill="%23fef3c7" font-family="monospace" font-size="16" font-weight="bold" text-anchor="middle"%3Efx-991EX%3C/text%3E%3Ccircle cx="160" cy="100" r="10" fill="%23334155"/%3E%3Ccircle cx="200" cy="100" r="10" fill="%23334155"/%3E%3Ccircle cx="240" cy="100" r="10" fill="%23334155"/%3E%3Ccircle cx="160" cy="130" r="10" fill="%23334155"/%3E%3Ccircle cx="200" cy="130" r="10" fill="%23334155"/%3E%3Ccircle cx="240" cy="130" r="10" fill="%23334155"/%3E%3Ccircle cx="160" cy="160" r="10" fill="%23334155"/%3E%3Ccircle cx="200" cy="160" r="10" fill="%23334155"/%3E%3Ccircle cx="240" cy="160" r="10" fill="%23334155"/%3E%3Crect x="145" y="185" width="110" height="20" rx="6" fill="%23f59e0b"/%3E%3Ctext x="200" y="200" fill="%23000000" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle"%3ECASIO ClassWiz%3C/text%3E%3C/svg%3E',
        "notebook": 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%23064e3b"/%3E%3Crect x="110" y="30" width="180" height="180" rx="8" fill="%2310b981" stroke="%23059669" stroke-width="4"/%3E%3Crect x="95" y="35" width="20" height="170" rx="4" fill="%23cbd5e1" stroke="%2364748b" stroke-width="2"/%3E%3Cline x1="140" y1="65" x2="260" y2="65" stroke="%23064e3b" stroke-width="3" stroke-linecap="round"/%3E%3Cline x1="140" y1="85" x2="240" y2="85" stroke="%23064e3b" stroke-width="2" stroke-linecap="round"/%3E%3Ctext x="200" y="130" fill="%23ffffff" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle"%3EDSA LAB NOTES%3C/text%3E%3Ctext x="200" y="150" fill="%23d1fae5" font-family="sans-serif" font-size="11" text-anchor="middle"%3ETrees & Graphs (CSE)%3C/text%3E%3C/svg%3E',
    }

    # Seed Indian Campus Sample Items
    items_data = [
        (
            "item-101",
            "lost",
            "Dell XPS 15 Laptop (Silver)",
            "Laptops",
            "Central Library 2nd Floor Reading Room",
            "2026-10-24",
            "Dev Anand",
            "student@campus.edu",
            "+91 98765 43210",
            "email",
            "Silver aluminum body with a GitHub sticker on the back cover. Left in carrel table #14.",
            "GitHub Octocat sticker and small scratch on left palm rest.",
            "active",
            sample_images["laptop"],
            "usr-student-01",
            0,
            "",
            0,
            "2026-10-24T10:30:00.000Z",
        ),
        (
            "item-102",
            "found",
            "Casio Scientific Calculator fx-991EX",
            "Accessories",
            "Computer Lab 3, Row B",
            "2026-10-25",
            "Priya Sharma",
            "priyasharma@campus.edu",
            "+91 99887 76655",
            "phone",
            "ClassWiz edition with black protective slide cover. Left near terminal 24.",
            "Has student roll number ending in 891B written in silver marker inside cover.",
            "active",
            sample_images["calculator"],
            "usr-student-01",
            0,
            "",
            0,
            "2026-10-25T14:15:00.000Z",
        ),
        (
            "item-103",
            "lost",
            "Student ID Card - CSE Department",
            "ID Cards",
            "Campus Cafeteria Counter",
            "2026-10-22",
            "Rahul Verma",
            "rahul.cse@campus.edu",
            "+91 97766 55443",
            "email",
            "Rathinam institution barcode ID with blue lanyard. Belongs to 3rd year CSE.",
            "Barcode 22BCS108 with blue Rathinam branded neck strap.",
            "recovered",
            sample_images["idcard"],
            "usr-student-01",
            0,
            "",
            0,
            "2026-10-22T09:00:00.000Z",
        ),
        (
            "item-104",
            "found",
            "Brown Leather Wallet with Bus Pass",
            "Bags",
            "Sports Complex Bleachers",
            "2026-10-26",
            "Coach Kumar",
            "sports.dept@campus.edu",
            "+91 98451 22334",
            "phone",
            "Contains campus transportation smart card, some change, and gym pass.",
            "Rathinam bus pass route 14 inside card sleeve.",
            "active",
            sample_images["wallet"],
            "usr-mod-01",
            0,
            "",
            0,
            "2026-10-26T17:40:00.000Z",
        ),
        (
            "item-105",
            "lost",
            "Titan Neo Analog Wristwatch",
            "Watches",
            "Lecture Hall A, Row 4",
            "2026-10-23",
            "Ananya Roy",
            "ananya.roy@campus.edu",
            "+91 98112 33445",
            "email",
            "Dark blue dial with brown leather strap. Dial has minor scratch near 2 o'clock.",
            "Mineral glass has slight scratch near the 2 o'clock marker.",
            "active",
            sample_images["watch"],
            "usr-student-01",
            0,
            "",
            0,
            "2026-10-23T11:20:00.000Z",
        ),
        (
            "item-106",
            "found",
            "Data Structures & Algorithms Hardcover Notes",
            "Books",
            "Central Library Reference Section",
            "2026-10-21",
            "Librarian Ramesh",
            "library.help@campus.edu",
            "+91 98111 00223",
            "email",
            "Spiral bound notebook with green cover containing handwritten Tree & Graph notes.",
            "Contains syllabus sheet and green binder clip.",
            "recovered",
            sample_images["notebook"],
            "usr-mod-01",
            0,
            "",
            0,
            "2026-10-21T16:00:00.000Z",
        ),
        (
            "item-107",
            "lost",
            "Milton Thermosteel Water Bottle 750ml",
            "Water Bottles",
            "Main Auditorium Entrance",
            "2026-10-27",
            "Karthik Raja",
            "karthik.mech@campus.edu",
            "+91 97890 12345",
            "email",
            "Silver matte finish stainless steel bottle with black screw cap and minor dent at bottom.",
            "Small dent on base ring and green initial 'K' sticker.",
            "active",
            sample_images["bottle"],
            "usr-student-01",
            0,
            "",
            0,
            "2026-10-27T15:00:00.000Z",
        ),
        (
            "item-108",
            "found",
            "OnePlus 11 5G Smartphone (Emerald Green)",
            "Mobile Phones",
            "Food Court Table #8",
            "2026-10-28",
            "Suresh Raina",
            "suresh.staff@campus.edu",
            "+91 98450 99887",
            "phone",
            "Emerald green back with frosted ring camera. Screen is intact and locked with PIN.",
            "Wallpaper is an anime space scene and phone has a spigen clear bumper case.",
            "active",
            sample_images["phone"],
            "usr-mod-01",
            0,
            "",
            0,
            "2026-10-28T09:15:00.000Z",
        ),
    ]

    cursor.executemany("""
    INSERT INTO items (
        id, type, name, category, location, date, contact_name, contact_email,
        contact_phone, contact_pref, description, identifying_marks, status,
        image, reported_by, flagged, flag_reason, hidden, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items_data)

    # Seed Sample Notifications
    notifs_data = [
        (
            "notif-101",
            "usr-student-01",
            "🎉 Welcome to FindIt Portal",
            "Your campus student account is active. You can report lost articles, register found items, and file verified ownership claims.",
            "info",
            1,
            "2026-10-24T10:30:00.000Z",
        ),
        (
            "notif-102",
            "usr-student-01",
            "📢 Report Filed Successfully",
            "Your report for 'Dell XPS 15 Laptop (Silver)' has been published to the campus directory.",
            "success",
            0,
            "2026-10-24T10:31:00.000Z",
        ),
        (
            "notif-103",
            "usr-admin-01",
            "🛡️ System Initialized",
            "Campus Lost & Found portal database synchronized with 8 seed records.",
            "info",
            1,
            "2026-10-24T08:00:00.000Z",
        ),
    ]

    cursor.executemany("""
    INSERT INTO notifications (id, user_id, title, message, type, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, notifs_data)

    # Seed Initial Audit Log
    cursor.execute("""
    INSERT INTO audit_logs (id, actor, action, target, details, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "log-101",
        "System Admin",
        "DATABASE_SEED",
        "All Tables",
        "Initialized campus Lost & Found database with demo accounts, items, and categories.",
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    reset_demo_db()
    print("Database initialized successfully at:", DB_PATH)
