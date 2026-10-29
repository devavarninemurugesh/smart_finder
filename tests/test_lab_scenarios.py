import os
import time
import tempfile
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot, SCREENSHOTS_DIR


# ============================================================================
# SOFTWARE TESTING LAB: 10 CORE AUTOMATED TEST SCENARIOS
# FindIt – Smart Lost & Found Management Portal
# ============================================================================

def test_01_website_navigation(live_page):
    """
    TEST 1: Website Navigation Test
    - Open the FindIt website.
    - Verify that the page loads successfully.
    - Verify the page title.
    - Verify that the main navigation elements are visible.
    """
    driver = live_page

    # Verify core structural containers exist
    navbar = driver.find_element(By.ID, "navbar")
    assert navbar.is_displayed(), "Navbar should be visible"

    hero = driver.find_element(By.ID, "hero")
    assert hero.is_displayed(), "Hero section should be visible"

    stats_grid = driver.find_element(By.ID, "stats-grid")
    assert stats_grid.is_displayed(), "Statistics grid should be visible"

    catalog = driver.find_element(By.ID, "catalog-section")
    assert catalog.is_displayed(), "Catalog section should be visible"

    # Verify page branding title
    assert "FindIt" in driver.title
    assert "Lost & Found" in driver.title

    # Verify navigation links are visible
    brand = driver.find_element(By.ID, "nav-brand")
    assert brand.is_displayed(), "Brand logo must be visible"

    browse_link = driver.find_element(By.ID, "nav-items-link")
    assert browse_link.is_displayed(), "Browse directory nav link must be visible"

    report_link = driver.find_element(By.ID, "nav-report-link")
    assert report_link.is_displayed(), "Report item nav link must be visible"

    dashboard_link = driver.find_element(By.ID, "nav-dashboard-link")
    assert dashboard_link.is_displayed(), "Dashboard nav link must be visible"

    # Capture required lab screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "homepage.png")
    driver.save_screenshot(screenshot_path)


def test_02_search_functionality(live_page):
    """
    TEST 2: Search Functionality Test
    - Search for an existing reported item.
    - Verify that the matching item appears.
    - Search for an item that does not exist.
    - Verify that an appropriate empty-state message appears.
    """
    driver = live_page
    search_keyword = "Casio"

    search_input = driver.find_element(By.ID, "search-input")
    driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
    search_input.clear()
    search_input.send_keys(search_keyword)
    time.sleep(0.4)

    # Verify matching items appear
    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) >= 1, "Should show at least one matching item card"
    for card in visible_cards:
        assert "casio" in card.text.lower() or "calculator" in card.text.lower()

    # Capture required lab search results screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "search_results.png")
    driver.save_screenshot(screenshot_path)

    # Search for an item that does not exist
    search_input.clear()
    search_input.send_keys("XYZNonExistentCampusItem999")
    time.sleep(0.4)

    empty_state = driver.find_element(By.ID, "empty-state")
    assert empty_state.is_displayed(), "Empty state container must be displayed"

    empty_title = driver.find_element(By.ID, "empty-title").text
    assert "No Matching Items Found" in empty_title, "Should display helpful empty title"

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) == 0, "No item cards should be displayed for non-existent search"


def test_03_button_and_link(live_page):
    """
    TEST 3: Button and Link Test
    - Verify that the Report Lost Item button works.
    - Verify that the Report Found Item button works.
    - Verify that the relevant navigation links work.
    """
    driver = live_page

    # Verify Report Lost Item button activates lost form
    tab_lost = driver.find_element(By.ID, "tab-btn-lost")
    driver.execute_script("arguments[0].click();", tab_lost)
    time.sleep(0.2)
    lost_panel = driver.find_element(By.ID, "lost-tab-panel")
    assert lost_panel.is_displayed(), "Lost item tab panel should be visible"

    # Verify Report Found Item button activates found form
    tab_found = driver.find_element(By.ID, "tab-btn-found")
    driver.execute_script("arguments[0].click();", tab_found)
    time.sleep(0.2)
    found_panel = driver.find_element(By.ID, "found-tab-panel")
    assert found_panel.is_displayed(), "Found item tab panel should be visible"

    # Capture required report form screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "report_form.png")
    driver.save_screenshot(screenshot_path)

    # Switch back to lost panel
    driver.execute_script("arguments[0].click();", tab_lost)
    time.sleep(0.2)
    assert lost_panel.is_displayed()

    # Verify Hero Action Buttons
    hero_lost_btn = driver.find_element(By.ID, "btn-report-lost-hero")
    assert hero_lost_btn.is_displayed(), "Hero Report Lost button must be visible"
    hero_found_btn = driver.find_element(By.ID, "btn-report-found-hero")
    assert hero_found_btn.is_displayed(), "Hero Report Found button must be visible"

    # Verify navigation links work
    browse_link = driver.find_element(By.ID, "nav-items-link")
    assert browse_link.get_attribute("href").endswith("#catalog-section")

    report_link = driver.find_element(By.ID, "nav-report-link")
    assert report_link.get_attribute("href").endswith("#report-section")

    dashboard_link = driver.find_element(By.ID, "nav-dashboard-link")
    assert dashboard_link.get_attribute("href").endswith("#dashboard")


