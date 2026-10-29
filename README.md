# FindIt – Smart Lost & Found Management Portal
**Software Testing Lab Mini-Project (College Quality Assurance Demonstration)**  
*Engineered with Role-Based Access Control (RBAC), Flask Backend, SQLite Persistence, and Automated Selenium QA Testing*

---

## 📌 1. Project Overview

**FindIt** is a full-featured, responsive, role-based web application engineered to solve the real-world challenge of lost and misplaced personal belongings across a college campus (demonstrated with realistic data from the Rathinam campus community).

Unlike generic prototypes or static mockups, FindIt delivers:
1. **Interactive Role-Based Access Control (RBAC)** across three distinct campus roles: **Student / User**, **Moderator**, and **Administrator**.
2. **Genuine Image Uploads & Fullscreen Gallery Modal** with format validation (JPG/PNG/WEBP), client-side file-size guardrails (5 MB ceiling), and dynamic previews.
3. **Structured Item Reporting** with 10 standardized campus categories, secret identifying marks for ownership proof, contact channel preferences, and validation rejecting future dates.
4. **End-to-End Ownership Claim & Recovery Workflow** tracking lifecycle progression (`Lost` / `Found` ➔ `Claim Pending` ➔ `Claim Approved` / `Claim Rejected` ➔ `Recovered` ➔ `Closed`).
5. **In-App Notification Dispatcher** with unread count badges, notification drawers, and one-click mark-as-read controls.
6. **Enhanced Analytics Dashboard** computing live statistics, category distribution progress bars, status breakdown distributions, and personalized greeting headers.
7. **Multi-Attribute Filter & Search Engine** supporting combined queries, date filter, status filter, location filter, and sorting (Newest / Oldest).
8. **User Profile Management** with student register number, department, contact preferences, and role immutability.
9. **Dual Architecture Persistence**:
   - **Production Full-Stack Mode**: Python Flask REST API + SQLite database (`findit.db`) storing salted SHA-256 password hashes, foreign-key relational records, and uploaded images in `uploads/`.
   - **Standalone Client Fallback Mode**: Pure HTML5/ES6 `localStorage` mode allowing standalone presentation without external dependencies.
10. **Automated Software Quality Assurance**: Complete suite of **34 deterministic Selenium WebDriver + pytest test cases** verifying functionality, edge cases, input validation, and security access controls.

---

## 👥 2. Role-Based User System & Predefined Demo Accounts

FindIt implements strict role-based access control. Unauthenticated guests and students cannot access moderator or administrator panels, and client-side URL or DOM tampering is prohibited. Passwords are never stored in plaintext (using salted SHA-256 on client and PBKDF2 on Flask backend).

### Predefined Demo Accounts

| Role | Email Address | Password | Campus / Register ID | Department | Permitted Capabilities |
|---|---|---|---|---|---|
| **Student / User** | `student@campus.edu` | `Student@123` | `22BCS108` | Computer Science | Report lost/found items, upload photos, browse items, submit ownership claims, view personal reports/claims, mark own items recovered, receive in-app notifications. |
| **Moderator** | `moderator@campus.edu` | `Mod@123` | `FAC-SAFE-04` | Campus Safety & Discipline | Access Moderator Center, inspect newly filed campus reports, flag suspicious/vague submissions with notes, hide inappropriate content from public catalog, unhide/unflag. |
| **Administrator** | `admin@campus.edu` | `Admin@123` | `ADM-DIR-01` | Campus Administration | Access Admin Dashboard, review pending claims with identifying proof, approve/reject claims with pickup remarks, manage taxonomy categories, change user roles, inspect audit trail logs, delete reports. |

> [!TIP]
> **One-Click Role Switching**: When running in browser, the role indicator strip at the top includes quick shortcuts: **[Student]**, **[Moderator]**, **[Admin]** to facilitate rapid demonstration during lab examinations.

---

## 🛠️ 3. Technology Stack

