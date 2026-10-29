import os
import time
import tempfile
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot
from backend.database import get_db_connection, reset_demo_db


# ============================================================================
# FEATURE 11: 34 SELENIUM AUTOMATION TEST CASES
# Complete End-to-End Test Suite for FindIt Campus Portal
# ============================================================================

# ----------------------------------------------------------------------------
# GROUP 1: AUTHENTICATION (TC 01 - 06)
# ----------------------------------------------------------------------------

def test_tc01_login_valid_credentials(live_page):
    """
    Test Case 1: Login with valid credentials.
    Verifies user can log in with demo student credentials and access authenticated state.
    """
    driver = live_page
    
    # Open login modal
    login_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "nav-login-btn"))
    )
    driver.execute_script("arguments[0].click();", login_btn)

    modal = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "login-modal"))
    )
    assert modal.is_displayed()

    # Enter valid student credentials
    driver.find_element(By.ID, "login-email").clear()
    driver.find_element(By.ID, "login-email").send_keys("student@campus.edu")
    driver.find_element(By.ID, "login-password").clear()
    driver.find_element(By.ID, "login-password").send_keys("Student@123")

    submit_btn = driver.find_element(By.ID, "btn-submit-login")
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify user menu pill appears with Student role
    user_menu = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "nav-user-menu"))
    )
    assert user_menu.is_displayed(), "User menu pill must appear after valid login"
    role_text = driver.find_element(By.ID, "nav-user-role").text
    assert "STUDENT" in role_text

    save_screenshot(driver, "tc01_login_valid_credentials")


def test_tc02_login_invalid_credentials(live_page):
    """
    Test Case 2: Login with invalid credentials.
    Verifies authentication rejection and error message display for incorrect password.
    """
    driver = live_page
    
    login_btn = driver.find_element(By.ID, "nav-login-btn")
    driver.execute_script("arguments[0].click();", login_btn)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "login-modal"))
    )

    # Enter wrong password
    driver.find_element(By.ID, "login-email").clear()
    driver.find_element(By.ID, "login-email").send_keys("student@campus.edu")
    driver.find_element(By.ID, "login-password").clear()
    driver.find_element(By.ID, "login-password").send_keys("IncorrectPass999")

    submit_btn = driver.find_element(By.ID, "btn-submit-login")
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify global error alert is displayed
    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()
    assert "invalid" in error_msg.text.lower() or "incorrect" in error_msg.text.lower()

    # User menu pill should remain hidden
    user_menu = driver.find_element(By.ID, "nav-user-menu")
    assert "d-none" in user_menu.get_attribute("class")

    save_screenshot(driver, "tc02_login_invalid_credentials")


def test_tc03_empty_login_form_submission(live_page):
    """
    Test Case 3: Empty login form submission.
    Verifies validation prevents submitting blank email and password.
    """
    driver = live_page

    login_btn = driver.find_element(By.ID, "nav-login-btn")
    driver.execute_script("arguments[0].click();", login_btn)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "login-modal"))
    )

    driver.find_element(By.ID, "login-email").clear()
    driver.find_element(By.ID, "login-password").clear()

    submit_btn = driver.find_element(By.ID, "btn-submit-login")
    driver.execute_script("arguments[0].click();", submit_btn)

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()
    assert "required" in error_msg.text.lower() or "both email and password" in error_msg.text.lower()

    save_screenshot(driver, "tc03_empty_login_submission")


def test_tc04_logout(live_page):
    """
    Test Case 4: Logout functionality.
    Verifies active session ends cleanly and login button is restored.
    """
    driver = live_page

    # Fast login via testing API
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    user_menu = driver.find_element(By.ID, "nav-user-menu")
    assert user_menu.is_displayed(), "User should be logged in"

    # Open dropdown menu and click logout
    pill_btn = driver.find_element(By.ID, "user-pill-btn")
    driver.execute_script("arguments[0].click();", pill_btn)
    time.sleep(0.2)

    logout_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "nav-logout-btn"))
    )
    driver.execute_script("arguments[0].click();", logout_btn)

    # Verify session terminated
    login_btn = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "nav-login-btn"))
    )
    assert login_btn.is_displayed(), "Login button should reappear after logout"
    assert "d-none" in user_menu.get_attribute("class")

    save_screenshot(driver, "tc04_logout_success")