def test_04_form_validation(live_page):
    """
    TEST 4: Form Validation Test
    - Attempt to submit a report with missing required fields.
    - Verify that submission is prevented.
    - Verify that the appropriate validation message appears.
    """
    driver = live_page

    # Click submit without entering any fields
    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify global error alert is displayed
    error_banner = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_banner.is_displayed(), "Error message banner should be displayed"
    assert "please correct the highlighted errors" in error_banner.text.lower() or "required" in error_banner.text.lower()

    # Verify specific input fields are flagged as invalid
    name_input = driver.find_element(By.ID, "item-name")
    assert "invalid" in name_input.get_attribute("class"), "Name input must have invalid CSS class"

    # Capture required form validation screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "form_validation.png")
    driver.save_screenshot(screenshot_path)


def test_05_item_reporting(live_page):
    """
    TEST 5: Item Reporting Test
    - Submit a valid lost-item report.
    - Verify that the report appears in the item list.
    - Verify that its details are correct.
    """
    driver = live_page
    test_item_name = "Lab Verified Lenovo ThinkPad Laptop"
    test_location = "Science Block Auditorium B"

    # Fill in required inputs
    driver.find_element(By.ID, "item-name").send_keys(test_item_name)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Laptops")
    driver.find_element(By.ID, "item-location").send_keys(test_location)
    driver.execute_script("arguments[0].value = '2026-10-25';", driver.find_element(By.ID, "item-date"))
    driver.find_element(By.ID, "contact-name").send_keys("Rohan Gupta")
    driver.find_element(By.ID, "contact-email").send_keys("rohan.gupta@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Silver Apple sticker and red webcam slide cover.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify success alert banner appears
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed(), "Success banner should be visible"
    assert "recorded" in success_msg.text.lower() or "successfully" in success_msg.text.lower()

    # Verify the item card is appended in item list with correct details
    card = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//article[contains(., '{test_item_name}')]"))
    )
    assert card.is_displayed(), f"Card for '{test_item_name}' must be visible in catalog"
    assert test_location in card.text, "Reported location must match in item card"
    assert "Laptops" in card.text, "Reported category must match in item card"


def test_06_image_upload(live_page):
    """
    TEST 6: Image Upload Test
    - Upload a valid test image.
    - Verify that the image preview appears.
    - Verify that invalid image types are rejected if the application implements this validation.
    """
    driver = live_page

    # Create temporary valid PNG image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        temp_img_path = f.name

    try:
        file_input = driver.find_element(By.ID, "item-image-file")
        file_input.send_keys(temp_img_path)
        time.sleep(0.4)

        preview_box = driver.find_element(By.ID, "lost-image-preview-box")
        assert not ("d-none" in preview_box.get_attribute("class")), "Image preview box should become visible"

        preview_img = driver.find_element(By.ID, "lost-preview-img")
        assert preview_img.get_attribute("src").startswith("data:image/png"), "Preview src must contain valid image data"
    finally:
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)

    # Test rejection of invalid image type
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"Invalid plain text file.")
        temp_txt_path = f.name

    try:
        file_input = driver.find_element(By.ID, "item-image-file")
        file_input.send_keys(temp_txt_path)
        time.sleep(0.3)

        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "error-message"))
        )
        assert error_msg.is_displayed(), "Error message must appear for non-image file"
        assert "valid image file" in error_msg.text.lower() or "jpg" in error_msg.text.lower()
    finally:
        if os.path.exists(temp_txt_path):
            os.remove(temp_txt_path)