| Layer | Technologies & Libraries |
|---|---|
| **Frontend UI & Layout** | Semantic HTML5, Vanilla CSS3 (Custom Design System, Glassmorphism, CSS Grid, Flexbox), Vanilla JavaScript (ES6+ async/await) |
| **Styling Tokens & Theme** | Modern purple-and-indigo palette (`--primary: #4f46e5`, `--accent: #8b5cf6`), Google Fonts (*Plus Jakarta Sans*, *Inter*), Inline SVG Icons |
| **Backend Web Server** | Python 3.10+, Flask 3.1+, Werkzeug WSGI server |
| **Database & Persistence** | SQLite 3 (`findit.db`) with foreign key constraints, HTML5 `localStorage` fallback |
| **Image Storage** | Dedicated `uploads/` directory with secure filename sanitation and 5MB validation |
| **Automated Testing** | pytest 9.1+, Selenium WebDriver 4.29+, Google Chrome Headless (`--headless=new`) |
| **Platform Target** | Windows 10/11, VS Code, Google Chrome |

---

## 📂 4. Project Directory Structure

```text
ST_Mini_Project/
├── app.py                          # Flask application entry point & static file server
├── findit.db                       # SQLite relational database (auto-created & seeded)
├── requirements.txt                # Python backend & testing dependencies
├── README.md                       # Comprehensive project documentation
├── backend/                        # Modular Flask backend architecture
│   ├── __init__.py                 # Backend package initializer
│   ├── database.py                 # SQLite schema, connections, and demo dataset seeding
│   ├── auth.py                     # Session tokens & role_required RBAC decorators
│   ├── routes_auth.py              # Endpoints: /api/auth/login, register, me, profile, users
│   ├── routes_items.py             # Endpoints: /api/items (CRUD, filter, sort, flag, hide, upload)
│   ├── routes_claims.py            # Endpoints: /api/claims (submit, approve, reject, history)
│   ├── routes_notifs.py            # Endpoints: /api/notifications (list, read, mark-all-read)
│   └── routes_stats.py             # Endpoints: /api/stats, /api/categories, /api/logs, /api/reset-demo
├── website/                        # Modern responsive web application
│   ├── index.html                  # Semantic UI structure with stable, deterministic test IDs
│   ├── style.css                   # Custom purple/white design system, animations, media queries
│   └── script.js                   # Application state engine, dual-mode API, and DOM controllers
├── tests/                          # Automated Selenium QA Test Suite
│   ├── conftest.py                 # Pytest fixtures: background server, Chrome WebDriver, screenshots
│   ├── test_findit_34_cases.py     # Complete suite of 34 required test cases (TC 01 to TC 34)
│   ├── test_dashboard.py           # Regression tests: Home, stats, title, responsiveness
│   ├── test_lost_item.py           # Regression tests: Lost item reporting & validation
│   ├── test_found_item.py          # Regression tests: Found item reporting
│   ├── test_search.py              # Regression tests: Search keywords & category filtering
│   ├── test_recovery.py            # Regression tests: Mark recovered & delete confirmation
│   └── test_role_based_system.py   # Regression tests: RBAC authentication & moderation
├── uploads/                        # Server directory for genuine image uploads
└── screenshots/                    # Generated PNG screenshots from Selenium test executions
```

---

## 🚀 5. Software Testing Lab Execution Guide (Windows & VS Code)

Follow this step-by-step guide designed for Windows 10/11 and Visual Studio Code to execute the automated tests and generate genuine lab terminal reports.

---

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Click **File > Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select the project folder:
   ```text
   C:\Users\devav\OneDrive - Rathinam Group Of Institutions\ST_Mini_Project
   ```
4. Verify that the file explorer in VS Code shows `app.py`, `run_tests.py`, `website/`, `backend/`, and `tests/`.

---

### Step 2: Install Python Dependencies
Open an integrated terminal in VS Code by pressing **`` Ctrl + ` ``** (or **Terminal > New Terminal**).

Ensure Python 3.10+ is active, then install all required packages:
- **PowerShell / Command Prompt**:
  ```powershell
  pip install -r requirements.txt
  ```
*Dependencies installed include*: `selenium`, `pytest`, `webdriver-manager`, `flask`, `werkzeug`, and `Pillow`.

---

### Step 3: Start the Existing FindIt Website
The FindIt portal is served by the Flask application on its discovered host and port:
- **Host**: `127.0.0.1`
- **Port**: `5000`
- **URL**: `http://127.0.0.1:5000`

In your VS Code terminal, start the server:
- **PowerShell / Command Prompt**:
  ```powershell
  python app.py
  ```
You will see confirmation in the console:
```text
============================================================
  FindIt – Smart Lost & Found Management Portal
  Serving at: http://127.0.0.1:5000
  Database:   SQLite (findit.db)
============================================================
 * Running on http://127.0.0.1:5000
```
Open your web browser and navigate to `http://127.0.0.1:5000` to confirm the website is active. **Leave this terminal running.**