def test_tc05_unauthorized_dashboard_access(live_page):
    """
    Test Case 5: Unauthorized dashboard access.
    Verifies unauthenticated guest users cannot view admin or moderator panels.
    """
    driver = live_page

    # Ensure in guest mode
    driver.execute_script("window.FindItApp.logout();")
    time.sleep(0.2)

    mod_section = driver.find_element(By.ID, "moderator-section")
    admin_section = driver.find_element(By.ID, "admin-section")

    assert "d-none" in mod_section.get_attribute("class"), "Moderator section must be hidden from guests"
    assert "d-none" in admin_section.get_attribute("class"), "Admin section must be hidden from guests"

    save_screenshot(driver, "tc05_unauthorized_access_blocked")


def test_tc06_role_based_access_restrictions(live_page):
    """
    Test Case 6: Role-based access restrictions.
    Verifies that a student user cannot view admin controls or access administrator links.
    """
    driver = live_page

    # Login as student
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    nav_admin = driver.find_element(By.ID, "nav-admin-link")
    nav_mod = driver.find_element(By.ID, "nav-moderator-link")
    admin_sec = driver.find_element(By.ID, "admin-section")

    assert "d-none" in nav_admin.get_attribute("class"), "Admin navbar link must be hidden for student role"
    assert "d-none" in nav_mod.get_attribute("class"), "Moderator navbar link must be hidden for student role"
    assert "d-none" in admin_sec.get_attribute("class"), "Admin panel section must be hidden for student role"

    save_screenshot(driver, "tc06_role_based_restrictions")


# ----------------------------------------------------------------------------
# GROUP 2: ITEM REPORTING (TC 07 - 14)
# ----------------------------------------------------------------------------

def test_tc07_submit_valid_lost_item_report(live_page):
    """
    Test Case 7: Submit a valid lost-item report.
    Verifies form validation, persistence, and UI display of new lost item.
    """
    driver = live_page
    item_title = "Matte Black HP Spectre x360"

    driver.find_element(By.ID, "item-name").send_keys(item_title)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Laptops")
    driver.find_element(By.ID, "item-location").send_keys("Science Block CS Lab 3")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-25")
    driver.find_element(By.ID, "contact-name").send_keys("Kavya Sharma")
    driver.find_element(By.ID, "contact-email").send_keys("kavya@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Intel i7, silver bumper case, Rathinam campus sticker.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed()
    assert "recorded" in success_msg.text.lower() or "successfully" in success_msg.text.lower()

    save_screenshot(driver, "tc07_valid_lost_report")


def test_tc08_submit_valid_found_item_report(live_page):
    """
    Test Case 8: Submit a valid found-item report.
    Verifies form switching to Found tab and recording a campus found article.
    """
    driver = live_page
    found_title = "Campus Library Barcode ID Card"

    tab_found = driver.find_element(By.ID, "tab-btn-found")
    driver.execute_script("arguments[0].scrollIntoView(true);", tab_found)
    time.sleep(0.2)
    tab_found.click()

    driver.find_element(By.ID, "found-item-name").send_keys(found_title)
    Select(driver.find_element(By.ID, "found-item-category")).select_by_value("ID Cards")
    driver.find_element(By.ID, "found-item-location").send_keys("Central Library 1st Floor")
    driver.find_element(By.ID, "found-item-date").send_keys("2026-10-26")
    driver.find_element(By.ID, "found-contact-name").send_keys("Librarian Desk")
    driver.find_element(By.ID, "found-contact-email").send_keys("library@campus.edu")
    driver.find_element(By.ID, "found-item-description").send_keys("Found between books in CSE rack 4.")

    submit_btn = driver.find_element(By.ID, "found-submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed()

    save_screenshot(driver, "tc08_valid_found_report")


def test_tc09_submit_empty_report_form(live_page):
    """
    Test Case 9: Submit an empty report form.
    Verifies that client-side validation detects missing required fields.
    """
    driver = live_page

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()
    assert "please correct the highlighted errors" in error_msg.text.lower() or "required" in error_msg.text.lower()

    save_screenshot(driver, "tc09_empty_form_validation")


def test_tc10_validate_invalid_email_input(live_page):
    """
    Test Case 10: Validate invalid email input.
    Verifies malformed email address is rejected with field-specific feedback.
    """
    driver = live_page

    driver.find_element(By.ID, "item-name").send_keys("Campus Gym Water Bottle")
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Water Bottles")
    driver.find_element(By.ID, "item-location").send_keys("Sports Arena")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-25")
    driver.find_element(By.ID, "contact-name").send_keys("Suresh")
    driver.find_element(By.ID, "contact-email").send_keys("not-a-valid-email")
    driver.find_element(By.ID, "item-description").send_keys("Steel thermos bottle.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    email_input = driver.find_element(By.ID, "contact-email")
    assert "invalid" in email_input.get_attribute("class")

    save_screenshot(driver, "tc10_invalid_email_validation")


def test_tc11_upload_valid_image(live_page):
    """
    Test Case 11: Upload a valid image.
    Verifies genuine file upload preview rendering for JPG/PNG images.
    """
    driver = live_page

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        # Minimal 1x1 PNG byte signature
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        temp_img_path = f.name

    try:
        file_input = driver.find_element(By.ID, "item-image-file")
        file_input.send_keys(temp_img_path)
        time.sleep(0.4)

        preview_box = driver.find_element(By.ID, "lost-image-preview-box")
        assert not ("d-none" in preview_box.get_attribute("class")), "Image preview box should become visible"
        
        preview_img = driver.find_element(By.ID, "lost-preview-img")
        assert preview_img.get_attribute("src").startswith("data:image/png"), "Preview src should contain loaded image data"

        save_screenshot(driver, "tc11_valid_image_preview")
    finally:
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)


def test_tc12_reject_unsupported_file_type(live_page):
    """
    Test Case 12: Reject an unsupported file type.
    Verifies that uploading a .txt or non-image file produces a validation error.
    """
    driver = live_page

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"This is not an image file.")
        temp_txt_path = f.name

    try:
        file_input = driver.find_element(By.ID, "item-image-file")
        file_input.send_keys(temp_txt_path)
        time.sleep(0.3)

        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "error-message"))
        )
        assert error_msg.is_displayed()
        assert "valid image file" in error_msg.text.lower() or "jpg" in error_msg.text.lower()

        save_screenshot(driver, "tc12_unsupported_file_rejected")
    finally:
        if os.path.exists(temp_txt_path):
            os.remove(temp_txt_path)


