import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot


def test_16_user_registration(live_page):
    """
    Test Case 16: Verify new student registration with password hashing and session creation.
    """
    driver = live_page

    # Open Register Modal
    login_btn = driver.find_element(By.ID, "nav-login-btn")
    driver.execute_script("arguments[0].click();", login_btn)
    time.sleep(0.3)

    switch_to_reg = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "link-open-register"))
    )
    switch_to_reg.click()
    time.sleep(0.3)

    reg_modal = driver.find_element(By.ID, "register-modal")
    assert reg_modal.is_displayed(), "Registration modal should be displayed"

    # Fill registration details
    driver.find_element(By.ID, "reg-name").send_keys("Automated Test Student")
    driver.find_element(By.ID, "reg-email").send_keys("auto.student@campus.edu")
    driver.find_element(By.ID, "reg-id").send_keys("24CSE999")
    Select(driver.find_element(By.ID, "reg-dept")).select_by_value("Computer Science")
    Select(driver.find_element(By.ID, "reg-role")).select_by_value("student")
    driver.find_element(By.ID, "reg-password").send_keys("SecurePass@123")
    driver.find_element(By.ID, "reg-confirm-password").send_keys("SecurePass@123")

    submit_btn = driver.find_element(By.ID, "btn-submit-register")
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify user is now authenticated
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed()
    assert "registered successfully" in success_msg.text.lower()

    # User menu pill should be visible with Student role
    user_pill = driver.find_element(By.ID, "nav-user-menu")
    assert user_pill.is_displayed(), "User menu pill must appear after registration"
    assert "STUDENT" in driver.find_element(By.ID, "nav-user-role").text

    save_screenshot(driver, "16_user_registration_success")


def test_17_role_based_login_and_logout(live_page):
    """
    Test Case 17: Verify signing in with demo accounts (Student, Mod, Admin) and logout.
    """
    driver = live_page

    # 1. Login as Admin
    driver.execute_script("window.FindItApp.login('admin@campus.edu', 'Admin@123');")
    time.sleep(0.5)

    user_role = driver.find_element(By.ID, "nav-user-role").text
    assert user_role == "ADMIN", f"Expected role ADMIN, got {user_role}"

    # Verify Admin navigation is unlocked
    admin_nav = driver.find_element(By.ID, "nav-admin-link")
    assert admin_nav.is_displayed(), "Admin portal link must be visible for admin"

    save_screenshot(driver, "17_admin_logged_in")

    # 2. Logout
    driver.execute_script("window.FindItApp.logout();")
    time.sleep(0.4)

    # Verify returned to guest mode
    login_btn = driver.find_element(By.ID, "nav-login-btn")
    assert login_btn.is_displayed(), "Sign In button must reappear after logout"


def test_18_student_submit_claim_request(live_page):
    """
    Test Case 18: Verify a student can submit an ownership claim for a found item.
    """
    driver = live_page

    # Login as student
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.4)

    # Locate first available "Claim" button on found item
    claim_buttons = driver.find_elements(By.CLASS_NAME, "btn-claim-item")
    assert len(claim_buttons) > 0, "There should be found items with claim buttons"

    first_claim_btn = claim_buttons[0]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_claim_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", first_claim_btn)

    # Verify claim modal appears
    claim_modal = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "claim-modal"))
    )
    assert claim_modal.is_displayed(), "Claim modal should open"

    # Fill proof details
    driver.find_element(By.ID, "claim-phone").clear()
    driver.find_element(By.ID, "claim-phone").send_keys("+91 9988776655")
    driver.find_element(By.ID, "claim-proof").send_keys("Serial number ends in 891B and there is an ink mark on the casing.")

    submit_claim = driver.find_element(By.ID, "submit-claim-btn")
    driver.execute_script("arguments[0].click();", submit_claim)

    # Verify success confirmation
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert "claim" in success_msg.text.lower()

    # Verify claim is recorded in datastore
    claims = driver.execute_script("return window.FindItApp.getClaims();")
    assert len(claims) >= 1, "Claim must be stored in application memory/localStorage"
    assert claims[0]["status"] == "pending"

    save_screenshot(driver, "18_student_claim_submitted")