---

### Step 4: Open a Second Terminal in the Project Folder
To keep the website server running while executing tests:
1. In the VS Code terminal pane, click the **`+`** icon (or press `Ctrl + Shift + \``) to open a second terminal tab.
2. Confirm the directory path is in the project folder:
   ```powershell
   cd "C:\Users\devav\OneDrive - Rathinam Group Of Institutions\ST_Mini_Project"
   ```

---

### Step 5: Execute All Selenium Tests
You can run the tests using either `pytest` directly or via the lab test runner.

#### Option A: Run 10 Core Lab Scenarios with Pytest
- **PowerShell / Command Prompt**:
  ```powershell
  pytest tests/test_lab_scenarios.py -v
  ```

#### Option B: Run the Full 34-Test Extended QA Matrix
- **PowerShell / Command Prompt**:
  ```powershell
  pytest tests/test_findit_34_cases.py -v
  ```

---

### Step 6: Generate the Formatted Terminal Report
Execute `run_tests.py` to trigger the automated test suite and produce the colored terminal output report matching the lab manual specification:
- **PowerShell / Command Prompt**:
  ```powershell
  python run_tests.py
  ```

#### Actual Terminal Execution Output:
```text
========== SELENIUM TEST EXECUTION ==========

[PASS] Website Navigation Test
[PASS] Search Functionality Test
[PASS] Button and Link Test
[PASS] Form Validation Test
[PASS] Item Reporting Test
[PASS] Image Upload Test
[PASS] Recovery Functionality Test
[PASS] Data Persistence Test
[PASS] Invalid Input Test
[PASS] Reset Demo Data Test

--------------------------------------------

Total Tests: 10
Passed: 10
Failed: 0
Success Rate: 100.0%

Test Report Generated Successfully.
```

---

### Step 7: Find the Saved Test Reports
In addition to the console display, `run_tests.py` automatically writes persistent reports to the `test_results/` folder:

1. **Machine-Readable JSON Report**:
   - Location: `test_results/test_report.json`
   - Contains: Execution timestamp, total tests, passed count, failed count, success rate, and per-test duration/status breakdown.
2. **Plaintext Lab Report**:
   - Location: `test_results/test_report.txt`
   - Formatted text report suitable for printing or pasting into lab experiment records.

---

### Step 8: Find the Screenshots
All screenshots captured during testing for your Software Testing Lab Record are stored in the `screenshots/` directory:

| Filename | Description | Captured By |
|---|---|---|
| `screenshots/homepage.png` | FindIt portal homepage, navbar, and statistics grid | `test_01_website_navigation` |
| `screenshots/search_results.png` | Live catalog search results for "Casio" calculator | `test_02_search_functionality` |
| `screenshots/report_form.png` | Active item incident reporting form with tab controls | `test_03_button_and_link` |
| `screenshots/form_validation.png` | Validation error banner and highlighted invalid fields | `test_04_form_validation` |
| `screenshots/recovery_status.png` | Item marked as Recovered with badge update and stats increment | `test_07_recovery_functionality` |
| `screenshots/selenium_test_execution.png` | Terminal test execution report output | `run_tests.py` |

> [!TIP]
> **Capturing Terminal Output with Windows Snipping Tool**:
> If you wish to capture your live interactive terminal window for your printed record:
> 1. Run `python run_tests.py` in your terminal.
> 2. Press **`Win + Shift + S`** on your Windows keyboard.
> 3. Select the terminal window showing the test results.
> 4. Save the file into `screenshots/selenium_test_execution.png`.

---

### Step 9: Troubleshooting Common Browser-Driver & Test Failures