def test_07_recovery_functionality(live_page):
    """
    TEST 7: Recovery Functionality Test
    - Mark an eligible item as recovered.
    - Verify that its status changes.
    - Verify that the dashboard statistics update correctly.
    """
    driver = live_page

    initial_recovered = int(driver.find_element(By.ID, "stats-total-recovered").text)

    # Find the first active "Recover" button
    recover_buttons = driver.find_elements(By.CLASS_NAME, "btn-mark-recovered")
    assert len(recover_buttons) > 0, "Expected at least one active item to have a Recover button"

    first_btn = recover_buttons[0]
    item_id = first_btn.get_attribute("data-id")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", first_btn)

    # Verify success alert appears
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )

    # Verify status badge in card reflects Recovered
    card = driver.find_element(By.ID, f"item-card-{item_id}")
    status_badge = card.find_element(By.CLASS_NAME, "recovery-status")
    assert "recovered" in status_badge.text.lower(), "Status badge text must be 'Recovered'"
    assert "badge-recovered" in status_badge.get_attribute("class"), "Badge must have recovered style class"

    # Verify total recovered stat incremented by 1
    updated_recovered = int(driver.find_element(By.ID, "stats-total-recovered").text)
    assert updated_recovered == initial_recovered + 1, f"Expected {initial_recovered + 1}, got {updated_recovered}"

    # Capture required recovery status screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "recovery_status.png")
    driver.save_screenshot(screenshot_path)


def test_08_data_persistence(live_page):
    """
    TEST 8: Data Persistence Test
    - Create a report.
    - Refresh the browser.
    - Verify that the report remains available.
    """
    driver = live_page
    persistent_title = "Persistence Verified Campus ID Card"

    driver.find_element(By.ID, "item-name").send_keys(persistent_title)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("ID Cards")
    driver.find_element(By.ID, "item-location").send_keys("Hostel Block 4")
    driver.execute_script("arguments[0].value = '2026-10-24';", driver.find_element(By.ID, "item-date"))
    driver.find_element(By.ID, "contact-name").send_keys("Amit Patel")
    driver.find_element(By.ID, "contact-email").send_keys("amit.patel@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Green RFID room key card.")

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


def test_09_invalid_input(live_page):
    """
    TEST 9: Invalid Input Test
    - Test invalid dates (e.g., future date) and other supported validation rules.
    - Verify the actual validation behavior.
    """
    driver = live_page

    # 1. Test future date rejection
    driver.find_element(By.ID, "item-name").send_keys("Future Date Test Watch")
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Watches")
    driver.find_element(By.ID, "item-location").send_keys("Main Block")
    date_input = driver.find_element(By.ID, "item-date")
    driver.execute_script("arguments[0].value = '2028-12-31';", date_input)
    driver.find_element(By.ID, "contact-name").send_keys("Tester")
    driver.find_element(By.ID, "contact-email").send_keys("tester@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Testing future date validation.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", submit_btn)

    date_error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "date-error"))
    )
    assert date_error.is_displayed(), "Future date error message should be displayed"
    assert "future" in date_error.text.lower(), "Validation must reject future dates"

    # 2. Test invalid email format rejection
    driver.execute_script("arguments[0].value = '2026-10-25';", date_input)
    email_input = driver.find_element(By.ID, "contact-email")
    email_input.clear()
    email_input.send_keys("invalid-email-format")

    driver.execute_script("arguments[0].click();", submit_btn)
    time.sleep(0.2)

    email_error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "email-error"))
    )
    assert email_error.is_displayed(), "Email format error should be displayed"
    assert "valid email" in email_error.text.lower(), "Validation must require valid email"


def test_10_reset_demo_data(live_page):
    """
    TEST 10: Reset Demo Data Test
    - Reset the demo data.
    - Verify that the application returns to the expected initial state.
    """
    driver = live_page

    # Click Reset Demo Data button in footer
    reset_btn = driver.find_element(By.ID, "reset-demo-btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reset_btn)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", reset_btn)

    # Verify confirmation alert
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed(), "Reset success confirmation must appear"
    assert "reset" in success_msg.text.lower()

    # Verify dashboard statistics return to baseline: 4 Lost, 4 Found, 2 Recovered
    total_lost = int(driver.find_element(By.ID, "stats-total-lost").text)
    total_found = int(driver.find_element(By.ID, "stats-total-found").text)
    total_recovered = int(driver.find_element(By.ID, "stats-total-recovered").text)

    assert total_lost == 4, f"Expected 4 baseline lost items, got {total_lost}"
    assert total_found == 4, f"Expected 4 baseline found items, got {total_found}"
    assert total_recovered == 2, f"Expected 2 baseline recovered items, got {total_recovered}"

    # Verify baseline items are present
    items_count = len(driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card"))
    assert items_count >= 6, "Baseline catalog items should be restored"