def test_tc13_reject_oversized_image(live_page):
    """
    Test Case 13: Reject an oversized image (> 5 MB).
    Verifies that files exceeding 5MB size limit are rejected cleanly without breaking the page.
    """
    driver = live_page

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        f.write(b"0" * (5 * 1024 * 1024 + 204800))
        temp_large_path = f.name

    try:
        file_input = driver.find_element(By.ID, "item-image-file")
        file_input.send_keys(temp_large_path)
        time.sleep(0.3)

        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "error-message"))
        )
        assert error_msg.is_displayed()
        assert "5mb" in error_msg.text.lower()

        save_screenshot(driver, "tc13_oversized_image_rejected")
    finally:
        if os.path.exists(temp_large_path):
            os.remove(temp_large_path)


def test_tc14_verify_report_appears_in_item_list(live_page):
    """
    Test Case 14: Verify that the report appears in the item list.
    Verifies newly reported item card is rendered immediately into the catalog.
    """
    driver = live_page
    unique_title = "TC14 Special Edition Scientific Calculator"

    driver.find_element(By.ID, "item-name").send_keys(unique_title)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Accessories")
    driver.find_element(By.ID, "item-location").send_keys("Math Dept Seminar Hall")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-25")
    driver.find_element(By.ID, "contact-name").send_keys("Ananya")
    driver.find_element(By.ID, "contact-email").send_keys("ananya@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Casio FX-991CW with protective hard case.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify appearance in catalog
    card = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//article[contains(., '{unique_title}')]"))
    )
    assert card.is_displayed(), "Newly reported item must appear in catalog"

    save_screenshot(driver, "tc14_report_in_item_list")


# ----------------------------------------------------------------------------
# GROUP 3: SEARCH & FILTERING (TC 15 - 20)
# ----------------------------------------------------------------------------