| Issue / Error | Likely Cause | Solution / Fix |
|---|---|---|
| `NoSuchElementException: Unable to locate element: [id="..."]` | Outdated element ID or page not fully loaded | Ensure you run tests against the running portal (`http://127.0.0.1:5000`). All locators use the actual IDs from `website/index.html` (e.g. `#nav-items-link`, `#tab-btn-lost`, `#date-error`). |
| `WebDriverException: Chrome failed to start` | Google Chrome not installed or damaged binary | Verify Google Chrome is installed at `%ProgramFiles%\Google\Chrome\Application\chrome.exe`. Selenium 4+ automatically manages and downloads matching ChromeDriver binaries via Selenium Manager. |
| `ConnectionRefusedError: [WinError 10061]` | Website server (`app.py`) is not running on port 5000 | Start the server with `python app.py` before running tests. `tests/conftest.py` also provides a built-in quiet HTTP server fallback if port 5000 is not detected. |
| Future Date not rejected | Browser date input formatted in non-ISO locale | In Windows Chrome, `<input type="date">` inputs should be set using `driver.execute_script("arguments[0].value = 'YYYY-MM-DD';", el)` to prevent locale-specific parsing errors. |
| Inconsistent test data / State corruption | Previous test runs modified items | Reset the database to factory state by running: `python -c "from backend.database import reset_demo_db; reset_demo_db()"` or clicking the **Reset Demo Data** button in the website. |
| Terminal ANSI color codes not appearing | Older Windows console (legacy `cmd.exe`) | Run in **Visual Studio Code Integrated Terminal** or **Windows Terminal**. `run_tests.py` also executes `os.system("")` on startup to activate Windows virtual terminal processing. |

---

## 🧪 6. Detailed 10 Lab Test Scenarios (Lab Manual Mapping)

The 10 core automated test scenarios implemented in `tests/test_lab_scenarios.py` align with standard Quality Assurance lab experiments:

1. **TEST 1: Website Navigation Test** (`test_01_website_navigation`)
   - Verifies page loading, document title branding, navbar presence, hero section, statistics grid, and catalog visibility.
   - Captures `screenshots/homepage.png`.

2. **TEST 2: Search Functionality Test** (`test_02_search_functionality`)
   - Searches for an existing item ("Casio"), verifies matching card display.
   - Searches for a non-existent item ("XYZNonExistentCampusItem999"), verifies empty state container and message.
   - Captures `screenshots/search_results.png`.

3. **TEST 3: Button and Link Test** (`test_03_button_and_link`)
   - Clicks "Report Lost Item" and "Report Found Item" tab buttons, asserting active panels.
   - Verifies hero call-to-action buttons and navbar navigation anchor links (`#catalog-section`, `#report-section`, `#dashboard`).
   - Captures `screenshots/report_form.png`.

4. **TEST 4: Form Validation Test** (`test_04_form_validation`)
   - Triggers form submission without filling mandatory inputs.
   - Verifies submission prevention, display of global error alert banner, and application of `.is-invalid` CSS classes.
   - Captures `screenshots/form_validation.png`.

5. **TEST 5: Item Reporting Test** (`test_05_item_reporting`)
   - Fills all required fields for a lost laptop report and submits the form.
   - Verifies success banner confirmation and verifies that the new item card renders in the catalog with matching title, location, and category.

6. **TEST 6: Image Upload Test** (`test_06_image_upload`)
   - Uploads a valid test PNG image and verifies the thumbnail preview element renders with valid base64 image data.
   - Uploads an unsupported text document (`.txt`) and asserts rejection with a format validation message.

7. **TEST 7: Recovery Functionality Test** (`test_07_recovery_functionality`)
   - Reads the initial recovered count, clicks "Mark as Recovered" on an active item card.
   - Asserts the item status badge transitions to "Recovered" (`.badge-recovered`) and verifies the dashboard counter increments by 1.
   - Captures `screenshots/recovery_status.png`.

8. **TEST 8: Data Persistence Test** (`test_08_data_persistence`)
   - Creates a new lost property entry, executes a browser refresh (`driver.refresh()`).
   - Verifies that the item persists in the catalog after the reload.

9. **TEST 9: Invalid Input Test** (`test_09_invalid_input`)
   - Submits a date in the future (`2028-12-31`) and verifies rejection with `#date-error`.
   - Submits a malformed email address and verifies rejection with `#email-error`.

10. **TEST 10: Reset Demo Data Test** (`test_10_reset_demo_data`)
    - Clicks the "Reset Demo Data" control, verifies confirmation alert.
    - Asserts that dashboard counters return to factory baseline (4 Lost, 4 Found, 2 Recovered) and default catalog items are restored.

---

## 📋 7. Complete Test Case Summary Matrix (34 Test Cases)

The following table summarizes all 34 automated test cases implemented in `tests/test_findit_34_cases.py`:

| Test ID | Test Category | Description & Test Procedure | Expected Outcome | Status |
|---|---|---|---|---|
| **TC 01** | **Authentication** | Login with valid credentials (`student@campus.edu` / `Student@123`) | User pill badge displays "STUDENT", login modal closes, session active | **PASS** |
| **TC 02** | **Authentication** | Login with invalid credentials (`student@campus.edu` / `WrongPass`) | Error banner displayed, authentication rejected, guest mode retained | **PASS** |
| **TC 03** | **Authentication** | Submit empty login form (blank email & password) | Client validation prevents submission, displays required fields warning | **PASS** |
| **TC 04** | **Authentication** | Logout active student session | Active session terminated, login button restored in navbar, pills cleared | **PASS** |
| **TC 05** | **Authentication** | Unauthorized dashboard access attempt by unauthenticated guest | Admin and Moderator control panels remain hidden (`d-none`) | **PASS** |
| **TC 06** | **Authentication** | Role-based access restrictions for Student role | Admin/Moderator navigation links and administration panel remain hidden | **PASS** |
| **TC 07** | **Item Reporting** | Submit a valid lost-item report with category "Laptops" | Success banner appears, report appended to items collection | **PASS** |
| **TC 08** | **Item Reporting** | Submit a valid found-item report with category "ID Cards" | Item recorded with "Found Item" tag, stored with custodian info | **PASS** |
| **TC 09** | **Item Reporting** | Submit empty report form without mandatory inputs | Global error banner displayed, form submission blocked | **PASS** |
| **TC 10** | **Item Reporting** | Validate invalid email input (e.g. `not-a-valid-email`) | Input flagged with `.invalid` class, error alert prevents submission | **PASS** |
| **TC 11** | **Item Reporting** | Upload a valid image file (PNG/JPG format) | Genuine image preview rendered in `#lost-preview-img`, file name shown | **PASS** |
| **TC 12** | **Item Reporting** | Reject unsupported file type (e.g. `.txt` document) | Error banner rejects non-image format, file input cleared | **PASS** |
| **TC 13** | **Item Reporting** | Reject oversized image exceeding 5MB ceiling | Validation blocks upload, informs user of 5MB threshold | **PASS** |
| **TC 14** | **Item Reporting** | Verify newly created report appears in catalog immediately | Item card with unique title rendered in `#item-list` DOM | **PASS** |
| **TC 15** | **Search & Filter** | Search for an existing campus article ("Casio") | Catalog filters to matching calculator items, non-matching items hidden | **PASS** |
| **TC 16** | **Search & Filter** | Search for a non-existent item keyword | Zero item cards rendered, `#empty-state` container becomes visible | **PASS** |
| **TC 17** | **Search & Filter** | Filter items by category ("Laptops") | All displayed item cards belong strictly to "Laptops" taxonomy | **PASS** |
| **TC 18** | **Search & Filter** | Filter items by lifecycle status ("Recovered") | All displayed item cards display "Recovered" status badge | **PASS** |
| **TC 19** | **Search & Filter** | Combine multiple orthogonal filters (Category="Laptops" + Status="Lost") | Displayed cards satisfy both category and lost status simultaneously | **PASS** |
| **TC 20** | **Search & Filter** | Clear all active search & category filters | Search input cleared, selects reset to "all", full catalog restored | **PASS** |
| **TC 21** | **Claim Management** | Student submits claim request for found article with proof | Claim registered with `pending` status, success confirmation shown | **PASS** |
| **TC 22** | **Claim Management** | Reject empty claim request lacking proof of ownership | Modal validation requires proof description before submission | **PASS** |
| **TC 23** | **Claim Management** | Administrator approves pending claim with pickup instructions | Claim status updates to `approved`, audit log and item status updated | **PASS** |
| **TC 24** | **Claim Management** | Administrator rejects claim with explanation note | Claim status updates to `rejected`, claimant receives decision reason | **PASS** |
| **TC 25** | **Claim Management** | Unauthorized user (student) attempts to approve claims | Action denied with access restriction error alert | **PASS** |
| **TC 26** | **Claim Management** | Prevent submitting ownership claim on already recovered item | Business logic blocks claim with informative notice | **PASS** |
| **TC 27** | **Notifications** | Verify claimant receives in-app notification upon claim update | Notification badge displays unread count, notification added to tray | **PASS** |
| **TC 28** | **Notifications** | Mark in-app notification as read | Notification item drops `.unread` highlight styling | **PASS** |
| **TC 29** | **Notifications** | Verify unread notification count badge updates | `#notif-badge` element receives `d-none` when unread count reaches 0 | **PASS** |
| **TC 30** | **Data & Dashboard** | Verify dynamic calculation of dashboard metrics | Total Lost (4), Found (4), Recovered (2), Active (6) accurately match data | **PASS** |
| **TC 31** | **Data & Dashboard** | Verify reports persist after browser page refresh | Report remains present in catalog after full browser reload | **PASS** |
| **TC 32** | **Data & Dashboard** | Verify updates persist across application restart (SQLite DB) | Database connection restart proves durability in SQLite `findit.db` | **PASS** |
| **TC 33** | **Data & Dashboard** | Verify deleting a report immediately updates dashboard counts | Catalog item count decreases by 1, statistics decrement in real time | **PASS** |
| **TC 34** | **Data & Dashboard** | Verify users cannot edit or delete another user's report | Security check prohibits editing foreign items; returns Access Denied | **PASS** |

