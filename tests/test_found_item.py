import time
# pyrefly: ignore[missing-import]
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot


def test_07_successful_found_item_report(live_page):
    """
    Test Case 7: Verify successful report submission for a found item with valid data.
    """
    driver = live_page
    test_found_item = "Apple AirPods Pro (White Case)"

    # Switch to Report Found Item tab
    tab_found = driver.find_element(By.ID, "tab-btn-found")
    driver.execute_script("arguments[0].scrollIntoView(true);", tab_found)
    time.sleep(0.2)
    tab_found.click()

    # Verify found panel is active
    found_panel = driver.find_element(By.ID, "found-tab-panel")
    assert found_panel.is_displayed(), "Found tab panel should be visible"

    # Fill found form
    driver.find_element(By.ID, "found-item-name").send_keys(test_found_item)
    Select(driver.find_element(By.ID, "found-item-category")).select_by_value("Accessories")
    driver.find_element(By.ID, "found-item-location").send_keys("Campus Gym Locker Area")
    driver.find_element(By.ID, "found-item-date").send_keys("2026-10-26")
    driver.find_element(By.ID, "found-contact-name").send_keys("Security Officer Raman")
    driver.find_element(By.ID, "found-contact-email").send_keys("security@campus.edu")
    driver.find_element(By.ID, "found-item-description").send_keys("Found on bench next to locker 12. Kept at security desk.")

    submit_btn = driver.find_element(By.ID, "found-submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Verify success alert banner
    success_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert success_msg.is_displayed(), "Success message should be displayed"

    # Verify item is visible in item-list and marked as Found Item
    new_card = driver.find_element(By.XPATH, f"//article[contains(., '{test_found_item}')]")
    assert new_card.is_displayed(), f"Card for '{test_found_item}' should be visible in catalog"
    assert "found item" in new_card.text.lower(), "Card must have 'Found Item' badge"

    save_screenshot(driver, "07_successful_found_item_report")