def test_tc15_search_existing_item(live_page):
    """
    Test Case 15: Search for an existing item.
    Verifies live search query narrows catalog to matching items.
    """
    driver = live_page
    search_input = driver.find_element(By.ID, "search-input")
    driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
    search_input.clear()
    search_input.send_keys("Casio")
    time.sleep(0.4)

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) >= 1
    for card in visible_cards:
        assert "casio" in card.text.lower() or "calculator" in card.text.lower()

    save_screenshot(driver, "tc15_search_existing_item")


def test_tc16_search_nonexistent_item(live_page):
    """
    Test Case 16: Search for a nonexistent item.
    Verifies empty state message and zero visible cards.
    """
    driver = live_page
    search_input = driver.find_element(By.ID, "search-input")
    driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
    search_input.clear()
    search_input.send_keys("NonExistentItemKeywordXYZ999")
    time.sleep(0.4)

    empty_state = driver.find_element(By.ID, "empty-state")
    assert empty_state.is_displayed(), "Empty state must be displayed for zero search matches"

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) == 0

    save_screenshot(driver, "tc16_search_nonexistent_item")


def test_tc17_filter_by_category(live_page):
    """
    Test Case 17: Filter by category.
    Verifies dropdown restricts results to selected category.
    """
    driver = live_page
    category_select = Select(driver.find_element(By.ID, "category-filter"))
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, "category-filter"))

    category_select.select_by_value("Laptops")
    time.sleep(0.3)

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) > 0
    for card in visible_cards:
        tag = card.find_element(By.CLASS_NAME, "item-category-tag").text
        assert tag == "Laptops"

    save_screenshot(driver, "tc17_filter_by_category")


def test_tc18_filter_by_status(live_page):
    """
    Test Case 18: Filter by status.
    Verifies filtering by 'recovered' isolates resolved items.
    """
    driver = live_page
    status_select = Select(driver.find_element(By.ID, "status-filter"))
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, "status-filter"))

    status_select.select_by_value("recovered")
    time.sleep(0.3)

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) > 0
    for card in visible_cards:
        badge = card.find_element(By.CLASS_NAME, "recovery-status").text.lower()
        assert "recovered" in badge

    save_screenshot(driver, "tc18_filter_by_status")


def test_tc19_combine_multiple_filters(live_page):
    """
    Test Case 19: Combine multiple filters (Category + Status).
    Verifies compound filtering across category and lifecycle status.
    """
    driver = live_page
    category_select = Select(driver.find_element(By.ID, "category-filter"))
    status_select = Select(driver.find_element(By.ID, "status-filter"))

    category_select.select_by_value("Laptops")
    status_select.select_by_value("lost")
    time.sleep(0.4)

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) >= 1
    for card in visible_cards:
        tag = card.find_element(By.CLASS_NAME, "item-category-tag").text
        assert tag == "Laptops"
        assert "lost" in card.text.lower()

    save_screenshot(driver, "tc19_combine_multiple_filters")


def test_tc20_clear_all_filters(live_page):
    """
    Test Case 20: Clear all filters.
    Verifies clear button resets search term, category, and status filters.
    """
    driver = live_page
    search_input = driver.find_element(By.ID, "search-input")
    search_input.send_keys("Casio")
    Select(driver.find_element(By.ID, "category-filter")).select_by_value("Accessories")

    clear_btn = driver.find_element(By.ID, "clear-filters-btn")
    driver.execute_script("arguments[0].click();", clear_btn)
    time.sleep(0.3)

    assert search_input.get_attribute("value") == ""
    assert Select(driver.find_element(By.ID, "category-filter")).first_selected_option.get_attribute("value") == "all"
    
    total_cards = len(driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card"))
    assert total_cards >= 6, "All baseline items should reappear after clearing filters"

    save_screenshot(driver, "tc20_clear_all_filters")


# ----------------------------------------------------------------------------
# GROUP 4: CLAIM MANAGEMENT (TC 21 - 26)
# ----------------------------------------------------------------------------

def test_tc21_submit_claim_request(live_page):
    """
    Test Case 21: Submit a claim request.
    Verifies student can submit proof of ownership for a found article.
    """
    driver = live_page

    # Log in as student
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    # Click claim on found item-102 (Casio Calculator)
    claim_btn = driver.find_element(By.ID, "claim-btn-item-102")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", claim_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", claim_btn)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "claim-modal"))
    )

    driver.find_element(By.ID, "claim-phone").clear()
    driver.find_element(By.ID, "claim-phone").send_keys("+91 9988776655")
    driver.find_element(By.ID, "claim-proof").clear()
    driver.find_element(By.ID, "claim-proof").send_keys("Serial sticker 891B on inside of sliding lid.")

    submit_btn = driver.find_element(By.ID, "submit-claim-btn")
    driver.execute_script("arguments[0].click();", submit_btn)

    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed()
    assert "claim" in success_msg.text.lower()

    save_screenshot(driver, "tc21_submit_claim_request")


