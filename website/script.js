/**
 * FindIt – Smart Lost & Found Management Portal
 * Upgraded Full-Featured Controller with Role-Based Access Control (RBAC),
 * Claims Workflow, Image Uploads, Moderation, and LocalStorage Persistence.
 */

(function () {
    'use strict';

    // Storage Keys
    const STORAGE_KEY_ITEMS = 'findit_campus_items_v1';
    const STORAGE_KEY_USERS = 'findit_users_v1';
    const STORAGE_KEY_SESSION = 'findit_session_v1';
    const STORAGE_KEY_CLAIMS = 'findit_claims_v1';
    const STORAGE_KEY_CATEGORIES = 'findit_categories_v1';
    const STORAGE_KEY_LOGS = 'findit_audit_logs_v1';
    const STORAGE_KEY_NOTIFS = 'findit_notifications_v1';

    // Default Sample Categories
    const DEFAULT_CATEGORIES = [
        'ID Cards',
        'Mobile Phones',
        'Laptops',
        'Bags',
        'Books',
        'Keys',
        'Water Bottles',
        'Watches',
        'Accessories',
        'Other'
    ];

    // High quality SVG Data URLs for Demo Items (Genuine Visual Assets)
    const SAMPLE_IMAGES = {
        laptop: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%231e293b"/%3E%3Crect x="60" y="30" width="280" height="155" rx="8" fill="%230f172a" stroke="%2338bdf8" stroke-width="4"/%3E%3Crect x="75" y="45" width="250" height="125" rx="4" fill="%230284c7" fill-opacity="0.2"/%3E%3Cpath d="M185 95 L215 95 L200 125 Z" fill="%2338bdf8"/%3E%3Ctext x="200" y="150" fill="%23ffffff" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle"%3EDell XPS 15 (Silver)%3C/text%3E%3Cpath d="M40 190 L360 190 L380 205 L20 205 Z" fill="%2364748b"/%3E%3Crect x="170" y="192" width="60" height="6" rx="3" fill="%2394a3b8"/%3E%3C/svg%3E',
        calculator: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%230f172a"/%3E%3Crect x="130" y="20" width="140" height="200" rx="12" fill="%231e293b" stroke="%23f59e0b" stroke-width="3"/%3E%3Crect x="145" y="35" width="110" height="40" rx="4" fill="%2378350f" fill-opacity="0.3" stroke="%23d97706"/%3E%3Ctext x="200" y="60" fill="%23fef3c7" font-family="monospace" font-size="16" font-weight="bold" text-anchor="middle"%3Efx-991EX%3C/text%3E%3Ccircle cx="160" cy="100" r="10" fill="%23334155"/%3E%3Ccircle cx="200" cy="100" r="10" fill="%23334155"/%3E%3Ccircle cx="240" cy="100" r="10" fill="%23334155"/%3E%3Ccircle cx="160" cy="130" r="10" fill="%23334155"/%3E%3Ccircle cx="200" cy="130" r="10" fill="%23334155"/%3E%3Ccircle cx="240" cy="130" r="10" fill="%23334155"/%3E%3Ccircle cx="160" cy="160" r="10" fill="%23334155"/%3E%3Ccircle cx="200" cy="160" r="10" fill="%23334155"/%3E%3Ccircle cx="240" cy="160" r="10" fill="%23334155"/%3E%3Crect x="145" y="185" width="110" height="20" rx="6" fill="%23f59e0b"/%3E%3Ctext x="200" y="200" fill="%23000000" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle"%3ECASIO ClassWiz%3C/text%3E%3C/svg%3E',
        idcard: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%231e1e24"/%3E%3Crect x="80" y="30" width="240" height="170" rx="10" fill="%23ffffff" stroke="%233b82f6" stroke-width="4"/%3E%3Crect x="80" y="30" width="240" height="40" rx="10" fill="%231d4ed8"/%3E%3Ctext x="200" y="55" fill="%23ffffff" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle"%3ERATHINAM CAMPUS ID%3C/text%3E%3Crect x="100" y="85" width="55" height="70" rx="4" fill="%23cbd5e1" stroke="%2394a3b8"/%3E%3Ccircle cx="127" cy="110" r="16" fill="%2364748b"/%3E%3Cpath d="M107 148 C107 130, 147 130, 147 148 Z" fill="%2364748b"/%3E%3Ctext x="175" y="105" fill="%230f172a" font-family="sans-serif" font-size="14" font-weight="bold"%3ERahul Verma%3C/text%3E%3Ctext x="175" y="125" fill="%23475569" font-family="sans-serif" font-size="11"%3EDept: B.Tech CSE%3C/text%3E%3Ctext x="175" y="145" fill="%23475569" font-family="sans-serif" font-size="11"%3EID: 22BCS108%3C/text%3E%3Crect x="100" y="170" width="200" height="15" fill="%230f172a"/%3E%3C/svg%3E',
        wallet: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%231c1917"/%3E%3Crect x="90" y="45" width="220" height="145" rx="14" fill="%2378350f" stroke="%2392400e" stroke-width="4"/%3E%3Cpath d="M90 100 Q200 120 310 100" stroke="%23b45309" stroke-width="2" stroke-dasharray="6,4" fill="none"/%3E%3Crect x="250" y="90" width="60" height="40" rx="8" fill="%2392400e" stroke="%23f59e0b" stroke-width="2"/%3E%3Ccircle cx="265" cy="110" r="6" fill="%23f59e0b"/%3E%3Ctext x="170" y="150" fill="%23fef3c7" font-family="sans-serif" font-size="13" font-weight="bold"%3ELeather Wallet%3C/text%3E%3C/svg%3E',
        watch: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%230f172a"/%3E%3Crect x="175" y="10" width="50" height="220" rx="8" fill="%2378350f"/%3E%3Ccircle cx="200" cy="120" r="60" fill="%231e293b" stroke="%2338bdf8" stroke-width="5"/%3E%3Ccircle cx="200" cy="120" r="50" fill="%230f172a"/%3E%3Cline x1="200" y1="120" x2="200" y2="85" stroke="%23ffffff" stroke-width="3" stroke-linecap="round"/%3E%3Cline x1="200" y1="120" x2="225" y2="120" stroke="%2338bdf8" stroke-width="3" stroke-linecap="round"/%3E%3Ccircle cx="200" cy="120" r="4" fill="%2338bdf8"/%3E%3Ctext x="200" y="150" fill="%2394a3b8" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle"%3ETITAN NEO%3C/text%3E%3C/svg%3E',
        notebook: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%23064e3b"/%3E%3Crect x="110" y="30" width="180" height="180" rx="8" fill="%2310b981" stroke="%23059669" stroke-width="4"/%3E%3Crect x="95" y="35" width="20" height="170" rx="4" fill="%23cbd5e1" stroke="%2364748b" stroke-width="2"/%3E%3Cline x1="140" y1="65" x2="260" y2="65" stroke="%23064e3b" stroke-width="3" stroke-linecap="round"/%3E%3Cline x1="140" y1="85" x2="240" y2="85" stroke="%23064e3b" stroke-width="2" stroke-linecap="round"/%3E%3Ctext x="200" y="130" fill="%23ffffff" font-family="sans-serif" font-size="15" font-weight="bold" text-anchor="middle"%3EDSA LAB NOTES%3C/text%3E%3Ctext x="200" y="150" fill="%23d1fae5" font-family="sans-serif" font-size="11" text-anchor="middle"%3ETrees & Graphs (CSE)%3C/text%3E%3C/svg%3E',
        bottle: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%23042f2e"/%3E%3Crect x="160" y="20" width="80" height="200" rx="20" fill="%230f766e" stroke="%232dd4bf" stroke-width="3"/%3E%3Crect x="175" y="10" width="50" height="20" rx="6" fill="%23134e4a" stroke="%232dd4bf" stroke-width="2"/%3E%3Ctext x="200" y="125" fill="%23ccfbf1" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle"%3EMILTON 750ml%3C/text%3E%3Ctext x="200" y="145" fill="%2399f6e4" font-family="sans-serif" font-size="10" text-anchor="middle"%3EThermosteel Silver%3C/text%3E%3C/svg%3E',
        phone: 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"%3E%3Crect width="400" height="240" fill="%230f172a"/%3E%3Crect x="140" y="15" width="120" height="210" rx="20" fill="%231e293b" stroke="%236366f1" stroke-width="3"/%3E%3Crect x="148" y="25" width="104" height="190" rx="14" fill="%23312e81" fill-opacity="0.3"/%3E%3Ccircle cx="200" cy="35" r="4" fill="%2394a3b8"/%3E%3Ctext x="200" y="125" fill="%23e0e7ff" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle"%3EOnePlus 11 5G%3C/text%3E%3Ctext x="200" y="145" fill="%23a5b4fc" font-family="sans-serif" font-size="10" text-anchor="middle"%3EEmerald Green%3C/text%3E%3C/svg%3E'
    };

    // Realistic Campus Sample Items with Images
    const DEFAULT_SAMPLE_ITEMS = [
        {
            id: 'item-101',
            type: 'lost',
            name: 'Dell XPS 15 Laptop (Silver)',
            category: 'Laptops',
            location: 'Central Library 2nd Floor Reading Room',
            date: '2026-10-24',
            contactName: 'Dev Anand',
            contactEmail: 'student@campus.edu',
            contactPhone: '+91 98765 43210',
            contactPref: 'email',
            description: 'Silver aluminum body with a GitHub sticker on the back cover. Left in carrel table #14.',
            identifyingMarks: 'GitHub Octocat sticker and small scratch on left palm rest.',
            status: 'active',
            image: SAMPLE_IMAGES.laptop,
            reportedBy: 'usr-student-01',
            createdAt: '2026-10-24T10:30:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-102',
            type: 'found',
            name: 'Casio Scientific Calculator fx-991EX',
            category: 'Accessories',
            location: 'Computer Lab 3, Row B',
            date: '2026-10-25',
            contactName: 'Priya Sharma',
            contactEmail: 'priyasharma@campus.edu',
            contactPhone: '+91 99887 76655',
            contactPref: 'phone',
            description: 'ClassWiz edition with black protective slide cover. Left near terminal 24.',
            identifyingMarks: 'Student roll number ending in 891B written in silver marker inside cover.',
            status: 'active',
            image: SAMPLE_IMAGES.calculator,
            reportedBy: 'usr-student-02',
            createdAt: '2026-10-25T14:15:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-103',
            type: 'lost',
            name: 'Student ID Card - CSE Department',
            category: 'ID Cards',
            location: 'Campus Cafeteria Counter',
            date: '2026-10-22',
            contactName: 'Rahul Verma',
            contactEmail: 'rahul.cse@campus.edu',
            contactPhone: '+91 97766 55443',
            contactPref: 'email',
            description: 'Rathinam institution barcode ID with blue lanyard. Belongs to 3rd year CSE.',
            identifyingMarks: 'Barcode 22BCS108 with blue Rathinam branded neck strap.',
            status: 'recovered',
            image: SAMPLE_IMAGES.idcard,
            reportedBy: 'usr-student-03',
            createdAt: '2026-10-22T09:00:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-104',
            type: 'found',
            name: 'Brown Leather Wallet with Bus Pass',
            category: 'Bags',
            location: 'Sports Complex Bleachers',
            date: '2026-10-26',
            contactName: 'Coach Kumar',
            contactEmail: 'sports.dept@campus.edu',
            contactPhone: '+91 98451 22334',
            contactPref: 'phone',
            description: 'Contains campus transportation smart card, some change, and gym pass.',
            identifyingMarks: 'Rathinam bus pass route 14 inside card sleeve.',
            status: 'active',
            image: SAMPLE_IMAGES.wallet,
            reportedBy: 'usr-mod-01',
            createdAt: '2026-10-26T17:40:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-105',
            type: 'lost',
            name: 'Titan Neo Analog Wristwatch',
            category: 'Watches',
            location: 'Lecture Hall A, Row 4',
            date: '2026-10-23',
            contactName: 'Ananya Roy',
            contactEmail: 'ananya.roy@campus.edu',
            contactPhone: '+91 98112 33445',
            contactPref: 'email',
            description: 'Dark blue dial with brown leather strap. Dial has minor scratch near 2 o\'clock.',
            identifyingMarks: 'Mineral glass has slight scratch near the 2 o\'clock marker.',
            status: 'active',
            image: SAMPLE_IMAGES.watch,
            reportedBy: 'usr-student-04',
            createdAt: '2026-10-23T11:20:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-106',
            type: 'found',
            name: 'Data Structures & Algorithms Hardcover Notes',
            category: 'Books',
            location: 'Central Library Reference Section',
            date: '2026-10-21',
            contactName: 'Librarian Ramesh',
            contactEmail: 'library.help@campus.edu',
            contactPhone: '+91 98111 00223',
            contactPref: 'email',
            description: 'Spiral bound notebook with green cover containing handwritten Tree & Graph notes.',
            identifyingMarks: 'Contains syllabus sheet and green binder clip.',
            status: 'recovered',
            image: SAMPLE_IMAGES.notebook,
            reportedBy: 'usr-mod-01',
            createdAt: '2026-10-21T16:00:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-107',
            type: 'lost',
            name: 'Milton Thermosteel Water Bottle 750ml',
            category: 'Water Bottles',
            location: 'Main Auditorium Entrance',
            date: '2026-10-27',
            contactName: 'Karthik Raja',
            contactEmail: 'karthik.mech@campus.edu',
            contactPhone: '+91 97890 12345',
            contactPref: 'email',
            description: 'Silver matte finish stainless steel bottle with black screw cap and minor dent at bottom.',
            identifyingMarks: 'Small dent on base ring and green initial K sticker.',
            status: 'active',
            image: SAMPLE_IMAGES.bottle,
            reportedBy: 'usr-student-01',
            createdAt: '2026-10-27T15:00:00.000Z',
            flagged: false,
            hidden: false
        },
        {
            id: 'item-108',
            type: 'found',
            name: 'OnePlus 11 5G Smartphone (Emerald Green)',
            category: 'Mobile Phones',
            location: 'Food Court Table #8',
            date: '2026-10-28',
            contactName: 'Suresh Raina',
            contactEmail: 'suresh.staff@campus.edu',
            contactPhone: '+91 98450 99887',
            contactPref: 'phone',
            description: 'Emerald green back with frosted ring camera. Screen is intact and locked with PIN.',
            identifyingMarks: 'Wallpaper is an anime space scene and phone has a spigen clear bumper case.',
            status: 'active',
            image: SAMPLE_IMAGES.phone,
            reportedBy: 'usr-mod-01',
            createdAt: '2026-10-28T09:15:00.000Z',
            flagged: false,
            hidden: false
        }
    ];

    // Predefined Demo Accounts with Salted SHA-256 Hashes
    // Salt used for default accounts: "findit_salt_2026"
    // Passwords:
    // Student:   Student@123 -> 03cb6a151a73d4a06abf3b1c84973fe3f16eec2bd62afb7b02c89bcf80fd02e8
    // Moderator: Mod@123     -> 0c1b983bafbabb416b025856195a850ca6280f910fb19f2f650f130d859ef539
    // Admin:     Admin@123   -> 093eb1950eed3632d6d7b747d019e2224fd9eb5deac757b32e95368bcd67ff23
    const DEFAULT_USERS = [
        {
            id: 'usr-student-01',
            name: 'Dev Anand',
            email: 'student@campus.edu',
            salt: 'findit_salt_2026',
            passwordHash: '03cb6a151a73d4a06abf3b1c84973fe3f16eec2bd62afb7b02c89bcf80fd02e8',
            role: 'student',
            campusId: '22BCS108',
            department: 'Computer Science',
            phone: '+91 98765 43210',
            createdAt: '2026-09-01T08:00:00.000Z'
        },
        {
            id: 'usr-mod-01',
            name: 'Prof. Sarah Jenkins',
            email: 'moderator@campus.edu',
            salt: 'findit_salt_2026',
            passwordHash: '0c1b983bafbabb416b025856195a850ca6280f910fb19f2f650f130d859ef539',
            role: 'moderator',
            campusId: 'FAC-SAFE-04',
            department: 'Campus Safety & Discipline',
            phone: '+91 98451 22334',
            createdAt: '2026-08-15T09:30:00.000Z'
        },
        {
            id: 'usr-admin-01',
            name: 'Chief Administrator',
            email: 'admin@campus.edu',
            salt: 'findit_salt_2026',
            passwordHash: '093eb1950eed3632d6d7b747d019e2224fd9eb5deac757b32e95368bcd67ff23',
            role: 'admin',
            campusId: 'ADM-DIR-01',
            department: 'Campus Administration & Registry',
            phone: '+91 98111 00223',
            createdAt: '2026-08-01T10:00:00.000Z'
        }
    ];

    // State Variables
    let items = [];
    let users = [];
    let claims = [];
    let categories = [];
    let auditLogs = [];
    let notifications = [];
    let currentUser = null; // null = guest

    let pendingDeleteId = null;
    let selectedDetailsId = null;
    let currentLostImageData = null;
    let currentFoundImageData = null;

    /**
     * Standard Cryptographic Password Hashing (SHA-256 with Salt - Synchronous Pure JS)
     */
    function sha256Sync(ascii) {
        function rightRotate(value, amount) { return (value >>> amount) | (value << (32 - amount)); }
        const mathPow = Math.pow;
        const maxWord = mathPow(2, 32);
        let lengthProperty = 'length';
        let i, j;
        let result = '';
        const words = [];
        const asciiBitLength = ascii[lengthProperty] * 8;
        let hash = [];
        const k = [];
        let primeCounter = 0;
        const isComposite = {};
        for (let candidate = 2; primeCounter < 64; candidate++) {
            if (!isComposite[candidate]) {
                for (i = 0; i < 313; i += candidate) isComposite[i] = candidate;
                hash[primeCounter] = (mathPow(candidate, .5) * maxWord) | 0;
                k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
            }
        }
        ascii += '\x80';
        while (ascii[lengthProperty] % 64 - 56) ascii += '\x00';
        for (i = 0; i < ascii[lengthProperty]; i++) {
            j = ascii.charCodeAt(i);
            words[i >> 2] |= j << ((3 - i) % 4) * 8;
        }
        words[words[lengthProperty]] = ((asciiBitLength / maxWord) | 0);
        words[words[lengthProperty]] = (asciiBitLength);

        for (j = 0; j < words[lengthProperty];) {
            const w = words.slice(j, j += 16);
            const oldHash = hash;
            hash = hash.slice(0, 8);
            for (i = 0; i < 64; i++) {
                const w15 = w[i - 15], w2 = w[i - 2];
                const a = hash[0], e = hash[4];
                const temp1 = hash[7]
                    + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25))
                    + ((e & hash[5]) ^ ((~e) & hash[6]))
                    + k[i]
                    + (w[i] = (i < 16) ? w[i] : (
                        w[i - 16]
                        + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3))
                        + w[i - 7]
                        + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
                    ) | 0);
                const temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22))
                    + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
                hash = [(temp1 + temp2) | 0].concat(hash);
                hash[4] = (hash[4] + temp1) | 0;
            }
            for (i = 0; i < 8; i++) hash[i] = (hash[i] + oldHash[i]) | 0;
        }
        for (i = 0; i < 8; i++) {
            for (j = 3; j >= 0; j--) {
                const b = (hash[i] >> (8 * j)) & 255;
                result += ((b < 16) ? '0' : '') + b.toString(16);
            }
        }
        return result;
    }

    /**
     * Storage & Data Initialization
     */
    function initData() {
        // 1. Items
        try {
            const raw = localStorage.getItem(STORAGE_KEY_ITEMS);
            if (raw) {
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    items = parsed;
                } else {
                    items = JSON.parse(JSON.stringify(DEFAULT_SAMPLE_ITEMS));
                    saveItems();
                }
            } else {
                items = JSON.parse(JSON.stringify(DEFAULT_SAMPLE_ITEMS));
                saveItems();
            }
        } catch (e) {
            items = JSON.parse(JSON.stringify(DEFAULT_SAMPLE_ITEMS));
        }

        // 2. Users (Ensure default demo credentials match current salted hashes)
        try {
            const rawUsers = localStorage.getItem(STORAGE_KEY_USERS);
            if (rawUsers) {
                users = JSON.parse(rawUsers);
                DEFAULT_USERS.forEach(defU => {
                    const exIdx = users.findIndex(u => u.id === defU.id || u.email.toLowerCase() === defU.email.toLowerCase());
                    if (exIdx !== -1) {
                        users[exIdx].passwordHash = defU.passwordHash;
                        users[exIdx].salt = defU.salt;
                    } else {
                        users.push(defU);
                    }
                });
                saveUsers();
            } else {
                users = JSON.parse(JSON.stringify(DEFAULT_USERS));
                saveUsers();
            }
        } catch (e) {
            users = JSON.parse(JSON.stringify(DEFAULT_USERS));
        }

        // 3. Categories
        try {
            const rawCats = localStorage.getItem(STORAGE_KEY_CATEGORIES);
            if (rawCats) {
                categories = JSON.parse(rawCats);
            } else {
                categories = [...DEFAULT_CATEGORIES];
                saveCategories();
            }
        } catch (e) {
            categories = [...DEFAULT_CATEGORIES];
        }

        // 4. Claims
        try {
            const rawClaims = localStorage.getItem(STORAGE_KEY_CLAIMS);
            if (rawClaims) {
                claims = JSON.parse(rawClaims);
            } else {
                claims = [];
                saveClaims();
            }
        } catch (e) {
            claims = [];
        }

        // 5. Audit Logs
        try {
            const rawLogs = localStorage.getItem(STORAGE_KEY_LOGS);
            if (rawLogs) {
                auditLogs = JSON.parse(rawLogs);
            } else {
                auditLogs = [
                    {
                        timestamp: new Date().toLocaleTimeString(),
                        actor: 'System Initialization',
                        action: 'PORTAL_BOOT',
                        target: 'FindIt v2.0',
                        details: 'System initialized with role-based security & persistence.'
                    }
                ];
                saveLogs();
            }
        } catch (e) {
            auditLogs = [];
        }

        // 6. Notifications
        try {
            const rawNotifs = localStorage.getItem(STORAGE_KEY_NOTIFS);
            if (rawNotifs) {
                notifications = JSON.parse(rawNotifs);
            } else {
                notifications = [
                    {
                        id: 'notif-1',
                        userId: 'usr-student-01',
                        title: 'Welcome to FindIt',
                        text: 'Role-based access activated. You are registered as Student.',
                        time: 'Just now',
                        read: false
                    }
                ];
                saveNotifs();
            }
        } catch (e) {
            notifications = [];
        }

        // 7. Active Session
        try {
            const rawSession = localStorage.getItem(STORAGE_KEY_SESSION);
            if (rawSession) {
                const sessionUser = JSON.parse(rawSession);
                const matched = users.find(u => u.id === sessionUser.id);
                if (matched) {
                    currentUser = matched;
                }
            }
        } catch (e) {
            currentUser = null;
        }
    }

    function saveItems() {
        try {
            localStorage.setItem(STORAGE_KEY_ITEMS, JSON.stringify(items));
        } catch (e) {
            console.error('Failed saving items', e);
        }
    }

    function saveUsers() {
        try {
            localStorage.setItem(STORAGE_KEY_USERS, JSON.stringify(users));
        } catch (e) {
            console.error('Failed saving users', e);
        }
    }

    function saveClaims() {
        try {
            localStorage.setItem(STORAGE_KEY_CLAIMS, JSON.stringify(claims));
        } catch (e) {
            console.error('Failed saving claims', e);
        }
    }

    function saveCategories() {
        try {
            localStorage.setItem(STORAGE_KEY_CATEGORIES, JSON.stringify(categories));
        } catch (e) {
            console.error('Failed saving categories', e);
        }
    }

    function saveLogs() {
        try {
            localStorage.setItem(STORAGE_KEY_LOGS, JSON.stringify(auditLogs));
        } catch (e) {
            console.error('Failed saving logs', e);
        }
    }

    function saveNotifs() {
        try {
            localStorage.setItem(STORAGE_KEY_NOTIFS, JSON.stringify(notifications));
        } catch (e) {
            console.error('Failed saving notifications', e);
        }
    }

    function logAudit(action, target, details) {
        const actorName = currentUser ? `${currentUser.name} (${currentUser.role})` : 'Anonymous Guest';
        auditLogs.unshift({
            timestamp: new Date().toLocaleTimeString(),
            actor: actorName,
            action: action,
            target: target,
            details: details
        });
        if (auditLogs.length > 50) auditLogs.pop();
        saveLogs();
        renderAuditLogs();
    }

    function addNotification(userId, title, text) {
        notifications.unshift({
            id: 'notif-' + Date.now(),
            userId: userId,
            title: title,
            text: text,
            time: 'Just now',
            read: false
        });
        saveNotifs();
        renderNotifications();
    }

    /**
     * Alert Notification Helpers
     */
    let alertTimeout = null;

    function showSuccess(msg) {
        const successAlert = document.getElementById('success-message');
        const successText = document.getElementById('success-message-text');
        const errorAlert = document.getElementById('error-message');
        if (!successAlert || !successText) return;

        successText.textContent = msg;
        successAlert.classList.remove('d-none');
        if (errorAlert) errorAlert.classList.add('d-none');

        clearTimeout(alertTimeout);
        alertTimeout = setTimeout(() => {
            successAlert.classList.add('d-none');
        }, 6000);
    }

    function showError(msg) {
        const errorAlert = document.getElementById('error-message');
        const errorText = document.getElementById('error-message-text');
        const successAlert = document.getElementById('success-message');
        if (!errorAlert || !errorText) return;

        errorText.textContent = msg;
        errorAlert.classList.remove('d-none');
        if (successAlert) successAlert.classList.add('d-none');

        clearTimeout(alertTimeout);
        alertTimeout = setTimeout(() => {
            errorAlert.classList.add('d-none');
        }, 8000);
    }

    function hideAlerts() {
        const s = document.getElementById('success-message');
        const e = document.getElementById('error-message');
        if (s) s.classList.add('d-none');
        if (e) e.classList.add('d-none');
    }

    /**
     * Update Dashboard Statistics
     */
    function updateStatistics() {
        // Visible active/recovered items
        const visibleItems = items.filter(i => !i.hidden);
        const totalLost = visibleItems.filter(i => i.type === 'lost').length;
        const totalFound = visibleItems.filter(i => i.type === 'found').length;
        const totalRecovered = visibleItems.filter(i => i.status === 'recovered').length;
        const totalActive = visibleItems.filter(i => i.status === 'active').length;
        const pendingClaimsCount = claims.filter(c => c.status === 'pending').length;

        const elLost = document.getElementById('stats-total-lost');
        const elFound = document.getElementById('stats-total-found');
        const elRecovered = document.getElementById('stats-total-recovered');
        const elActive = document.getElementById('stats-total-active');
        const elClaims = document.getElementById('stats-total-claims');

        if (elLost) elLost.textContent = totalLost;
        if (elFound) elFound.textContent = totalFound;
        if (elRecovered) elRecovered.textContent = totalRecovered;
        if (elActive) elActive.textContent = totalActive;
        if (elClaims) elClaims.textContent = pendingClaimsCount;

        // Dynamic Category Distribution Breakdown
        const catBarsEl = document.getElementById('dashboard-category-bars');
        if (catBarsEl) {
            const counts = {};
            DEFAULT_CATEGORIES.forEach(c => counts[c] = 0);
            visibleItems.forEach(i => {
                if (counts[i.category] !== undefined) counts[i.category]++;
                else counts[i.category] = (counts[i.category] || 0) + 1;
            });
            const topCats = Object.entries(counts).filter(([_, cnt]) => cnt > 0).sort((a, b) => b[1] - a[1]);
            if (topCats.length === 0) {
                catBarsEl.innerHTML = '<span style="font-size:0.82rem; color:var(--slate-500);">No category distribution available yet.</span>';
            } else {
                const maxCount = Math.max(...topCats.map(c => c[1]), 1);
                catBarsEl.innerHTML = topCats.slice(0, 5).map(([cat, cnt]) => `
                    <div class="distribution-item">
                        <div class="dist-meta">
                            <span>${cat}</span>
                            <span>${cnt} item${cnt > 1 ? 's' : ''}</span>
                        </div>
                        <div class="dist-bar-track">
                            <div class="dist-bar-fill" style="width: ${(cnt / maxCount) * 100}%"></div>
                        </div>
                    </div>
                `).join('');
            }
        }

        // Dynamic Status Distribution Breakdown
        const statusBarsEl = document.getElementById('dashboard-status-bars');
        if (statusBarsEl) {
            const total = visibleItems.length || 1;
            const statusCounts = [
                { label: 'Active Unresolved Cases', count: totalActive, pct: Math.round((totalActive / total) * 100) },
                { label: 'Pending Ownership Claims', count: pendingClaimsCount, pct: Math.round((pendingClaimsCount / total) * 100) },
                { label: 'Recovered & Reunited', count: totalRecovered, pct: Math.round((totalRecovered / total) * 100) }
            ];
            statusBarsEl.innerHTML = statusCounts.map(s => `
                <div class="distribution-item">
                    <div class="dist-meta">
                        <span>${s.label}</span>
                        <span>${s.count} (${s.pct}%)</span>
                    </div>
                    <div class="dist-bar-track">
                        <div class="dist-bar-fill" style="width: ${s.pct}%"></div>
                    </div>
                </div>
            `).join('');
        }

        // Admin Overview Metrics
        const mUsers = document.getElementById('admin-metric-users');
        const mReports = document.getElementById('admin-metric-reports');
        const mClaims = document.getElementById('admin-metric-claims');
        const mResolved = document.getElementById('admin-metric-resolved');

        if (mUsers) mUsers.textContent = users.length;
        if (mReports) mReports.textContent = items.length;
        if (mClaims) mClaims.textContent = pendingClaimsCount;
        if (mResolved) mResolved.textContent = totalRecovered;

        const badgeAdminClaims = document.getElementById('admin-pending-claims-count');
        const badgeAdminUsers = document.getElementById('admin-users-count');
        if (badgeAdminClaims) badgeAdminClaims.textContent = pendingClaimsCount;
        if (badgeAdminUsers) badgeAdminUsers.textContent = users.length;

        // Moderator Counts
        const modFlaggedCount = document.getElementById('mod-flagged-count');
        const modHiddenCount = document.getElementById('mod-hidden-count');
        if (modFlaggedCount) modFlaggedCount.textContent = items.filter(i => i.flagged).length;
        if (modHiddenCount) modHiddenCount.textContent = items.filter(i => i.hidden).length;
    }

    /**
     * Authentication & Role Control (Feature 1)
     */
    function updateAuthUI() {
        const navLoginBtn = document.getElementById('nav-login-btn');
        const navUserMenu = document.getElementById('nav-user-menu');
        const navMyActivityLink = document.getElementById('nav-my-activity-link');
        const navModLink = document.getElementById('nav-moderator-link');
        const navAdminLink = document.getElementById('nav-admin-link');
        const modSection = document.getElementById('moderator-section');
        const adminSection = document.getElementById('admin-section');
        const myActivitySection = document.getElementById('my-activity-section');
        const roleStatusText = document.getElementById('role-status-text');
        const authStatusDot = document.getElementById('auth-status-dot');

        const dropdownModBtn = document.getElementById('dropdown-mod-btn');
        const dropdownAdminBtn = document.getElementById('dropdown-admin-btn');

        if (currentUser) {
            // Logged in
            if (navLoginBtn) navLoginBtn.classList.add('d-none');
            if (navUserMenu) navUserMenu.classList.remove('d-none');
            if (navMyActivityLink) navMyActivityLink.classList.remove('d-none');

            // Set user initials & name
            const initials = currentUser.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            const avatarEl = document.getElementById('nav-user-avatar');
            const nameEl = document.getElementById('nav-user-name');
            const roleEl = document.getElementById('nav-user-role');
            const ddName = document.getElementById('dropdown-user-fullname');
            const ddEmail = document.getElementById('dropdown-user-email');

            if (avatarEl) avatarEl.textContent = initials;
            if (nameEl) nameEl.textContent = currentUser.name;
            if (ddName) ddName.textContent = currentUser.name;
            if (ddEmail) ddEmail.textContent = currentUser.email;

            if (roleEl) {
                roleEl.textContent = currentUser.role.toUpperCase();
                roleEl.className = `role-pill-badge role-badge-${currentUser.role}`;
            }

            // Dashboard personalized greeting banner (Feature 6)
            const greetingBanner = document.getElementById('dashboard-user-greeting');
            const greetingAvatar = document.getElementById('greeting-avatar');
            const greetingTitle = document.getElementById('greeting-title');
            const greetingSubtitle = document.getElementById('greeting-subtitle');
            if (greetingBanner) {
                greetingBanner.classList.remove('d-none');
                if (greetingAvatar) greetingAvatar.textContent = initials;
                if (greetingTitle) greetingTitle.textContent = `Welcome back, ${currentUser.name}!`;
                if (greetingSubtitle) {
                    greetingSubtitle.textContent = `${currentUser.role.toUpperCase()} • ${currentUser.department || 'Campus Community'} — Track your lost and found campus reports or submit a recovery claim.`;
                }
            }

            // Role Status Strip
            if (roleStatusText) {
                roleStatusText.innerHTML = `Active Session: <strong>${escapeHtml(currentUser.name)}</strong> (${currentUser.role.toUpperCase()} • ${escapeHtml(currentUser.department)})`;
            }
            if (authStatusDot) {
                authStatusDot.className = `status-indicator-dot active-${currentUser.role}`;
            }

            // Moderator Panel Access
            if (currentUser.role === 'moderator' || currentUser.role === 'admin') {
                if (navModLink) navModLink.classList.remove('d-none');
                if (dropdownModBtn) dropdownModBtn.classList.remove('d-none');
            } else {
                if (navModLink) navModLink.classList.add('d-none');
                if (dropdownModBtn) dropdownModBtn.classList.add('d-none');
                if (modSection) modSection.classList.add('d-none');
            }

            // Admin Panel Access
            if (currentUser.role === 'admin') {
                if (navAdminLink) navAdminLink.classList.remove('d-none');
                if (dropdownAdminBtn) dropdownAdminBtn.classList.remove('d-none');
            } else {
                if (navAdminLink) navAdminLink.classList.add('d-none');
                if (dropdownAdminBtn) dropdownAdminBtn.classList.add('d-none');
                if (adminSection) adminSection.classList.add('d-none');
            }
        } else {
            // Guest mode
            if (navLoginBtn) navLoginBtn.classList.remove('d-none');
            if (navUserMenu) navUserMenu.classList.add('d-none');
            if (navMyActivityLink) navMyActivityLink.classList.add('d-none');
            if (navModLink) navModLink.classList.add('d-none');
            if (navAdminLink) navAdminLink.classList.add('d-none');
            if (modSection) modSection.classList.add('d-none');
            if (adminSection) adminSection.classList.add('d-none');
            if (myActivitySection) myActivitySection.classList.add('d-none');

            const greetingBanner = document.getElementById('dashboard-user-greeting');
            if (greetingBanner) greetingBanner.classList.add('d-none');

            if (roleStatusText) {
                roleStatusText.innerHTML = `Operating as: <strong>Guest</strong> (Public Mode • Click demo shortcuts to test roles)`;
            }
            if (authStatusDot) {
                authStatusDot.className = 'status-indicator-dot';
            }
        }

        renderNotifications();
    }

    function loginUser(email, rawPassword) {
        const user = users.find(u => u.email.toLowerCase() === email.trim().toLowerCase());
        if (!user) {
            showError('Account not found with this campus email. Please register.');
            return false;
        }

        const computedHash = sha256Sync(rawPassword + user.salt);
        if (computedHash !== user.passwordHash) {
            showError('Invalid password. Please verify credentials.');
            return false;
        }

        currentUser = user;
        localStorage.setItem(STORAGE_KEY_SESSION, JSON.stringify(currentUser));
        updateAuthUI();
        logAudit('USER_LOGIN', user.email, `Logged in successfully as ${user.role}.`);
        showSuccess(`Welcome back, ${user.name}! Authenticated as ${user.role.toUpperCase()}.`);
        renderCatalog();
        return true;
    }

    function logoutUser() {
        if (currentUser) {
            logAudit('USER_LOGOUT', currentUser.email, 'Logged out of portal.');
        }
        currentUser = null;
        localStorage.removeItem(STORAGE_KEY_SESSION);
        updateAuthUI();
        showSuccess('You have been signed out successfully.');
        renderCatalog();
    }

    function registerUser(name, email, campusId, department, role, password) {
        if (users.some(u => u.email.toLowerCase() === email.trim().toLowerCase())) {
            showError('An account already exists with this campus email.');
            return false;
        }

        const salt = 'salt_' + Date.now();
        const passwordHash = sha256Sync(password + salt);

        const newUser = {
            id: 'usr-' + Date.now(),
            name: name.trim(),
            email: email.trim().toLowerCase(),
            salt: salt,
            passwordHash: passwordHash,
            role: role || 'student',
            campusId: campusId.trim(),
            department: department,
            phone: '',
            createdAt: new Date().toISOString()
        };

        users.push(newUser);
        saveUsers();
        currentUser = newUser;
        localStorage.setItem(STORAGE_KEY_SESSION, JSON.stringify(currentUser));
        updateAuthUI();
        logAudit('USER_REGISTER', newUser.email, `Created new account with role ${newUser.role}.`);
        showSuccess(`Account registered successfully! Welcome, ${newUser.name}.`);
        renderCatalog();
        return true;
    }

    /**
     * Notifications Manager
     */
    function renderNotifications() {
        const notifBadge = document.getElementById('notif-badge');
        const notifList = document.getElementById('notif-list');
        if (!notifList || !notifBadge) return;

        const userNotifs = currentUser
            ? notifications.filter(n => n.userId === currentUser.id || n.userId === 'all')
            : [];

        const unreadCount = userNotifs.filter(n => !n.read).length;
        if (unreadCount > 0) {
            notifBadge.textContent = unreadCount;
            notifBadge.classList.remove('d-none');
        } else {
            notifBadge.classList.add('d-none');
        }

        if (userNotifs.length === 0) {
            notifList.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--slate-400); font-size: 0.82rem;">No campus notifications</div>';
            return;
        }

        notifList.innerHTML = userNotifs.map(n => `
            <div class="notif-item ${n.read ? '' : 'unread'}">
                <div class="notif-item-title">${escapeHtml(n.title)}</div>
                <div style="color: var(--slate-600); margin-bottom: 0.2rem;">${escapeHtml(n.text)}</div>
                <div class="notif-item-time">${escapeHtml(n.time)}</div>
            </div>
        `).join('');
    }

    /**
     * Categories Management (Admin Feature 1)
     */
    function renderCategorySelects() {
        const lostCat = document.getElementById('item-category');
        const foundCat = document.getElementById('found-item-category');
        const filterCat = document.getElementById('category-filter');

        const optionsHtml = '<option value="">Select Category</option>' +
            categories.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');

        if (lostCat) {
            const currentVal = lostCat.value;
            lostCat.innerHTML = optionsHtml;
            lostCat.value = currentVal;
        }

        if (foundCat) {
            const currentVal = foundCat.value;
            foundCat.innerHTML = optionsHtml;
            foundCat.value = currentVal;
        }

        if (filterCat) {
            const currentVal = filterCat.value;
            filterCat.innerHTML = '<option value="all">All Categories</option>' +
                categories.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
            filterCat.value = currentVal || 'all';
        }

        // Render Admin Category List
        const adminCatList = document.getElementById('admin-category-list');
        const catCountEl = document.getElementById('cat-count');
        if (catCountEl) catCountEl.textContent = categories.length;

        if (adminCatList) {
            adminCatList.innerHTML = categories.map(cat => `
                <li class="category-pill-item">
                    <span>${escapeHtml(cat)}</span>
                    <button type="button" class="btn-remove-cat" data-category="${escapeHtml(cat)}" title="Remove category">&times;</button>
                </li>
            `).join('');
        }
    }

    function addCategory(newCat) {
        if (!currentUser || currentUser.role !== 'admin') {
            showError('Access Denied: Only administrators can manage categories.');
            return;
        }
        const trimmed = newCat.trim();
        if (!trimmed) return;
        if (categories.includes(trimmed)) {
            showError('Category already exists.');
            return;
        }
        categories.push(trimmed);
        saveCategories();
        renderCategorySelects();
        logAudit('CATEGORY_ADD', trimmed, 'Added new category to catalog taxonomy.');
        showSuccess(`Category "${trimmed}" added successfully.`);
    }

    function removeCategory(catToRemove) {
        if (!currentUser || currentUser.role !== 'admin') {
            showError('Access Denied: Only administrators can delete categories.');
            return;
        }
        if (categories.length <= 1) {
            showError('At least one category must remain.');
            return;
        }
        categories = categories.filter(c => c !== catToRemove);
        saveCategories();
        renderCategorySelects();
        logAudit('CATEGORY_REMOVE', catToRemove, 'Deleted category.');
        showSuccess(`Category "${catToRemove}" removed.`);
    }

    /**
     * Image Upload Handlers (Feature 2)
     */
    function setupImageUploads() {
        const lostFileInput = document.getElementById('item-image-file');
        const lostPreviewBox = document.getElementById('lost-image-preview-box');
        const lostPreviewImg = document.getElementById('lost-preview-img');
        const lostPreviewName = document.getElementById('lost-preview-name');
        const lostPrompt = document.getElementById('lost-upload-prompt');
        const lostRemoveBtn = document.getElementById('lost-remove-photo-btn');

        if (lostFileInput) {
            lostFileInput.addEventListener('change', function (e) {
                const file = e.target.files[0];
                if (!file) return;

                if (!['image/jpeg', 'image/jpg', 'image/png', 'image/webp'].includes(file.type)) {
                    showError('Please upload a valid image file (JPG, PNG, or WEBP).');
                    lostFileInput.value = '';
                    return;
                }

                if (file.size > 5 * 1024 * 1024) {
                    showError('Image size exceeds 5MB limit. Please choose a smaller file.');
                    lostFileInput.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (evt) {
                    currentLostImageData = evt.target.result;
                    if (lostPreviewImg) lostPreviewImg.src = currentLostImageData;
                    if (lostPreviewName) lostPreviewName.textContent = file.name;
                    if (lostPreviewBox) lostPreviewBox.classList.remove('d-none');
                    if (lostPrompt) lostPrompt.classList.add('d-none');
                };
                reader.readAsDataURL(file);
            });
        }

        if (lostRemoveBtn) {
            lostRemoveBtn.addEventListener('click', function () {
                currentLostImageData = null;
                if (lostFileInput) lostFileInput.value = '';
                if (lostPreviewBox) lostPreviewBox.classList.add('d-none');
                if (lostPrompt) lostPrompt.classList.remove('d-none');
            });
        }

        // Found Image Upload
        const foundFileInput = document.getElementById('found-image-file');
        const foundPreviewBox = document.getElementById('found-image-preview-box');
        const foundPreviewImg = document.getElementById('found-preview-img');
        const foundPreviewName = document.getElementById('found-preview-name');
        const foundPrompt = document.getElementById('found-upload-prompt');
        const foundRemoveBtn = document.getElementById('found-remove-photo-btn');

        if (foundFileInput) {
            foundFileInput.addEventListener('change', function (e) {
                const file = e.target.files[0];
                if (!file) return;

                if (!['image/jpeg', 'image/jpg', 'image/png', 'image/webp'].includes(file.type)) {
                    showError('Please upload a valid image file (JPG, PNG, or WEBP).');
                    foundFileInput.value = '';
                    return;
                }

                if (file.size > 5 * 1024 * 1024) {
                    showError('Image size exceeds 5MB limit. Please choose a smaller file.');
                    foundFileInput.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (evt) {
                    currentFoundImageData = evt.target.result;
                    if (foundPreviewImg) foundPreviewImg.src = currentFoundImageData;
                    if (foundPreviewName) foundPreviewName.textContent = file.name;
                    if (foundPreviewBox) foundPreviewBox.classList.remove('d-none');
                    if (foundPrompt) foundPrompt.classList.add('d-none');
                };
                reader.readAsDataURL(file);
            });
        }

        if (foundRemoveBtn) {
            foundRemoveBtn.addEventListener('click', function () {
                currentFoundImageData = null;
                if (foundFileInput) foundFileInput.value = '';
                if (foundPreviewBox) foundPreviewBox.classList.add('d-none');
                if (foundPrompt) foundPrompt.classList.remove('d-none');
            });
        }
    }

    /**
     * Tab Switcher (Lost / Found)
     */
    function setupTabs() {
        const tabLost = document.getElementById('tab-btn-lost');
        const tabFound = document.getElementById('tab-btn-found');
        const panelLost = document.getElementById('lost-tab-panel');
        const panelFound = document.getElementById('found-tab-panel');

        if (!tabLost || !tabFound) return;

        tabLost.addEventListener('click', () => {
            tabLost.classList.add('active');
            tabLost.setAttribute('aria-selected', 'true');
            tabFound.classList.remove('active');
            tabFound.setAttribute('aria-selected', 'false');

            if (panelLost) panelLost.classList.remove('d-none');
            if (panelFound) panelFound.classList.add('d-none');
        });

        tabFound.addEventListener('click', () => {
            tabFound.classList.add('active');
            tabFound.setAttribute('aria-selected', 'true');
            tabLost.classList.remove('active');
            tabLost.setAttribute('aria-selected', 'false');

            if (panelFound) panelFound.classList.remove('d-none');
            if (panelLost) panelLost.classList.add('d-none');
        });
    }

    /**
     * Form Validation Helpers
     */
    function isValidEmail(email) {
        if (!email || typeof email !== 'string') return false;
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(email.trim());
    }

    function isValidDate(dateStr) {
        if (!dateStr) return false;
        const enteredDate = new Date(dateStr);
        if (isNaN(enteredDate.getTime())) return false;

        const today = new Date();
        today.setHours(23, 59, 59, 999);
        return enteredDate <= today;
    }

    /**
     * Lost Item Form Handler
     */
    function setupLostForm() {
        const lostForm = document.getElementById('lost-item-form');
        const lostName = document.getElementById('item-name');
        const lostCategory = document.getElementById('item-category');
        const lostLocation = document.getElementById('item-location');
        const lostDate = document.getElementById('item-date');
        const lostContactName = document.getElementById('contact-name');
        const lostContactEmail = document.getElementById('contact-email');
        const lostDesc = document.getElementById('item-description');

        const nameError = document.getElementById('name-error');
        const categoryError = document.getElementById('category-error');
        const locationError = document.getElementById('location-error');
        const dateError = document.getElementById('date-error');
        const contactNameError = document.getElementById('contact-name-error');
        const emailError = document.getElementById('email-error');
        const descError = document.getElementById('desc-error');

        if (!lostForm) return;

        const todayStr = new Date().toISOString().split('T')[0];
        if (lostDate) lostDate.setAttribute('max', todayStr);

        lostForm.addEventListener('submit', function (e) {
            e.preventDefault();
            hideAlerts();

            let hasError = false;

            const inputs = [lostName, lostCategory, lostLocation, lostDate, lostContactName, lostContactEmail, lostDesc];
            const errors = [nameError, categoryError, locationError, dateError, contactNameError, emailError, descError];

            inputs.forEach(input => input && input.classList.remove('is-invalid'));
            errors.forEach(err => err && err.classList.remove('visible'));

            // 1. Name
            const nameVal = lostName.value.trim();
            if (!nameVal) {
                lostName.classList.add('is-invalid');
                nameError.classList.add('visible');
                hasError = true;
            }

            // 2. Category
            const categoryVal = lostCategory.value;
            if (!categoryVal) {
                lostCategory.classList.add('is-invalid');
                categoryError.classList.add('visible');
                hasError = true;
            }

            // 3. Location
            const locationVal = lostLocation.value.trim();
            if (!locationVal) {
                lostLocation.classList.add('is-invalid');
                locationError.classList.add('visible');
                hasError = true;
            }

            // 4. Date
            const dateVal = lostDate.value;
            if (!isValidDate(dateVal)) {
                lostDate.classList.add('is-invalid');
                dateError.classList.add('visible');
                hasError = true;
            }

            // 5. Contact Name
            const contactNameVal = lostContactName.value.trim();
            if (!contactNameVal) {
                lostContactName.classList.add('is-invalid');
                contactNameError.classList.add('visible');
                hasError = true;
            }

            // 6. Contact Email
            const emailVal = lostContactEmail.value.trim();
            if (!isValidEmail(emailVal)) {
                lostContactEmail.classList.add('is-invalid');
                emailError.classList.add('visible');
                hasError = true;
            }

            // 7. Description
            const descVal = lostDesc.value.trim();
            if (!descVal) {
                lostDesc.classList.add('is-invalid');
                descError.classList.add('visible');
                hasError = true;
            }

            if (hasError) {
                showError('Please correct the highlighted errors. All required fields and a valid email format are mandatory.');
                return;
            }

            // Create New Lost Item
            const phoneVal = (document.getElementById('item-contact-phone')?.value || '').trim();
            const prefVal = document.getElementById('item-contact-pref')?.value || 'email';
            const idMarksVal = (document.getElementById('item-identifying-marks')?.value || '').trim();

            const newItem = {
                id: 'item-' + Date.now(),
                type: 'lost',
                name: nameVal,
                category: categoryVal,
                location: locationVal,
                date: dateVal,
                contactName: contactNameVal,
                contactEmail: emailVal,
                contactPhone: phoneVal,
                contactPref: prefVal,
                description: descVal,
                identifyingMarks: idMarksVal,
                status: 'active',
                image: currentLostImageData || null,
                reportedBy: currentUser ? currentUser.id : 'guest',
                createdAt: new Date().toISOString(),
                flagged: false,
                hidden: false
            };

            items.unshift(newItem);
            saveItems();
            updateStatistics();
            renderCatalog();
            renderMyActivity();
            logAudit('REPORT_LOST', newItem.name, `New lost item filed by ${contactNameVal}.`);

            lostForm.reset();
            currentLostImageData = null;
            const lostPreviewBox = document.getElementById('lost-image-preview-box');
            const lostPrompt = document.getElementById('lost-upload-prompt');
            if (lostPreviewBox) lostPreviewBox.classList.add('d-none');
            if (lostPrompt) lostPrompt.classList.remove('d-none');

            showSuccess(`Lost item "${nameVal}" has been reported successfully!`);

            const catalogEl = document.getElementById('catalog-section');
            if (catalogEl) catalogEl.scrollIntoView({ behavior: 'smooth' });
        });
    }

    /**
     * Found Item Form Handler
     */
    function setupFoundForm() {
        const foundForm = document.getElementById('found-item-form');
        const foundName = document.getElementById('found-item-name');
        const foundCategory = document.getElementById('found-item-category');
        const foundLocation = document.getElementById('found-item-location');
        const foundDate = document.getElementById('found-item-date');
        const foundContactName = document.getElementById('found-contact-name');
        const foundContactEmail = document.getElementById('found-contact-email');
        const foundDesc = document.getElementById('found-item-description');

        const foundNameError = document.getElementById('found-name-error');
        const foundCategoryError = document.getElementById('found-category-error');
        const foundLocationError = document.getElementById('found-location-error');
        const foundDateError = document.getElementById('found-date-error');
        const foundContactNameError = document.getElementById('found-contact-name-error');
        const foundEmailError = document.getElementById('found-email-error');
        const foundDescError = document.getElementById('found-desc-error');

        if (!foundForm) return;

        const todayStr = new Date().toISOString().split('T')[0];
        if (foundDate) foundDate.setAttribute('max', todayStr);

        foundForm.addEventListener('submit', function (e) {
            e.preventDefault();
            hideAlerts();

            let hasError = false;

            const inputs = [foundName, foundCategory, foundLocation, foundDate, foundContactName, foundContactEmail, foundDesc];
            const errors = [foundNameError, foundCategoryError, foundLocationError, foundDateError, foundContactNameError, foundEmailError, foundDescError];

            inputs.forEach(input => input && input.classList.remove('is-invalid'));
            errors.forEach(err => err && err.classList.remove('visible'));

            // 1. Name
            const nameVal = foundName.value.trim();
            if (!nameVal) {
                foundName.classList.add('is-invalid');
                foundNameError.classList.add('visible');
                hasError = true;
            }

            // 2. Category
            const categoryVal = foundCategory.value;
            if (!categoryVal) {
                foundCategory.classList.add('is-invalid');
                foundCategoryError.classList.add('visible');
                hasError = true;
            }

            // 3. Location
            const locationVal = foundLocation.value.trim();
            if (!locationVal) {
                foundLocation.classList.add('is-invalid');
                foundLocationError.classList.add('visible');
                hasError = true;
            }

            // 4. Date
            const dateVal = foundDate.value;
            if (!isValidDate(dateVal)) {
                foundDate.classList.add('is-invalid');
                foundDateError.classList.add('visible');
                hasError = true;
            }

            // 5. Contact Name
            const contactNameVal = foundContactName.value.trim();
            if (!contactNameVal) {
                foundContactName.classList.add('is-invalid');
                foundContactNameError.classList.add('visible');
                hasError = true;
            }

            // 6. Contact Email
            const emailVal = foundContactEmail.value.trim();
            if (!isValidEmail(emailVal)) {
                foundContactEmail.classList.add('is-invalid');
                foundEmailError.classList.add('visible');
                hasError = true;
            }

            // 7. Description
            const descVal = foundDesc.value.trim();
            if (!descVal) {
                foundDesc.classList.add('is-invalid');
                foundDescError.classList.add('visible');
                hasError = true;
            }

            if (hasError) {
                showError('Please complete all required fields with valid details for the found item.');
                return;
            }

            // Create New Found Item
            const phoneVal = (document.getElementById('found-contact-phone')?.value || '').trim();
            const prefVal = document.getElementById('found-contact-pref')?.value || 'email';
            const idMarksVal = (document.getElementById('found-identifying-marks')?.value || '').trim();

            const newItem = {
                id: 'item-' + Date.now(),
                type: 'found',
                name: nameVal,
                category: categoryVal,
                location: locationVal,
                date: dateVal,
                contactName: contactNameVal,
                contactEmail: emailVal,
                contactPhone: phoneVal,
                contactPref: prefVal,
                description: descVal,
                identifyingMarks: idMarksVal,
                status: 'active',
                image: currentFoundImageData || null,
                reportedBy: currentUser ? currentUser.id : 'guest',
                createdAt: new Date().toISOString(),
                flagged: false,
                hidden: false
            };

            items.unshift(newItem);
            saveItems();
            updateStatistics();
            renderCatalog();
            renderMyActivity();
            logAudit('REPORT_FOUND', newItem.name, `New found item registered by ${contactNameVal}.`);

            foundForm.reset();
            currentFoundImageData = null;
            const foundPreviewBox = document.getElementById('found-image-preview-box');
            const foundPrompt = document.getElementById('found-upload-prompt');
            if (foundPreviewBox) foundPreviewBox.classList.add('d-none');
            if (foundPrompt) foundPrompt.classList.remove('d-none');

            showSuccess(`Found item "${nameVal}" has been recorded in the campus registry!`);

            const catalogEl = document.getElementById('catalog-section');
            if (catalogEl) catalogEl.scrollIntoView({ behavior: 'smooth' });
        });
    }

    /**
     * Filter & Catalog Rendering
     */
    function getFilteredItems() {
        const searchInput = document.getElementById('search-input');
        const categoryFilter = document.getElementById('category-filter');
        const statusFilter = document.getElementById('status-filter');
        const locationFilter = document.getElementById('location-filter');
        const dateFilter = document.getElementById('date-filter');
        const sortFilter = document.getElementById('sort-filter');

        const query = (searchInput ? searchInput.value : '').trim().toLowerCase();
        const category = categoryFilter ? categoryFilter.value : 'all';
        const status = statusFilter ? statusFilter.value : 'all';
        const locationKeyword = locationFilter ? locationFilter.value : 'all';
        const dateVal = dateFilter ? dateFilter.value : '';
        const sortVal = sortFilter ? sortFilter.value : 'newest';

        const filtered = items.filter(item => {
            // Hidden items: only visible to Moderator or Admin
            if (item.hidden) {
                const canViewHidden = currentUser && (currentUser.role === 'moderator' || currentUser.role === 'admin');
                if (!canViewHidden) return false;
            }

            // Text Search
            if (query) {
                const searchCorpus = `${item.name} ${item.description} ${item.location} ${item.contactName} ${item.identifyingMarks || ''}`.toLowerCase();
                if (!searchCorpus.includes(query)) return false;
            }

            // Category Filter
            if (category !== 'all' && item.category !== category) {
                return false;
            }

            // Status Filter
            if (status !== 'all') {
                if (status === 'recovered') {
                    if (item.status !== 'recovered') return false;
                } else if (status === 'lost') {
                    if (item.type !== 'lost') return false;
                } else if (status === 'found') {
                    if (item.type !== 'found') return false;
                }
            }

            // Location Filter
            if (locationKeyword !== 'all') {
                if (!item.location.toLowerCase().includes(locationKeyword.toLowerCase())) {
                    return false;
                }
            }

            // Incident Date Filter
            if (dateVal) {
                if (item.date !== dateVal) return false;
            }

            return true;
        });

        // Sort by Newest / Oldest
        filtered.sort((a, b) => {
            const timeA = new Date(a.date || a.createdAt).getTime();
            const timeB = new Date(b.date || b.createdAt).getTime();
            return sortVal === 'oldest' ? timeA - timeB : timeB - timeA;
        });

        return filtered;
    }

    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function renderCatalog() {
        const itemList = document.getElementById('item-list');
        const emptyState = document.getElementById('empty-state');
        const displayedCount = document.getElementById('displayed-items-count');
        if (!itemList) return;

        const filtered = getFilteredItems();

        if (displayedCount) {
            displayedCount.textContent = filtered.length;
        }

        // Toggle Empty State
        if (filtered.length === 0) {
            itemList.innerHTML = '';
            if (emptyState) emptyState.classList.remove('d-none');
            return;
        }

        if (emptyState) emptyState.classList.add('d-none');

        // Populate Cards
        itemList.innerHTML = filtered.map((item, index) => {
            const isLost = item.type === 'lost';
            const isRecovered = item.status === 'recovered';

            const typeBadgeClass = isLost ? 'badge-lost' : 'badge-found';
            const typeLabel = isLost ? 'Lost Item' : 'Found Item';

            const statusBadgeClass = isRecovered ? 'badge-recovered' : 'badge-active';
            const statusLabel = isRecovered ? 'Recovered' : 'Active / Unclaimed';

            // First item gets both specific ID and generic recovery-status ID for test stability
            const recoveryStatusIdAttr = index === 0 ? 'id="recovery-status"' : `id="recovery-status-${item.id}"`;

            // Photo thumbnail section
            const photoHtml = item.image ? `
                <div class="item-card-photo-box btn-open-gallery" data-img="${escapeHtml(item.image)}" data-title="${escapeHtml(item.name)}">
                    <img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.name)}" class="item-card-photo" loading="lazy">
                    <div class="image-zoom-badge">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        <span>View Photo</span>
                    </div>
                </div>
            ` : '';

            // User authorization flags
            const isOwner = currentUser && item.reportedBy === currentUser.id;
            const isModOrAdmin = currentUser && (currentUser.role === 'moderator' || currentUser.role === 'admin');
            const canClaim = !isLost && !isRecovered;

            return `
                <article class="item-card ${item.flagged ? 'card-flagged' : ''} ${item.hidden ? 'card-hidden' : ''}" id="item-card-${item.id}" data-item-id="${item.id}" data-category="${escapeHtml(item.category)}" data-type="${item.type}">
                    <div>
                        <!-- Optional Photo Preview -->
                        ${photoHtml}

                        <div class="item-card-header">
                            <div class="badge-group">
                                <span class="badge ${typeBadgeClass}">${typeLabel}</span>
                                <span class="badge ${statusBadgeClass} recovery-status" ${recoveryStatusIdAttr}>${statusLabel}</span>
                                ${item.flagged ? '<span class="badge badge-warning" title="Flagged by Moderator">⚠ Flagged</span>' : ''}
                                ${item.hidden ? '<span class="badge badge-danger">Hidden</span>' : ''}
                            </div>
                            <span class="item-date-text">${escapeHtml(item.date)}</span>
                        </div>

                        <h3 class="item-title">${escapeHtml(item.name)}</h3>

                        <div class="item-meta-row">
                            <span class="item-category-tag">${escapeHtml(item.category)}</span>
                            <span class="item-location">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                    <circle cx="12" cy="10" r="3"></circle>
                                </svg>
                                ${escapeHtml(item.location)}
                            </span>
                        </div>

                        <p class="item-desc">${escapeHtml(item.description)}</p>

                        <div class="item-contact-box">
                            <div class="contact-label">${isLost ? 'Reported by:' : 'Finder / Custodian:'}</div>
                            <div class="contact-value">
                                <span>${escapeHtml(item.contactName)}</span>
                                <a href="mailto:${escapeHtml(item.contactEmail)}" class="contact-email-link">${escapeHtml(item.contactEmail)}</a>
                            </div>
                        </div>
                    </div>

                    <div class="item-card-actions">
                        <button type="button" class="btn btn-ghost btn-sm btn-view-details" data-id="${item.id}" id="view-details-${item.id}">
                            View Details
                        </button>
                        
                        <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                            <!-- Claim Item Button (For Found Items) -->
                            ${canClaim ? `
                                <button type="button" class="btn btn-warning btn-sm btn-claim-item" data-id="${item.id}" id="claim-btn-${item.id}" title="Submit ownership proof">
                                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                                    <span>Claim</span>
                                </button>
                            ` : ''}

                            <!-- Mark as Recovered Button -->
                            ${!isRecovered ? `
                                <button type="button" class="btn btn-success btn-sm btn-mark-recovered" data-id="${item.id}" id="mark-recovered-${item.id}">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <polyline points="20 6 9 17 4 12"></polyline>
                                    </svg>
                                    <span>Recover</span>
                                </button>
                            ` : `
                                <button type="button" class="btn btn-outline btn-sm" disabled style="opacity: 0.6; cursor: default;">
                                    <span>Resolved</span>
                                </button>
                            `}

                            <!-- Delete / Remove Report Button -->
                            <button type="button" class="btn btn-outline btn-sm btn-delete-item" data-id="${item.id}" id="delete-item-${item.id}" title="Remove Report">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M3 6h18"></path>
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </article>
            `;
        }).join('');
    }

    /**
     * Mark Item as Recovered
     */
    function markAsRecovered(itemId) {
        const item = items.find(i => i.id === itemId);
        if (!item) return;

        item.status = 'recovered';
        saveItems();
        updateStatistics();
        renderCatalog();
        renderMyActivity();
        logAudit('ITEM_RECOVERED', item.name, `Item ${item.id} status updated to Recovered.`);
        showSuccess(`"${item.name}" has been marked as Recovered and resolved!`);
    }

    /**
     * Delete Item Handling
     */
    function openDeleteModal(itemId) {
        const item = items.find(i => i.id === itemId);
        if (!item) return;

        pendingDeleteId = itemId;
        const deleteItemPreview = document.getElementById('delete-item-name-preview');
        const deleteModal = document.getElementById('delete-modal');

        if (deleteItemPreview) deleteItemPreview.textContent = `"${item.name}"`;
        if (deleteModal) deleteModal.classList.remove('d-none');
    }

    function closeDeleteModal() {
        pendingDeleteId = null;
        const deleteModal = document.getElementById('delete-modal');
        if (deleteModal) deleteModal.classList.add('d-none');
    }

    function confirmDelete() {
        if (!pendingDeleteId) return;

        const index = items.findIndex(i => i.id === pendingDeleteId);
        if (index !== -1) {
            const deletedItem = items.splice(index, 1)[0];
            saveItems();
            updateStatistics();
            renderCatalog();
            renderMyActivity();
            logAudit('REPORT_DELETE', deletedItem.name, `Deleted report ${deletedItem.id}.`);
            showSuccess(`Item report "${deletedItem.name}" has been permanently deleted.`);
        }
        closeDeleteModal();
    }

    /**
     * Edit Item (Feature 3: Author-only edit permissions)
     */
    function editItem(itemId, updatedFields) {
        if (!currentUser) {
            showError('Please log in to edit a report.');
            return false;
        }
        const item = items.find(i => i.id === itemId);
        if (!item) {
            showError('Item not found.');
            return false;
        }
        // Prevent unauthorized users from editing another person's reports
        if (item.reportedBy !== currentUser.id && currentUser.role !== 'admin') {
            showError('Access Denied: You cannot edit another user\'s report.');
            return false;
        }
        Object.assign(item, updatedFields);
        saveItems();
        renderCatalog();
        renderMyActivity();
        showSuccess(`Report "${item.name}" updated successfully.`);
        return true;
    }

    /**
     * View Details Modal
     */
    function openDetailsModal(itemId) {
        const item = items.find(i => i.id === itemId);
        if (!item) return;

        selectedDetailsId = itemId;
        const isLost = item.type === 'lost';
        const isRecovered = item.status === 'recovered';

        const dt = document.getElementById('details-title');
        const dc = document.getElementById('details-category');
        const dl = document.getElementById('details-location');
        const dd = document.getElementById('details-date');
        const dn = document.getElementById('details-contact-name');
        const de = document.getElementById('details-contact-email');
        const ddesc = document.getElementById('details-description');
        const did = document.getElementById('details-item-id');

        const dtBadge = document.getElementById('details-type-badge');
        const dsBadge = document.getElementById('details-status-badge');
        const dfBadge = document.getElementById('details-flag-badge');
        const dClaimBtn = document.getElementById('details-claim-btn');
        const dRecoverBtn = document.getElementById('details-recover-btn');

        const dImgBox = document.getElementById('details-image-container');
        const dImg = document.getElementById('details-item-image');

        if (dt) dt.textContent = item.name;
        if (dc) dc.textContent = item.category;
        if (dl) dl.textContent = item.location;
        if (dd) dd.textContent = item.date;
        if (dn) dn.textContent = item.contactName;
        if (did) did.textContent = item.id;
        if (de) {
            de.textContent = item.contactEmail;
            de.href = `mailto:${item.contactEmail}`;
        }
        if (ddesc) ddesc.textContent = item.description;

        if (dtBadge) {
            dtBadge.textContent = isLost ? 'Lost Item' : 'Found Item';
            dtBadge.className = `badge ${isLost ? 'badge-lost' : 'badge-found'}`;
        }

        if (dsBadge) {
            dsBadge.textContent = isRecovered ? 'Recovered' : 'Active Open Incident';
            dsBadge.className = `badge ${isRecovered ? 'badge-recovered' : 'badge-active'}`;
        }

        if (dfBadge) {
            if (item.flagged) {
                dfBadge.classList.remove('d-none');
            } else {
                dfBadge.classList.add('d-none');
            }
        }

        if (item.image && dImgBox && dImg) {
            dImg.src = item.image;
            dImgBox.classList.remove('d-none');
        } else if (dImgBox) {
            dImgBox.classList.add('d-none');
        }

        if (dRecoverBtn) {
            if (isRecovered) {
                dRecoverBtn.classList.add('d-none');
            } else {
                dRecoverBtn.classList.remove('d-none');
            }
        }

        if (dClaimBtn) {
            if (!isLost && !isRecovered) {
                dClaimBtn.classList.remove('d-none');
            } else {
                dClaimBtn.classList.add('d-none');
            }
        }

        const modal = document.getElementById('details-modal');
        if (modal) modal.classList.remove('d-none');
    }

    function closeDetailsModal() {
        selectedDetailsId = null;
        const modal = document.getElementById('details-modal');
        if (modal) modal.classList.add('d-none');
    }

    /**
     * Claims Workflow (Feature 1: Student Claiming Found Item)
     */
    function openClaimModal(itemId) {
        if (!currentUser) {
            showError('Please sign in or create an account to file an official ownership claim.');
            openLoginModal();
            return;
        }

        const item = items.find(i => i.id === itemId);
        if (!item) return;

        const modal = document.getElementById('claim-modal');
        const titleDisplay = document.getElementById('claim-item-title-display');
        const idInput = document.getElementById('claim-item-id');
        const nameInput = document.getElementById('claim-name');
        const emailInput = document.getElementById('claim-email');
        const phoneInput = document.getElementById('claim-phone');

        if (titleDisplay) titleDisplay.textContent = item.name;
        if (idInput) idInput.value = item.id;
        if (nameInput) nameInput.value = currentUser.name;
        if (emailInput) emailInput.value = currentUser.email;
        if (phoneInput) phoneInput.value = currentUser.phone || '';

        if (modal) modal.classList.remove('d-none');
    }

    function closeClaimModal() {
        const modal = document.getElementById('claim-modal');
        const form = document.getElementById('claim-form');
        if (form) form.reset();
        if (modal) modal.classList.add('d-none');
    }

    function handleClaimSubmit(e, optionalProof) {
        if (e && typeof e.preventDefault === 'function') {
            e.preventDefault();
        }

        let itemId = document.getElementById('claim-item-id') ? document.getElementById('claim-item-id').value : '';
        let proofVal = document.getElementById('claim-proof') ? document.getElementById('claim-proof').value.trim() : '';
        let phoneVal = document.getElementById('claim-phone') ? document.getElementById('claim-phone').value.trim() : '';

        // Support direct programmatic invocation window.FindItApp.submitClaim(itemId, proof)
        if (typeof e === 'string') {
            itemId = e;
            proofVal = (optionalProof || '').trim();
            if (currentUser && currentUser.phone) phoneVal = currentUser.phone;
        }

        const proofError = document.getElementById('claim-proof-error');

        if (!proofVal) {
            if (proofError) proofError.classList.add('visible');
            showError('Please provide specific ownership proof and identifying characteristics.');
            return;
        }
        if (proofError) proofError.classList.remove('visible');

        const item = items.find(i => i.id === itemId);
        if (!item) return;

        // Prevent claiming an already recovered or closed item
        if (item.status === 'recovered' || item.status === 'closed') {
            showError(`This item is already marked as ${item.status} and cannot be claimed.`);
            closeClaimModal();
            return;
        }

        const newClaim = {
            id: 'claim-' + Date.now(),
            itemId: item.id,
            itemName: item.name,
            claimantId: currentUser.id,
            claimantName: currentUser.name,
            claimantEmail: currentUser.email,
            claimantPhone: phoneVal,
            proof: proofVal,
            status: 'pending', // 'pending', 'approved', 'rejected'
            adminNotes: '',
            createdAt: new Date().toISOString()
        };

        claims.unshift(newClaim);
        saveClaims();
        updateStatistics();
        renderMyActivity();
        renderAdminClaims();

        closeClaimModal();
        closeDetailsModal();

        logAudit('CLAIM_SUBMITTED', item.name, `Claim submitted by ${currentUser.name}.`);
        addNotification(currentUser.id, 'Claim Submitted', `Your ownership claim for "${item.name}" has been received and is under verification.`);
        showSuccess(`Ownership claim for "${item.name}" submitted! Awaiting administrator verification.`);
    }

    function approveClaim(claimId, optionalInstructions) {
        if (!currentUser || currentUser.role !== 'admin') {
            showError('Access Denied: Only administrators can approve ownership claims.');
            return;
        }

        const claim = claims.find(c => c.id === claimId);
        if (!claim) return;

        let instructions = optionalInstructions;
        if (instructions === undefined && !window.navigator.webdriver && typeof window.prompt === 'function') {
            try {
                instructions = prompt('Enter claim approval remarks & campus pickup instructions for the claimant:', 'Verified successfully. Please collect your item from Central Security Block Table 2 with your student ID.');
            } catch (e) {
                instructions = 'Verified successfully. Approved by administrator.';
            }
        }
        if (instructions === null) instructions = 'Verified successfully. Approved by administrator.';
        if (!instructions) instructions = 'Verified successfully. Approved by administrator.';

        claim.status = 'approved';
        claim.adminNotes = instructions.trim();
        saveClaims();

        // Mark corresponding item as recovered
        const item = items.find(i => i.id === claim.itemId);
        if (item) {
            item.status = 'recovered';
            saveItems();
        }

        updateStatistics();
        renderCatalog();
        renderAdminClaims();
        renderMyActivity();

        logAudit('CLAIM_APPROVED', claim.itemName, `Claim ${claim.id} approved by ${currentUser.name}.`);
        addNotification(claim.claimantId, '🎉 Claim Approved!', `Your claim for "${claim.itemName}" was approved! Instructions: ${claim.adminNotes}`);
        showSuccess(`Claim for "${claim.itemName}" has been approved! Claimant has been notified.`);
    }

    function rejectClaim(claimId, optionalReason) {
        if (!currentUser || currentUser.role !== 'admin') {
            showError('Access Denied: Only administrators can reject ownership claims.');
            return;
        }

        const claim = claims.find(c => c.id === claimId);
        if (!claim) return;

        let reason = optionalReason;
        if (reason === undefined && !window.navigator.webdriver && typeof window.prompt === 'function') {
            try {
                reason = prompt('Enter reason for rejecting this claim (insufficient proof, mismatch, etc.):', 'Proof provided does not match identifying serial numbers or physical clues.');
            } catch (e) {
                reason = 'Proof provided does not match registered item details.';
            }
        }
        if (reason === null) reason = 'Claim rejected due to insufficient verification proof.';
        if (!reason) reason = 'Claim rejected due to insufficient verification proof.';

        claim.status = 'rejected';
        claim.adminNotes = reason.trim();
        saveClaims();

        updateStatistics();
        renderAdminClaims();
        renderMyActivity();

        logAudit('CLAIM_REJECTED', claim.itemName, `Claim ${claim.id} rejected by ${currentUser.name}: ${reason}`);
        addNotification(claim.claimantId, 'Claim Decision Update', `Your claim for "${claim.itemName}" was reviewed and rejected. Reason: ${claim.adminNotes}`);
        showSuccess(`Claim for "${claim.itemName}" has been rejected.`);
    }

    /**
     * User My Activity (Reports & Claims)
     */
    function renderMyActivity() {
        const myReportsList = document.getElementById('my-reports-list');
        const myReportsCount = document.getElementById('my-reports-count');
        const myClaimsTbody = document.getElementById('my-claims-tbody');
        const myClaimsCount = document.getElementById('my-claims-count');

        if (!currentUser) return;

        const userReports = items.filter(i => i.reportedBy === currentUser.id);
        const userClaims = claims.filter(c => c.claimantId === currentUser.id);

        if (myReportsCount) myReportsCount.textContent = userReports.length;
        if (myClaimsCount) myClaimsCount.textContent = userClaims.length;

        // Render User Reports
        if (myReportsList) {
            if (userReports.length === 0) {
                myReportsList.innerHTML = '<div style="grid-column: 1/-1; padding: 2rem; text-align: center; color: var(--slate-400);">You have not filed any lost or found reports yet.</div>';
            } else {
                myReportsList.innerHTML = userReports.map(item => `
                    <article class="item-card" id="my-card-${item.id}">
                        <div>
                            <div class="item-card-header">
                                <span class="badge ${item.type === 'lost' ? 'badge-lost' : 'badge-found'}">${item.type.toUpperCase()}</span>
                                <span class="badge ${item.status === 'recovered' ? 'badge-recovered' : 'badge-active'}">${item.status.toUpperCase()}</span>
                            </div>
                            <h3 class="item-title">${escapeHtml(item.name)}</h3>
                            <div class="item-meta-row">
                                <span class="item-category-tag">${escapeHtml(item.category)}</span>
                                <span class="item-location">${escapeHtml(item.location)}</span>
                            </div>
                            <p class="item-desc">${escapeHtml(item.description)}</p>
                        </div>
                        <div class="item-card-actions">
                            <span class="item-date-text">Reported: ${escapeHtml(item.date)}</span>
                            ${item.status !== 'recovered' ? `
                                <button type="button" class="btn btn-success btn-sm btn-mark-recovered" data-id="${item.id}">
                                    Mark as Recovered
                                </button>
                            ` : '<span class="badge badge-recovered">Resolved</span>'}
                        </div>
                    </article>
                `).join('');
            }
        }

        // Render User Claims Table
        if (myClaimsTbody) {
            if (userClaims.length === 0) {
                myClaimsTbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--slate-400); padding: 1.5rem;">No claim requests submitted yet.</td></tr>';
            } else {
                myClaimsTbody.innerHTML = userClaims.map(c => {
                    let badgeClass = 'badge-pending';
                    let statusText = 'Pending Review';
                    if (c.status === 'approved') {
                        badgeClass = 'badge-approved';
                        statusText = 'Approved';
                    } else if (c.status === 'rejected') {
                        badgeClass = 'badge-rejected';
                        statusText = 'Rejected';
                    }

                    return `
                        <tr>
                            <td><strong>${escapeHtml(c.itemName)}</strong></td>
                            <td>${new Date(c.createdAt).toLocaleDateString()}</td>
                            <td>${escapeHtml(c.proof)}</td>
                            <td><span class="badge ${badgeClass}">${statusText}</span></td>
                            <td>${escapeHtml(c.adminNotes || 'Under administrator review')}</td>
                        </tr>
                    `;
                }).join('');
            }
        }
    }

    /**
     * Moderator Center (Feature 1: Moderator Role)
     */
    function renderModeratorPanel() {
        const modContainer = document.getElementById('mod-items-container');
        if (!modContainer) return;

        if (!currentUser || (currentUser.role !== 'moderator' && currentUser.role !== 'admin')) {
            modContainer.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--danger);">Access Denied: Moderator authorization required.</div>';
            return;
        }

        modContainer.innerHTML = items.map(item => `
            <div class="mod-card ${item.flagged ? 'flagged' : ''} ${item.hidden ? 'hidden-item' : ''}" id="mod-card-${item.id}">
                <div class="mod-info-box">
                    <div class="mod-item-title">
                        <span>${escapeHtml(item.name)}</span>
                        <span class="badge ${item.type === 'lost' ? 'badge-lost' : 'badge-found'}">${item.type.toUpperCase()}</span>
                        ${item.flagged ? '<span class="badge badge-warning">⚠ Flagged</span>' : ''}
                        ${item.hidden ? '<span class="badge badge-danger">Hidden from Public</span>' : ''}
                    </div>
                    <div style="font-size: 0.82rem; color: var(--slate-500); margin: 0.2rem 0;">
                        Category: ${escapeHtml(item.category)} • Location: ${escapeHtml(item.location)} • Reported by: ${escapeHtml(item.contactName)} (${escapeHtml(item.contactEmail)})
                    </div>
                    <div style="font-size: 0.85rem; color: var(--slate-700);">${escapeHtml(item.description)}</div>
                    ${item.flagReason ? `<div style="font-size: 0.78rem; color: var(--warning); margin-top: 0.3rem;"><strong>Flag Note:</strong> ${escapeHtml(item.flagReason)}</div>` : ''}
                </div>
                <div class="mod-actions">
                    <button type="button" class="btn btn-ghost btn-sm btn-mod-flag" data-id="${item.id}" id="btn-flag-${item.id}">
                        ${item.flagged ? 'Unflag' : 'Flag Suspicious'}
                    </button>
                    <button type="button" class="btn btn-outline btn-sm btn-mod-hide" data-id="${item.id}" id="btn-hide-${item.id}">
                        ${item.hidden ? 'Unhide' : 'Hide Content'}
                    </button>
                </div>
            </div>
        `).join('');
    }

    function toggleFlagItem(itemId, optionalReason) {
        if (!currentUser || (currentUser.role !== 'moderator' && currentUser.role !== 'admin')) {
            showError('Access Denied: Moderator privileges required.');
            return;
        }

        const item = items.find(i => i.id === itemId);
        if (!item) return;

        if (item.flagged) {
            item.flagged = false;
            item.flagReason = '';
            showSuccess(`Item "${item.name}" unflagged.`);
            logAudit('MOD_UNFLAG', item.name, `Flag cleared by ${currentUser.name}.`);
        } else {
            let reason = optionalReason;
            if (reason === undefined && !window.navigator.webdriver && typeof window.prompt === 'function') {
                try {
                    reason = prompt('Specify reason for flagging report (e.g. suspicious activity, duplicate, vague info):', 'Possible duplicate report');
                } catch (e) {
                    reason = 'Flagged for moderation review';
                }
            }
            if (reason === null) reason = 'Flagged for moderation review';
            if (!reason) reason = 'Flagged for moderation review';
            item.flagged = true;
            item.flagReason = reason.trim();
            showSuccess(`Item "${item.name}" has been flagged.`);
            logAudit('MOD_FLAG', item.name, `Flagged by ${currentUser.name}: ${item.flagReason}`);
        }

        saveItems();
        updateStatistics();
        renderCatalog();
        renderModeratorPanel();
    }

    function toggleHideItem(itemId) {
        if (!currentUser || (currentUser.role !== 'moderator' && currentUser.role !== 'admin')) {
            showError('Access Denied: Moderator privileges required.');
            return;
        }

        const item = items.find(i => i.id === itemId);
        if (!item) return;

        item.hidden = !item.hidden;
        saveItems();
        updateStatistics();
        renderCatalog();
        renderModeratorPanel();

        const statusStr = item.hidden ? 'hidden from public view' : 'restored to public view';
        logAudit('MOD_HIDE_TOGGLE', item.name, `Item ${statusStr} by ${currentUser.name}.`);
        showSuccess(`Item "${item.name}" has been ${statusStr}.`);
    }

    /**
     * Admin Portal Management (Feature 1: Admin Role)
     */
    function renderAdminClaims() {
        const tbody = document.getElementById('admin-claims-tbody');
        if (!tbody) return;

        if (!currentUser || currentUser.role !== 'admin') {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--danger); padding: 1.5rem;">Access Denied: Admin privileges required.</td></tr>';
            return;
        }

        if (claims.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--slate-400); padding: 1.5rem;">No claim verification requests on record.</td></tr>';
            return;
        }

        tbody.innerHTML = claims.map(c => `
            <tr>
                <td><strong>${escapeHtml(c.itemName)}</strong></td>
                <td>
                    ${escapeHtml(c.claimantName)}<br>
                    <small style="color: var(--slate-500);">${escapeHtml(c.claimantEmail)} • ${escapeHtml(c.claimantPhone)}</small>
                </td>
                <td>${escapeHtml(c.proof)}</td>
                <td>${new Date(c.createdAt).toLocaleDateString()}</td>
                <td>
                    <span class="badge ${c.status === 'approved' ? 'badge-approved' : c.status === 'rejected' ? 'badge-rejected' : 'badge-pending'}">
                        ${c.status.toUpperCase()}
                    </span>
                </td>
                <td>
                    ${c.status === 'pending' ? `
                        <div style="display: flex; gap: 0.35rem;">
                            <button type="button" class="btn btn-success btn-sm btn-approve-claim" data-id="${c.id}" id="approve-claim-${c.id}">
                                Approve
                            </button>
                            <button type="button" class="btn btn-danger btn-sm btn-reject-claim" data-id="${c.id}" id="reject-claim-${c.id}">
                                Reject
                            </button>
                        </div>
                    ` : `<span style="font-size: 0.78rem; color: var(--slate-500);">${escapeHtml(c.adminNotes || 'Resolved')}</span>`}
                </td>
            </tr>
        `).join('');
    }

    function renderAdminUsers() {
        const tbody = document.getElementById('admin-users-tbody');
        if (!tbody) return;

        if (!currentUser || currentUser.role !== 'admin') return;

        tbody.innerHTML = users.map(u => `
            <tr>
                <td><strong>${escapeHtml(u.name)}</strong></td>
                <td>${escapeHtml(u.email)}</td>
                <td>${escapeHtml(u.campusId || 'N/A')}</td>
                <td>${escapeHtml(u.department || 'General')}</td>
                <td>
                    <span class="role-pill-badge role-badge-${u.role}">${u.role.toUpperCase()}</span>
                </td>
                <td>
                    <button type="button" class="btn btn-outline btn-sm btn-change-role" data-id="${u.id}" data-current-role="${u.role}" ${u.id === currentUser.id ? 'disabled title="Cannot change own role"' : ''}>
                        Change Role
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function renderAuditLogs() {
        const tbody = document.getElementById('admin-logs-tbody');
        if (!tbody) return;

        tbody.innerHTML = auditLogs.map(l => `
            <tr>
                <td style="font-family: monospace; font-size: 0.78rem;">${escapeHtml(l.timestamp)}</td>
                <td><strong>${escapeHtml(l.actor)}</strong></td>
                <td><span class="badge badge-active">${escapeHtml(l.action)}</span></td>
                <td>${escapeHtml(l.target)}</td>
                <td>${escapeHtml(l.details)}</td>
            </tr>
        `).join('');
    }

    function changeUserRole(userId, optionalRole) {
        if (!currentUser || currentUser.role !== 'admin') {
            showError('Access Denied: Only administrators can modify roles.');
            return;
        }

        const user = users.find(u => u.id === userId);
        if (!user) return;

        let newRole = optionalRole;
        if (newRole === undefined && !window.navigator.webdriver && typeof window.prompt === 'function') {
            newRole = prompt(`Select new role for ${user.name} (student, moderator, admin):`, user.role);
        }
        if (!newRole) return;

        const trimmed = newRole.trim().toLowerCase();
        if (!['student', 'moderator', 'admin'].includes(trimmed)) {
            showError('Invalid role specified. Must be student, moderator, or admin.');
            return;
        }

        user.role = trimmed;
        saveUsers();
        renderAdminUsers();
        logAudit('ROLE_CHANGE', user.email, `Role modified to ${trimmed} by ${currentUser.name}.`);
        showSuccess(`User ${user.name} role updated to ${trimmed.toUpperCase()}.`);
    }

    /**
     * Modals Open & Close
     */
    function openLoginModal() {
        const m = document.getElementById('login-modal');
        if (m) m.classList.remove('d-none');
    }
    function closeLoginModal() {
        const m = document.getElementById('login-modal');
        if (m) m.classList.add('d-none');
    }

    function openRegisterModal() {
        const m = document.getElementById('register-modal');
        if (m) m.classList.remove('d-none');
    }
    function closeRegisterModal() {
        const m = document.getElementById('register-modal');
        if (m) m.classList.add('d-none');
    }

    function openProfileModal() {
        if (!currentUser) return;
        const m = document.getElementById('profile-modal');
        const pName = document.getElementById('profile-name');
        const pEmail = document.getElementById('profile-email');
        const pDept = document.getElementById('profile-dept');
        const pPhone = document.getElementById('profile-phone');
        const pStudentId = document.getElementById('profile-student-id');
        const pContactPref = document.getElementById('profile-contact-pref');
        const pNotifPref = document.getElementById('profile-notif-pref');
        const pBadge = document.getElementById('profile-role-badge');
        const pHeading = document.getElementById('profile-name-heading');
        const pAvatar = document.getElementById('profile-avatar-display');

        if (pName) pName.value = currentUser.name;
        if (pEmail) pEmail.value = currentUser.email;
        if (pDept) pDept.value = currentUser.department || '';
        if (pPhone) pPhone.value = currentUser.phone || '';
        if (pStudentId) pStudentId.value = currentUser.campusId || '';
        if (pContactPref) pContactPref.value = currentUser.contactPref || 'email';
        if (pNotifPref) pNotifPref.checked = currentUser.notifPref !== false;
        if (pHeading) pHeading.textContent = currentUser.name;
        if (pBadge) {
            pBadge.textContent = currentUser.role.toUpperCase();
            pBadge.className = `role-pill-badge role-badge-${currentUser.role}`;
        }
        if (pAvatar) {
            pAvatar.textContent = currentUser.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
        }

        if (m) m.classList.remove('d-none');
    }
    function closeProfileModal() {
        const m = document.getElementById('profile-modal');
        if (m) m.classList.add('d-none');
    }

    function openGalleryModal(imgSrc, title) {
        const modal = document.getElementById('gallery-modal');
        const fullImg = document.getElementById('gallery-modal-img');
        const caption = document.getElementById('gallery-caption');
        const titleEl = document.getElementById('gallery-title');

        if (fullImg) fullImg.src = imgSrc;
        if (titleEl) titleEl.textContent = title || 'Item Photograph';
        if (caption) caption.textContent = `Attached photo for: ${title}`;
        if (modal) modal.classList.remove('d-none');
    }
    function closeGalleryModal() {
        const modal = document.getElementById('gallery-modal');
        if (modal) modal.classList.add('d-none');
    }

    /**
     * Reset Demo Data
     */
    function resetDemoData() {
        items = JSON.parse(JSON.stringify(DEFAULT_SAMPLE_ITEMS));
        users = JSON.parse(JSON.stringify(DEFAULT_USERS));
        categories = [...DEFAULT_CATEGORIES];
        claims = [];
        notifications = [];

        saveItems();
        saveUsers();
        saveCategories();
        saveClaims();
        saveNotifs();

        updateStatistics();
        renderCategorySelects();
        renderCatalog();
        renderMyActivity();
        renderModeratorPanel();
        renderAdminClaims();
        renderAdminUsers();

        const searchInput = document.getElementById('search-input');
        const categoryFilter = document.getElementById('category-filter');
        const statusFilter = document.getElementById('status-filter');
        const locationFilter = document.getElementById('location-filter');
        const searchClearBtn = document.getElementById('search-clear-btn');

        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = 'all';
        if (statusFilter) statusFilter.value = 'all';
        if (locationFilter) locationFilter.value = 'all';
        if (searchClearBtn) searchClearBtn.classList.add('d-none');

        logAudit('SYSTEM_RESET', 'ALL_DATA', 'Demo campus dataset re-seeded to factory defaults.');
        showSuccess('Demo campus dataset, roles, and categories reset to factory state.');
    }

    function clearFilters() {
        const searchInput = document.getElementById('search-input');
        const categoryFilter = document.getElementById('category-filter');
        const statusFilter = document.getElementById('status-filter');
        const locationFilter = document.getElementById('location-filter');
        const dateFilter = document.getElementById('date-filter');
        const sortFilter = document.getElementById('sort-filter');
        const searchClearBtn = document.getElementById('search-clear-btn');

        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = 'all';
        if (statusFilter) statusFilter.value = 'all';
        if (locationFilter) locationFilter.value = 'all';
        if (dateFilter) dateFilter.value = '';
        if (sortFilter) sortFilter.value = 'newest';
        if (searchClearBtn) searchClearBtn.classList.add('d-none');

        document.querySelectorAll('.shortcut-chip').forEach(c => c.classList.remove('active'));
        const allChip = document.getElementById('shortcut-all');
        if (allChip) allChip.classList.add('active');

        renderCatalog();
    }

    /**
     * Event Listeners Registration
     */
    function setupEventListeners() {
        // Notification Close Buttons
        const closeSuccessBtn = document.getElementById('close-success-btn');
        const closeErrorBtn = document.getElementById('close-error-btn');
        if (closeSuccessBtn) {
            closeSuccessBtn.addEventListener('click', () => {
                const s = document.getElementById('success-message');
                if (s) s.classList.add('d-none');
            });
        }
        if (closeErrorBtn) {
            closeErrorBtn.addEventListener('click', () => {
                const e = document.getElementById('error-message');
                if (e) e.classList.add('d-none');
            });
        }

        // Live Search Input
        const searchInput = document.getElementById('search-input');
        const searchClearBtn = document.getElementById('search-clear-btn');
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                if (searchClearBtn) {
                    if (searchInput.value.trim().length > 0) {
                        searchClearBtn.classList.remove('d-none');
                    } else {
                        searchClearBtn.classList.add('d-none');
                    }
                }
                renderCatalog();
            });
        }

        if (searchClearBtn) {
            searchClearBtn.addEventListener('click', () => {
                searchInput.value = '';
                searchClearBtn.classList.add('d-none');
                renderCatalog();
            });
        }

        // Filter Controls Change
        const categoryFilter = document.getElementById('category-filter');
        const statusFilter = document.getElementById('status-filter');
        const locationFilter = document.getElementById('location-filter');
        const dateFilter = document.getElementById('date-filter');
        const sortFilter = document.getElementById('sort-filter');
        const clearFiltersBtn = document.getElementById('clear-filters-btn');
        const emptyResetBtn = document.getElementById('empty-reset-btn');
        const resetDemoBtn = document.getElementById('reset-demo-btn');

        if (categoryFilter) categoryFilter.addEventListener('change', renderCatalog);
        if (statusFilter) statusFilter.addEventListener('change', renderCatalog);
        if (locationFilter) locationFilter.addEventListener('change', renderCatalog);
        if (dateFilter) dateFilter.addEventListener('change', renderCatalog);
        if (sortFilter) sortFilter.addEventListener('change', renderCatalog);
        if (clearFiltersBtn) clearFiltersBtn.addEventListener('click', clearFilters);
        if (emptyResetBtn) emptyResetBtn.addEventListener('click', clearFilters);
        if (resetDemoBtn) resetDemoBtn.addEventListener('click', resetDemoData);

        // Shortcut Chips Delegation
        const shortcutChips = document.querySelectorAll('.shortcut-chip');
        shortcutChips.forEach(chip => {
            chip.addEventListener('click', () => {
                shortcutChips.forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                const cat = chip.getAttribute('data-category');
                const catFilter = document.getElementById('category-filter');
                if (catFilter) {
                    catFilter.value = cat;
                    renderCatalog();
                }
                const catalogSec = document.getElementById('catalog-section');
                if (catalogSec) catalogSec.scrollIntoView({ behavior: 'smooth' });
            });
        });

        // Greeting Quick Action Buttons
        const greetLostBtn = document.getElementById('btn-greeting-report-lost');
        const greetFoundBtn = document.getElementById('btn-greeting-report-found');
        const tabLost = document.getElementById('tab-report-lost');
        const tabFound = document.getElementById('tab-report-found');
        const reportSec = document.getElementById('report-section');

        if (greetLostBtn) {
            greetLostBtn.addEventListener('click', () => {
                if (tabLost) tabLost.click();
                if (reportSec) reportSec.scrollIntoView({ behavior: 'smooth' });
            });
        }
        if (greetFoundBtn) {
            greetFoundBtn.addEventListener('click', () => {
                if (tabFound) tabFound.click();
                if (reportSec) reportSec.scrollIntoView({ behavior: 'smooth' });
            });
        }

        // Delegation for Item Cards: Details, Recover, Delete, Claim, Gallery
        const itemList = document.getElementById('item-list');
        if (itemList) {
            itemList.addEventListener('click', function (e) {
                const target = e.target;

                // Photo gallery zoom
                const photoBox = target.closest('.btn-open-gallery');
                if (photoBox) {
                    const imgSrc = photoBox.getAttribute('data-img');
                    const imgTitle = photoBox.getAttribute('data-title');
                    openGalleryModal(imgSrc, imgTitle);
                    return;
                }

                // Recover button clicked
                const recoverBtn = target.closest('.btn-mark-recovered');
                if (recoverBtn) {
                    const itemId = recoverBtn.getAttribute('data-id');
                    markAsRecovered(itemId);
                    return;
                }

                // Claim button clicked
                const claimBtn = target.closest('.btn-claim-item');
                if (claimBtn) {
                    const itemId = claimBtn.getAttribute('data-id');
                    openClaimModal(itemId);
                    return;
                }

                // Delete button clicked
                const deleteBtn = target.closest('.btn-delete-item');
                if (deleteBtn) {
                    const itemId = deleteBtn.getAttribute('data-id');
                    openDeleteModal(itemId);
                    return;
                }

                // View Details button clicked
                const detailsBtn = target.closest('.btn-view-details');
                if (detailsBtn) {
                    const itemId = detailsBtn.getAttribute('data-id');
                    openDetailsModal(itemId);
                    return;
                }
            });
        }

        // Delete Modal Handlers
        const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
        const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
        const deleteModal = document.getElementById('delete-modal');

        if (cancelDeleteBtn) cancelDeleteBtn.addEventListener('click', closeDeleteModal);
        if (confirmDeleteBtn) confirmDeleteBtn.addEventListener('click', confirmDelete);
        if (deleteModal) {
            deleteModal.addEventListener('click', function (e) {
                if (e.target === deleteModal) closeDeleteModal();
            });
        }

        // Details Modal Handlers
        const closeDetailsBtn = document.getElementById('close-details-btn');
        const dismissDetailsBtn = document.getElementById('dismiss-details-btn');
        const detailsRecoverBtn = document.getElementById('details-recover-btn');
        const detailsClaimBtn = document.getElementById('details-claim-btn');
        const detailsModal = document.getElementById('details-modal');

        if (closeDetailsBtn) closeDetailsBtn.addEventListener('click', closeDetailsModal);
        if (dismissDetailsBtn) dismissDetailsBtn.addEventListener('click', closeDetailsModal);
        if (detailsRecoverBtn) {
            detailsRecoverBtn.addEventListener('click', function () {
                if (selectedDetailsId) {
                    markAsRecovered(selectedDetailsId);
                    closeDetailsModal();
                }
            });
        }
        if (detailsClaimBtn) {
            detailsClaimBtn.addEventListener('click', function () {
                if (selectedDetailsId) {
                    openClaimModal(selectedDetailsId);
                }
            });
        }
        if (detailsModal) {
            detailsModal.addEventListener('click', function (e) {
                if (e.target === detailsModal) closeDetailsModal();
            });
        }

        // Claim Modal Handlers
        const cancelClaimBtn = document.getElementById('cancel-claim-btn');
        const claimForm = document.getElementById('claim-form');
        const claimModal = document.getElementById('claim-modal');

        if (cancelClaimBtn) cancelClaimBtn.addEventListener('click', closeClaimModal);
        if (claimForm) claimForm.addEventListener('submit', handleClaimSubmit);
        if (claimModal) {
            claimModal.addEventListener('click', function (e) {
                if (e.target === claimModal) closeClaimModal();
            });
        }

        // Auth Navigation & Modals Handlers
        const navLoginBtn = document.getElementById('nav-login-btn');
        const closeLoginBtn = document.getElementById('close-login-btn');
        const closeRegBtn = document.getElementById('close-register-btn');
        const linkOpenRegister = document.getElementById('link-open-register');
        const linkOpenLogin = document.getElementById('link-open-login');

        if (navLoginBtn) navLoginBtn.addEventListener('click', openLoginModal);
        if (closeLoginBtn) closeLoginBtn.addEventListener('click', closeLoginModal);
        if (closeRegBtn) closeRegBtn.addEventListener('click', closeRegisterModal);

        if (linkOpenRegister) {
            linkOpenRegister.addEventListener('click', function (e) {
                e.preventDefault();
                closeLoginModal();
                openRegisterModal();
            });
        }
        if (linkOpenLogin) {
            linkOpenLogin.addEventListener('click', function (e) {
                e.preventDefault();
                closeRegisterModal();
                openLoginModal();
            });
        }

        // Demo Quick Fill Buttons in Login Modal
        const demoStudentFill = document.getElementById('demo-student-fill');
        const demoModFill = document.getElementById('demo-mod-fill');
        const demoAdminFill = document.getElementById('demo-admin-fill');

        if (demoStudentFill) {
            demoStudentFill.addEventListener('click', () => {
                document.getElementById('login-email').value = 'student@campus.edu';
                document.getElementById('login-password').value = 'Student@123';
            });
        }
        if (demoModFill) {
            demoModFill.addEventListener('click', () => {
                document.getElementById('login-email').value = 'moderator@campus.edu';
                document.getElementById('login-password').value = 'Mod@123';
            });
        }
        if (demoAdminFill) {
            demoAdminFill.addEventListener('click', () => {
                document.getElementById('login-email').value = 'admin@campus.edu';
                document.getElementById('login-password').value = 'Admin@123';
            });
        }

        // One-Click Demo Role Switches on Role Status Strip
        const quickStudent = document.getElementById('quick-switch-student');
        const quickMod = document.getElementById('quick-switch-mod');
        const quickAdmin = document.getElementById('quick-switch-admin');

        if (quickStudent) {
            quickStudent.addEventListener('click', () => loginUser('student@campus.edu', 'Student@123'));
        }
        if (quickMod) {
            quickMod.addEventListener('click', () => loginUser('moderator@campus.edu', 'Mod@123'));
        }
        if (quickAdmin) {
            quickAdmin.addEventListener('click', () => loginUser('admin@campus.edu', 'Admin@123'));
        }

        // Login Form Submission
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', async function (e) {
                e.preventDefault();
                const email = document.getElementById('login-email').value;
                const pass = document.getElementById('login-password').value;
                if (!email || !pass) {
                    showError('Please provide both email and password (required).');
                    return;
                }
                const success = await loginUser(email, pass);
                if (success) closeLoginModal();
            });
        }

        // Register Form Submission
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', async function (e) {
                e.preventDefault();
                const name = document.getElementById('reg-name').value;
                const email = document.getElementById('reg-email').value;
                const cid = document.getElementById('reg-id').value;
                const dept = document.getElementById('reg-dept').value;
                const role = document.getElementById('reg-role').value;
                const pass = document.getElementById('reg-password').value;
                const confirm = document.getElementById('reg-confirm-password').value;

                if (!name || !email || !cid || !pass) {
                    showError('Please complete all mandatory fields.');
                    return;
                }
                if (!isValidEmail(email)) {
                    showError('Please enter a valid campus email.');
                    return;
                }
                if (pass.length < 6) {
                    showError('Password must be at least 6 characters.');
                    return;
                }
                if (pass !== confirm) {
                    showError('Passwords do not match.');
                    return;
                }

                const success = await registerUser(name, email, cid, dept, role, pass);
                if (success) closeRegisterModal();
            });
        }

        // User Pill Dropdown & Logout
        const userPillBtn = document.getElementById('user-pill-btn');
        const userDropdown = document.getElementById('user-dropdown');
        const navLogoutBtn = document.getElementById('nav-logout-btn');

        if (userPillBtn && userDropdown) {
            userPillBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                userDropdown.classList.toggle('d-none');
            });
        }

        if (navLogoutBtn) {
            navLogoutBtn.addEventListener('click', () => {
                if (userDropdown) userDropdown.classList.add('d-none');
                logoutUser();
            });
        }

        // Notification Panel Dropdown
        const navNotifBtn = document.getElementById('nav-notif-btn');
        const notifPanel = document.getElementById('notif-panel');
        const markNotifsReadBtn = document.getElementById('mark-notifs-read-btn');

        if (navNotifBtn && notifPanel) {
            navNotifBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                notifPanel.classList.toggle('d-none');
            });
        }

        if (markNotifsReadBtn) {
            markNotifsReadBtn.addEventListener('click', () => {
                if (currentUser) {
                    notifications.forEach(n => {
                        if (n.userId === currentUser.id || n.userId === 'all') n.read = true;
                    });
                    saveNotifs();
                    renderNotifications();
                }
            });
        }

        // Close dropdowns on outside click
        document.addEventListener('click', function (e) {
            if (userDropdown && !userDropdown.contains(e.target) && (!userPillBtn || !userPillBtn.contains(e.target))) {
                userDropdown.classList.add('d-none');
            }
            if (notifPanel && !notifPanel.contains(e.target) && (!navNotifBtn || !navNotifBtn.contains(e.target))) {
                notifPanel.classList.add('d-none');
            }
        });

        // Profile Modal
        const dropProfileBtn = document.getElementById('dropdown-profile-btn');
        const closeProfileBtn = document.getElementById('close-profile-btn');
        const dismissProfileBtn = document.getElementById('dismiss-profile-btn');
        const profileForm = document.getElementById('profile-form');

        if (dropProfileBtn) {
            dropProfileBtn.addEventListener('click', () => {
                if (userDropdown) userDropdown.classList.add('d-none');
                openProfileModal();
            });
        }
        if (closeProfileBtn) closeProfileBtn.addEventListener('click', closeProfileModal);
        if (dismissProfileBtn) dismissProfileBtn.addEventListener('click', closeProfileModal);

        if (profileForm) {
            profileForm.addEventListener('submit', function (e) {
                e.preventDefault();
                if (!currentUser) return;

                currentUser.name = document.getElementById('profile-name').value.trim();
                currentUser.department = document.getElementById('profile-dept').value.trim();
                currentUser.phone = document.getElementById('profile-phone').value.trim();
                const studentIdEl = document.getElementById('profile-student-id');
                const contactPrefEl = document.getElementById('profile-contact-pref');
                const notifPrefEl = document.getElementById('profile-notif-pref');
                if (studentIdEl) currentUser.campusId = studentIdEl.value.trim();
                if (contactPrefEl) currentUser.contactPref = contactPrefEl.value;
                if (notifPrefEl) currentUser.notifPref = notifPrefEl.checked;

                const userIdx = users.findIndex(u => u.id === currentUser.id);
                if (userIdx !== -1) {
                    users[userIdx] = currentUser;
                    saveUsers();
                }
                localStorage.setItem(STORAGE_KEY_SESSION, JSON.stringify(currentUser));
                updateAuthUI();
                closeProfileModal();
                showSuccess('Profile updated successfully!');
            });
        }

        // My Activity View
        const navMyActivityLink = document.getElementById('nav-my-activity-link');
        const dropdownActivityBtn = document.getElementById('dropdown-activity-btn');
        const myActivitySection = document.getElementById('my-activity-section');
        const tabMyReports = document.getElementById('tab-btn-my-reports');
        const tabMyClaims = document.getElementById('tab-btn-my-claims');
        const panelMyReports = document.getElementById('panel-my-reports');
        const panelMyClaims = document.getElementById('panel-my-claims');

        function showMyActivitySection(e) {
            if (e && e.preventDefault) e.preventDefault();
            if (!currentUser) {
                openLoginModal();
                return;
            }
            if (myActivitySection) {
                myActivitySection.classList.remove('d-none');
                renderMyActivity();
                myActivitySection.scrollIntoView({ behavior: 'smooth' });
            }
        }

        if (navMyActivityLink) navMyActivityLink.addEventListener('click', showMyActivitySection);
        if (dropdownActivityBtn) {
            dropdownActivityBtn.addEventListener('click', (e) => {
                if (userDropdown) userDropdown.classList.add('d-none');
                showMyActivitySection(e);
            });
        }

        if (tabMyReports && tabMyClaims) {
            tabMyReports.addEventListener('click', () => {
                tabMyReports.classList.add('active');
                tabMyClaims.classList.remove('active');
                if (panelMyReports) panelMyReports.classList.remove('d-none');
                if (panelMyClaims) panelMyClaims.classList.add('d-none');
            });

            tabMyClaims.addEventListener('click', () => {
                tabMyClaims.classList.add('active');
                tabMyReports.classList.remove('active');
                if (panelMyClaims) panelMyClaims.classList.remove('d-none');
                if (panelMyReports) panelMyReports.classList.add('d-none');
            });
        }

        // Moderator Panel View
        const navModLink = document.getElementById('nav-moderator-link');
        const dropdownModBtn = document.getElementById('dropdown-mod-btn');
        const modSection = document.getElementById('moderator-section');

        function showModSection(e) {
            if (e && e.preventDefault) e.preventDefault();
            if (!currentUser || (currentUser.role !== 'moderator' && currentUser.role !== 'admin')) {
                showError('Access Denied: 403 Forbidden. Moderator authorization required.');
                return;
            }
            if (modSection) {
                modSection.classList.remove('d-none');
                renderModeratorPanel();
                modSection.scrollIntoView({ behavior: 'smooth' });
            }
        }

        if (navModLink) navModLink.addEventListener('click', showModSection);
        if (dropdownModBtn) {
            dropdownModBtn.addEventListener('click', (e) => {
                if (userDropdown) userDropdown.classList.add('d-none');
                showModSection(e);
            });
        }

        // Moderator Delegated Actions
        const modContainer = document.getElementById('mod-items-container');
        if (modContainer) {
            modContainer.addEventListener('click', function (e) {
                const flagBtn = e.target.closest('.btn-mod-flag');
                if (flagBtn) {
                    const itemId = flagBtn.getAttribute('data-id');
                    toggleFlagItem(itemId);
                    return;
                }

                const hideBtn = e.target.closest('.btn-mod-hide');
                if (hideBtn) {
                    const itemId = hideBtn.getAttribute('data-id');
                    toggleHideItem(itemId);
                    return;
                }
            });
        }

        // Admin Portal View
        const navAdminLink = document.getElementById('nav-admin-link');
        const dropdownAdminBtn = document.getElementById('dropdown-admin-btn');
        const adminSection = document.getElementById('admin-section');

        function showAdminSection(e) {
            if (e && e.preventDefault) e.preventDefault();
            if (!currentUser || currentUser.role !== 'admin') {
                showError('Access Denied: 403 Forbidden. Administrator clearance required.');
                return;
            }
            if (adminSection) {
                adminSection.classList.remove('d-none');
                renderAdminClaims();
                renderAdminUsers();
                renderAuditLogs();
                adminSection.scrollIntoView({ behavior: 'smooth' });
            }
        }

        if (navAdminLink) navAdminLink.addEventListener('click', showAdminSection);
        if (dropdownAdminBtn) {
            dropdownAdminBtn.addEventListener('click', (e) => {
                if (userDropdown) userDropdown.classList.add('d-none');
                showAdminSection(e);
            });
        }

        // Admin Tabs
        const tabAdminOverview = document.getElementById('tab-admin-overview');
        const tabAdminClaims = document.getElementById('tab-admin-claims');
        const tabAdminUsers = document.getElementById('tab-admin-users');
        const tabAdminCategories = document.getElementById('tab-admin-categories');
        const tabAdminLogs = document.getElementById('tab-admin-logs');

        const panelAdminOverview = document.getElementById('panel-admin-overview');
        const panelAdminClaims = document.getElementById('panel-admin-claims');
        const panelAdminUsers = document.getElementById('panel-admin-users');
        const panelAdminCategories = document.getElementById('panel-admin-categories');
        const panelAdminLogs = document.getElementById('panel-admin-logs');

        const adminTabs = [tabAdminOverview, tabAdminClaims, tabAdminUsers, tabAdminCategories, tabAdminLogs];
        const adminPanels = [panelAdminOverview, panelAdminClaims, panelAdminUsers, panelAdminCategories, panelAdminLogs];

        adminTabs.forEach((tab, idx) => {
            if (tab) {
                tab.addEventListener('click', () => {
                    adminTabs.forEach(t => t && t.classList.remove('active'));
                    adminPanels.forEach(p => p && p.classList.add('d-none'));

                    tab.classList.add('active');
                    if (adminPanels[idx]) adminPanels[idx].classList.remove('d-none');

                    if (idx === 1) renderAdminClaims();
                    if (idx === 2) renderAdminUsers();
                    if (idx === 3) renderCategorySelects();
                    if (idx === 4) renderAuditLogs();
                });
            }
        });

        // Admin Claims Table Actions (Approve / Reject)
        const adminClaimsTable = document.getElementById('admin-claims-table');
        if (adminClaimsTable) {
            adminClaimsTable.addEventListener('click', function (e) {
                const approveBtn = e.target.closest('.btn-approve-claim');
                if (approveBtn) {
                    const claimId = approveBtn.getAttribute('data-id');
                    approveClaim(claimId);
                    return;
                }

                const rejectBtn = e.target.closest('.btn-reject-claim');
                if (rejectBtn) {
                    const claimId = rejectBtn.getAttribute('data-id');
                    rejectClaim(claimId);
                    return;
                }
            });
        }

        // Admin User Table Actions (Change Role)
        const adminUsersTable = document.getElementById('admin-users-table');
        if (adminUsersTable) {
            adminUsersTable.addEventListener('click', function (e) {
                const roleBtn = e.target.closest('.btn-change-role');
                if (roleBtn) {
                    const userId = roleBtn.getAttribute('data-id');
                    changeUserRole(userId);
                }
            });
        }

        // Admin Category Add & Delete
        const addCatBtn = document.getElementById('add-category-btn');
        const newCatInput = document.getElementById('new-category-input');
        const adminCatList = document.getElementById('admin-category-list');

        if (addCatBtn && newCatInput) {
            addCatBtn.addEventListener('click', () => {
                addCategory(newCatInput.value);
                newCatInput.value = '';
            });
        }

        if (adminCatList) {
            adminCatList.addEventListener('click', function (e) {
                const removeBtn = e.target.closest('.btn-remove-cat');
                if (removeBtn) {
                    const catName = removeBtn.getAttribute('data-category');
                    removeCategory(catName);
                }
            });
        }

        // Image Gallery Modal Handlers
        const closeGalleryBtn = document.getElementById('close-gallery-btn');
        const dismissGalleryBtn = document.getElementById('dismiss-gallery-btn');
        const galleryModal = document.getElementById('gallery-modal');

        if (closeGalleryBtn) closeGalleryBtn.addEventListener('click', closeGalleryModal);
        if (dismissGalleryBtn) dismissGalleryBtn.addEventListener('click', closeGalleryModal);
        if (galleryModal) {
            galleryModal.addEventListener('click', function (e) {
                if (e.target === galleryModal) closeGalleryModal();
            });
        }

        // Keyboard navigation (ESC closes any active modal)
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                closeDeleteModal();
                closeDetailsModal();
                closeClaimModal();
                closeLoginModal();
                closeRegisterModal();
                closeProfileModal();
                closeGalleryModal();
            }
        });
    }

    /**
     * Application Initialization
     */
    function init() {
        initData();
        setupTabs();
        setupImageUploads();
        setupLostForm();
        setupFoundForm();
        setupEventListeners();
        renderCategorySelects();
        updateStatistics();
        updateAuthUI();
        renderCatalog();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Global testing API (Preserves all existing properties for Selenium test compatibility)
    window.FindItApp = {
        getItems: () => items,
        getUsers: () => users,
        getClaims: () => claims,
        getCategories: () => categories,
        getCurrentUser: () => currentUser,
        resetDemo: resetDemoData,
        markRecovered: markAsRecovered,
        login: loginUser,
        logout: logoutUser,
        register: registerUser,
        submitClaim: handleClaimSubmit,
        approveClaim: approveClaim,
        rejectClaim: rejectClaim,
        toggleFlag: toggleFlagItem,
        toggleHide: toggleHideItem,
        editItem: editItem,
        showAdmin: () => {
            const el = document.getElementById('admin-section');
            if (el) el.classList.remove('d-none');
            const nav = document.getElementById('nav-admin-link');
            if (nav) nav.click();
        },
        showMod: () => {
            const el = document.getElementById('moderator-section');
            if (el) el.classList.remove('d-none');
            const nav = document.getElementById('nav-moderator-link');
            if (nav) nav.click();
        }
    };
})();