---

## 🗄️ 8. Database Architecture & Schema

When running with Flask (`python app.py`), FindIt utilizes SQLite (`findit.db`). The database schema is fully normalized with foreign key integrity:

```sql
-- Users Table
CREATE TABLE users (
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

-- Items Table
CREATE TABLE items (
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

-- Claims Table
CREATE TABLE claims (
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

-- In-App Notifications Table
CREATE TABLE notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    time TEXT NOT NULL,
    read INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

-- Audit Trail Logs Table
CREATE TABLE audit_logs (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    details TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### Resetting the Database to Factory Seed Data
To programmatically reset the database to clean Rathinam campus demo records at any time:
```powershell
python -c "from backend.database import reset_demo_db; reset_demo_db()"
```
Or click the **"Reset Demo Data"** button in the website footer.

---

## 📸 9. Screenshot Generation & Verification

The automated test runner captures genuine visual evidence for each major workflow. Screenshots are stored in the `screenshots/` directory:

- `01_home_page_loaded.png` – Home page layout and navbar
- `03_dashboard_statistics.png` – Initial metrics counter cards
- `04_successful_lost_item_report.png` – Lost item report submission confirmation
- `07_successful_found_item_report.png` – Found item report submission confirmation
- `08_search_existing_item.png` – Live search results
- `09_search_nonexistent_item.png` – Empty state view
- `10_filter_by_category.png` – Category filtered directory
- `11_mark_item_as_recovered.png` – Lifecycle state updated to Recovered
- `15_responsive_mobile_375x667.png` – Mobile responsive viewport check
- `15_responsive_tablet_768x1024.png` – Tablet responsive viewport check
- `15_responsive_desktop_1280x800.png` – Desktop responsive viewport check
- `16_user_registration_success.png` – Student self-service registration
- `17_admin_session_active.png` – Admin dashboard with management tables
- `18_student_claim_submitted.png` – Ownership claim submission
- `19_admin_claims_inspection.png` – Admin reviewing claim proof
- `20_moderator_panel_flagged.png` – Moderator Center flagged item notes
- `21_access_denied_guest.png` – Access control enforcement
- `22_image_upload_preview.png` – File upload preview display
- `tc01_login_valid_credentials.png` to `tc34_cannot_edit_another_users_report.png` – Dedicated test case screenshots

---

## 🔒 10. Security & Quality Assurance Features

1. **Role-Based Access Control (RBAC)**: Backend endpoint enforcement with `@role_required` decorators; frontend views dynamically hidden/shown based on cryptographically verifiable tokens or authenticated session state.
2. **Safe File Handling**: Uploaded files are checked against allowed extensions (`.jpg`, `.jpeg`, `.png`, `.webp`), sanitized with `secure_filename`, limited to 5 MB, and stored in `uploads/` rather than executable paths.
3. **Password Security**: Passwords hashed using PBKDF2 with SHA-256 (Flask) and salted SHA-256 (client); plain text passwords are never stored.
4. **Deterministic Testing Locators**: Every interactive element, modal, button, input, and badge contains stable HTML `id` attributes (e.g., `#nav-login-btn`, `#submit-claim-btn`, `#stats-total-lost`) ensuring flakiness-free automation in Selenium.

---

## 📝 11. Known Limitations

- **Email Dispatching**: In-app notifications are stored and displayed in the application UI tray. Actual SMTP campus email delivery requires configuring campus mail server credentials in `app.py`.
- **Browser Alert Popups**: In headless automated WebDriver runs, native JavaScript `window.prompt()` is bypassed in favor of clean in-page dialogs and automated testing API hooks to prevent `UnexpectedAlertPresentException`.