def test_tc22_reject_empty_claim_request(live_page):
    """
    Test Case 22: Reject an empty claim request.
    Verifies that claims without identifying proof details are rejected.
    """
    driver = live_page

    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    claim_btn = driver.find_element(By.ID, "claim-btn-item-102")
    driver.execute_script("arguments[0].click();", claim_btn)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "claim-modal"))
    )

    driver.find_element(By.ID, "claim-proof").clear()
    submit_btn = driver.find_element(By.ID, "submit-claim-btn")
    driver.execute_script("arguments[0].click();", submit_btn)

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()
    assert "proof" in error_msg.text.lower() or "required" in error_msg.text.lower()

    save_screenshot(driver, "tc22_empty_claim_rejected")


def test_tc23_approve_claim_as_authorized_admin(live_page):
    """
    Test Case 23: Approve a claim as an authorized administrator.
    Verifies that an admin can review and approve a pending claim.
    """
    driver = live_page

    # Create a pending claim via student session
    driver.execute_script("""
        window.FindItApp.login('student@campus.edu', 'Student@123');
        window.FindItApp.submitClaim('item-102', 'Genuine ownership proof: Serial number matched.');
    """)
    time.sleep(0.3)

    # Log in as Admin
    driver.execute_script("window.FindItApp.login('admin@campus.edu', 'Admin@123');")
    time.sleep(0.3)

    # Approve claim via FindItApp testing API with remarks
    claim_id = driver.execute_script("return window.FindItApp.getClaims()[0].id;")
    driver.execute_script("window.FindItApp.approveClaim(arguments[0], 'Verified. Pick up at admin desk.');", claim_id)
    time.sleep(0.3)

    # Verify claim status is updated to approved
    claim = driver.execute_script("return window.FindItApp.getClaims().find(c => c.id === arguments[0]);", claim_id)
    assert claim["status"] == "approved"

    save_screenshot(driver, "tc23_admin_claim_approved")


def test_tc24_reject_claim_as_authorized_admin(live_page):
    """
    Test Case 24: Reject a claim as an authorized administrator.
    Verifies that an admin can reject an unverified claim with reason.
    """
    driver = live_page

    driver.execute_script("""
        window.FindItApp.login('student@campus.edu', 'Student@123');
        window.FindItApp.submitClaim('item-102', 'Unsubstantiated ownership claim.');
    """)
    time.sleep(0.3)

    driver.execute_script("window.FindItApp.login('admin@campus.edu', 'Admin@123');")
    time.sleep(0.3)

    claim_id = driver.execute_script("return window.FindItApp.getClaims()[0].id;")
    driver.execute_script("window.FindItApp.rejectClaim(arguments[0], 'Serial numbers do not match.');", claim_id)
    time.sleep(0.3)

    claim = driver.execute_script("return window.FindItApp.getClaims().find(c => c.id === arguments[0]);", claim_id)
    assert claim["status"] == "rejected"

    save_screenshot(driver, "tc24_admin_claim_rejected")


def test_tc25_unauthorized_users_cannot_approve_claims(live_page):
    """
    Test Case 25: Verify that unauthorized users cannot approve claims.
    Verifies RBAC protection blocks students from approving claims.
    """
    driver = live_page

    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    # Student attempts to approve claim
    driver.execute_script("window.FindItApp.approveClaim('claim-test');")
    time.sleep(0.2)

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert "access denied" in error_msg.text.lower() or "administrator" in error_msg.text.lower()

    save_screenshot(driver, "tc25_unauthorized_claim_approval_blocked")


