import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot


def test_04_successful_lost_item_report(live_page):
    """
    Test Case 4: Verify successful report submission for a lost item with valid data.
    """
    driver = live_page
    test_item_name = "Midnight Blue Lenovo ThinkPad"

    # Fill in required inputs
    driver.find_element(By.ID, "item-name").send_keys(test_item_name)
    
    category_dropdown = Select(driver.find_element(By.ID, "item-category"))
    category_dropdown.select_by_value("Laptops")

    driver.find_element(By.ID, "item-location").send_keys("Science Block Auditorium B")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-26")
    driver.find_element(By.ID, "contact-name").send_keys("Rohan Gupta")
    driver.find_element(By.ID, "contact-email").send_keys("rohan.gupta@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Has a silver Apple sticker and a red webcam slide cover.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify success alert banner appears
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed(), "Success banner should be visible"
    assert "successfully" in success_msg.text.lower()

    # Verify the item card is appended in item list
    item_titles = [el.text for el in driver.find_elements(By.CLASS_NAME, "item-title")]
    assert any(test_item_name in title for title in item_titles), f"'{test_item_name}' should be in item list"

    save_screenshot(driver, "04_successful_lost_item_report")


def test_05_empty_form_submission(live_page):
    """
    Test Case 5: Verify validation behavior when submitting an empty lost item form.
    """
    driver = live_page

    # Click submit without entering any field
    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify global error alert is displayed
    error_banner = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_banner.is_displayed(), "Error banner must be displayed on empty submission"

    # Verify individual field errors are triggered
    name_error = driver.find_element(By.ID, "name-error")
    assert "visible" in name_error.get_attribute("class"), "Name field error should be visible"

    email_error = driver.find_element(By.ID, "email-error")
    assert "visible" in email_error.get_attribute("class"), "Email field error should be visible"

    save_screenshot(driver, "05_empty_form_submission_validation")


def test_06_invalid_email_validation(live_page):
    """
    Test Case 6: Verify validation error is displayed when entering an invalid email format.
    """
    driver = live_page

    driver.find_element(By.ID, "item-name").send_keys("Keys with Blue Lanyard")
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Keys")
    driver.find_element(By.ID, "item-location").send_keys("Cafeteria Table 10")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-25")
    driver.find_element(By.ID, "contact-name").send_keys("Dev Anand")
    
    # Enter invalid email
    driver.find_element(By.ID, "contact-email").send_keys("invalid_email_format")
    driver.find_element(By.ID, "item-description").send_keys("Keys found near cafeteria.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify error alert
    error_banner = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "error-message"))
    )
    assert error_banner.is_displayed(), "Error banner should be visible for invalid email"

    email_error = driver.find_element(By.ID, "email-error")
    assert "visible" in email_error.get_attribute("class"), "Email specific error must be visible"

    save_screenshot(driver, "06_invalid_email_validation")