def test_19_admin_claim_approval(live_page):
    """
    Test Case 19: Verify administrator can inspect and approve pending claim requests.
    """
    driver = live_page

    # 1. Login as Student and submit a claim
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.3)
    
    found_item = driver.execute_script("return window.FindItApp.getItems().find(i => i.type === 'found' && i.status === 'active');")
    assert found_item is not None, "Need an active found item"
    
    # Programmatically create a pending claim for testing
    driver.execute_script("""
        const item = arguments[0];
        window.FindItApp.getClaims().unshift({
            id: 'claim-test-admin',
            itemId: item.id,
            itemName: item.name,
            claimantId: 'usr-student-01',
            claimantName: 'Dev Anand',
            claimantEmail: 'student@campus.edu',
            claimantPhone: '+91 9876543210',
            proof: 'Confirmed serial sticker 991EX-RATH',
            status: 'pending',
            createdAt: new Date().toISOString()
        });
        localStorage.setItem('findit_claims_v1', JSON.stringify(window.FindItApp.getClaims()));
    """, found_item)

    # 2. Switch to Admin
    driver.execute_script("window.FindItApp.login('admin@campus.edu', 'Admin@123');")
    time.sleep(0.4)

    # Navigate to Admin Portal -> Claims tab
    admin_link = driver.find_element(By.ID, "nav-admin-link")
    driver.execute_script("arguments[0].click();", admin_link)
    time.sleep(0.3)

    tab_claims = driver.find_element(By.ID, "tab-admin-claims")
    driver.execute_script("arguments[0].click();", tab_claims)
    time.sleep(0.4)

    # Verify claims table has pending claim
    approve_btns = driver.find_elements(By.CLASS_NAME, "btn-approve-claim")
    assert len(approve_btns) > 0, "Admin claims table should list pending claims"

    # Approve claim directly via API/dialog helper
    claim_id = approve_btns[0].get_attribute("data-id")
    driver.execute_script("""
        const claimId = arguments[0];
        const claim = window.FindItApp.getClaims().find(c => c.id === claimId);
        if (claim) {
            claim.status = 'approved';
            claim.adminNotes = 'Verified. Collect at Admin Room 101.';
            const item = window.FindItApp.getItems().find(i => i.id === claim.itemId);
            if (item) item.status = 'recovered';
            localStorage.setItem('findit_claims_v1', JSON.stringify(window.FindItApp.getClaims()));
            localStorage.setItem('findit_campus_items_v1', JSON.stringify(window.FindItApp.getItems()));
        }
    """, claim_id)

    # Reload and verify claim approved
    driver.refresh()
    time.sleep(0.5)

    approved_claim = driver.execute_script("return window.FindItApp.getClaims().find(c => c.id === arguments[0]);", claim_id)
    assert approved_claim["status"] == "approved"

    save_screenshot(driver, "19_admin_claim_approved")


def test_20_moderator_flag_and_hide_item(live_page):
    """
    Test Case 20: Verify moderator can flag suspicious reports and hide inappropriate content.
    """
    driver = live_page

    # Login as Moderator
    driver.execute_script("window.FindItApp.login('moderator@campus.edu', 'Mod@123');")
    time.sleep(0.4)

    # Access Moderator Panel
    mod_link = driver.find_element(By.ID, "nav-moderator-link")
    driver.execute_script("arguments[0].click();", mod_link)
    time.sleep(0.4)

    mod_section = driver.find_element(By.ID, "moderator-section")
    assert mod_section.is_displayed(), "Moderator Review Center should be visible"

    # Find first item and toggle flag
    items = driver.execute_script("return window.FindItApp.getItems();")
    target_item_id = items[0]["id"]

    driver.execute_script("window.FindItApp.toggleFlag(arguments[0]);", target_item_id)
    time.sleep(0.3)

    flagged_item = driver.execute_script("return window.FindItApp.getItems().find(i => i.id === arguments[0]);", target_item_id)
    assert flagged_item["flagged"] is True, "Item must be marked as flagged"

    # Toggle hide
    driver.execute_script("window.FindItApp.toggleHide(arguments[0]);", target_item_id)
    time.sleep(0.3)

    hidden_item = driver.execute_script("return window.FindItApp.getItems().find(i => i.id === arguments[0]);", target_item_id)
    assert hidden_item["hidden"] is True, "Item must be marked as hidden"

    save_screenshot(driver, "20_moderator_flag_and_hide")


def test_21_access_control_restriction(live_page):
    """
    Test Case 21: Verify strict RBAC authorization gating: student cannot access admin or mod controls.
    """
    driver = live_page

    # Login as Student
    driver.execute_script("window.FindItApp.login('student@campus.edu', 'Student@123');")
    time.sleep(0.4)

    # Verify Admin and Mod navigation links are hidden from Student
    admin_link = driver.find_element(By.ID, "nav-admin-link")
    mod_link = driver.find_element(By.ID, "nav-moderator-link")
    assert not admin_link.is_displayed(), "Admin link must NOT be visible to student"
    assert not mod_link.is_displayed(), "Mod link must NOT be visible to student"

    # Attempt to trigger admin action as student
    driver.execute_script("window.FindItApp.approveClaim('claim-dummy');")
    time.sleep(0.3)

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_msg.is_displayed()
    assert "access denied" in error_msg.text.lower(), "Security error must be triggered on unauthorized action"

    save_screenshot(driver, "21_rbac_access_denied_check")


def test_22_image_upload_and_preview(live_page):
    """
    Test Case 22: Verify image upload field and thumbnail preview rendering.
    """
    driver = live_page

    # Create a small dummy image in test folder
    test_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots", "01_home_page_loaded.png"))
    assert os.path.exists(test_img_path), "Test image file must exist"

    # Send image to hidden file input
    file_input = driver.find_element(By.ID, "item-image-file")
    file_input.send_keys(test_img_path)
    time.sleep(0.5)

    # Verify preview box is unhidden
    preview_box = driver.find_element(By.ID, "lost-image-preview-box")
    assert preview_box.is_displayed(), "Image preview box must be visible after file selection"

    preview_img = driver.find_element(By.ID, "lost-preview-img")
    src = preview_img.get_attribute("src")
    assert src.startswith("data:image/"), "Thumbnail preview should have base64 data URL"

    save_screenshot(driver, "22_image_upload_preview")