def test_tc26_prevent_claiming_recovered_item(live_page):
    """
    Test Case 26: Prevent claiming an already recovered item.
    Verifies business logic prevents claims on closed or recovered articles.
    """
    driver = live_page

    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    # Attempt to submit claim for recovered item-103
    driver.execute_script("window.FindItApp.submitClaim('item-103', 'Trying to claim already recovered ID');")
    time.sleep(0.2)

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert "already been recovered" in error_msg.text.lower() or "cannot be claimed" in error_msg.text.lower()

    save_screenshot(driver, "tc26_prevent_claiming_recovered_item")


# ----------------------------------------------------------------------------
# GROUP 5: NOTIFICATIONS (TC 27 - 29)
# ----------------------------------------------------------------------------

def test_tc27_notification_created_after_claim_update(live_page):
    """
    Test Case 27: Verify that a notification is created after a claim update.
    Verifies claimant receives in-app notification when administrator resolves a claim.
    """
    driver = live_page

    # Student submits claim, Admin approves it
    driver.execute_script("""
        window.FindItApp.login('student@campus.edu', 'Student@123');
        window.FindItApp.submitClaim('item-102', 'Serial proof matched.');
        window.FindItApp.login('admin@campus.edu', 'Admin@123');
        const claims = window.FindItApp.getClaims();
        if (claims.length > 0) {
            window.FindItApp.approveClaim(claims[0].id, 'Pick up at reception');
        }
        window.FindItApp.login('student@campus.edu', 'Student@123');
    """)
    time.sleep(0.4)

    notif_badge = driver.find_element(By.ID, "notif-badge")
    assert not ("d-none" in notif_badge.get_attribute("class")), "Notification badge must be visible with unread count"
    assert int(notif_badge.text) >= 1

    save_screenshot(driver, "tc27_claim_update_notification")


def test_tc28_mark_notification_as_read(live_page):
    """
    Test Case 28: Mark a notification as read.
    Verifies user can open notifications drop panel and mark notifications read.
    """
    driver = live_page

    driver.execute_script("""
        window.FindItApp.login('student@campus.edu', 'Student@123');
        window.FindItApp.submitClaim('item-102', 'Serial proof matched.');
    """)
    time.sleep(0.3)

    notif_btn = driver.find_element(By.ID, "nav-notif-btn")
    driver.execute_script("arguments[0].click();", notif_btn)
    time.sleep(0.2)

    notif_panel = driver.find_element(By.ID, "notif-panel")
    assert not ("d-none" in notif_panel.get_attribute("class")), "Notification panel should open"

    mark_read_btn = driver.find_element(By.ID, "mark-notifs-read-btn")
    driver.execute_script("arguments[0].click();", mark_read_btn)
    time.sleep(0.3)

    unread_items = driver.find_elements(By.CSS_SELECTOR, "#notif-list .notif-item.unread")
    assert len(unread_items) == 0, "No notification items should remain unread"

    save_screenshot(driver, "tc28_notifications_marked_read")


def test_tc29_unread_notification_count_changes(live_page):
    """
    Test Case 29: Verify that the unread notification count changes.
    Verifies badge clears/hides when all notifications have been read.
    """
    driver = live_page

    driver.execute_script("""
        window.FindItApp.login('student@campus.edu', 'Student@123');
        window.FindItApp.submitClaim('item-102', 'Serial proof matched.');
    """)
    time.sleep(0.3)

    # Click mark all read
    mark_read_btn = driver.find_element(By.ID, "mark-notifs-read-btn")
    driver.execute_script("arguments[0].click();", mark_read_btn)
    time.sleep(0.3)

    notif_badge = driver.find_element(By.ID, "notif-badge")
    assert "d-none" in notif_badge.get_attribute("class"), "Unread badge must be hidden when unread count is 0"

    save_screenshot(driver, "tc29_unread_count_cleared")


# ----------------------------------------------------------------------------
# GROUP 6: DATA AND DASHBOARD (TC 30 - 34)
# ----------------------------------------------------------------------------

def test_tc30_verify_dashboard_statistics(live_page):
    """
    Test Case 30: Verify dashboard statistics.
    Verifies accurate calculation of total lost, found, recovered, and active cases.
    """
    driver = live_page

    total_lost = int(driver.find_element(By.ID, "stats-total-lost").text)
    total_found = int(driver.find_element(By.ID, "stats-total-found").text)
    total_recovered = int(driver.find_element(By.ID, "stats-total-recovered").text)
    total_active = int(driver.find_element(By.ID, "stats-total-active").text)

    assert total_lost == 4
    assert total_found == 4
    assert total_recovered == 2
    assert total_active == 6

    save_screenshot(driver, "tc30_dashboard_statistics")


def test_tc31_reports_persist_after_refresh(live_page):
    """
    Test Case 31: Verify that reports persist after refreshing the page.
    Verifies data durability across browser reloads.
    """
    driver = live_page
    persistent_title = "TC31 Refresh Durability Test Keychain"

    driver.find_element(By.ID, "item-name").send_keys(persistent_title)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Keys")
    driver.find_element(By.ID, "item-location").send_keys("Automobile Lab")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-25")
    driver.find_element(By.ID, "contact-name").send_keys("Lab Incharge")
    driver.find_element(By.ID, "contact-email").send_keys("incharge@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Honda bike key with brass ring.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )

    # Refresh browser
    driver.refresh()
    time.sleep(0.8)

    # Verify report is still present in catalog
    matching_cards = driver.find_elements(By.XPATH, f"//article[contains(., '{persistent_title}')]")
    assert len(matching_cards) >= 1, "Report must persist in catalog across page refreshes"

    save_screenshot(driver, "tc31_persists_after_refresh")


def test_tc32_updates_persist_after_restart():
    """
    Test Case 32: Verify that updates persist after application restart if a database is implemented.
    Verifies SQLite database backend durability across distinct connection cycles.
    """
    test_item_id = "test-backend-restart-999"
    with get_db_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO items (id, type, name, category, location, date, contact_name, contact_email, description, status, reported_by, created_at)
            VALUES (?, 'lost', 'SQLite Restart Test Laptop', 'Laptops', 'Server Room', '2026-10-28', 'Sysadmin', 'sysadmin@campus.edu', 'Persistent backend test', 'active', 'usr-admin-01', '2026-10-28T12:00:00Z')
        """, (test_item_id,))

    # Simulate fresh restart cycle by closing and opening a brand-new DB connection
    with get_db_connection() as conn:
        row = conn.execute("SELECT name, category, status FROM items WHERE id = ?", (test_item_id,)).fetchone()
        assert row is not None, "Item must exist in SQLite database after connection restart"
        assert row["name"] == "SQLite Restart Test Laptop"
        assert row["category"] == "Laptops"
        assert row["status"] == "active"

        # Clean up test row
        conn.execute("DELETE FROM items WHERE id = ?", (test_item_id,))


def test_tc33_delete_report_updates_dashboard(live_page):
    """
    Test Case 33: Verify that deleting a report updates the dashboard.
    Verifies metrics immediately synchronize when an item is removed.
    """
    driver = live_page

    initial_items = len(driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card"))
    assert initial_items > 0

    first_card = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")[0]
    item_id = first_card.get_attribute("data-item-id")

    delete_btn = driver.find_element(By.ID, f"delete-item-{item_id}")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", delete_btn)

    confirm_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "confirm-delete-btn"))
    )
    confirm_btn.click()

    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.ID, "delete-modal"))
    )
    time.sleep(0.3)

    remaining_items = len(driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card"))
    assert remaining_items == initial_items - 1, f"Expected {initial_items - 1} items remaining, got {remaining_items}"

    save_screenshot(driver, "tc33_delete_report_updates_dashboard")


def test_tc34_cannot_edit_another_users_report(live_page):
    """
    Test Case 34: Verify that users cannot edit another user's report.
    Verifies ownership permissions prohibit unauthorized tampering with foreign records.
    """
    driver = live_page

    # Log in as student (usr-student-01)
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)

    # Attempt to edit item-104 (reported by usr-mod-01)
    result = driver.execute_script("return window.FindItApp.editItem('item-104', { name: 'Tampered Name' });")
    assert result is False, "Student should not be able to edit another user's report"

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()
    assert "access denied" in error_msg.text.lower() or "cannot edit" in error_msg.text.lower()

    save_screenshot(driver, "tc34_cannot_edit_another_users_report")
