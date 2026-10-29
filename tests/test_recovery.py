import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot


def test_11_mark_item_as_recovered(live_page):
    """
    Test Case 11: Verify marking an active item as recovered updates its status badge and statistics.
    """
    driver = live_page

    # Find the first active "Recover" button
    recover_buttons = driver.find_elements(By.CLASS_NAME, "btn-mark-recovered")
    assert len(recover_buttons) > 0, "Expected at least one active item to have a Recover button"

    initial_recovered = int(driver.find_element(By.ID, "stats-total-recovered").text)

    first_btn = recover_buttons[0]
    item_id = first_btn.get_attribute("data-id")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_btn)
    time.sleep(0.3)
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

    # Verify total recovered stat incremented
    updated_recovered = int(driver.find_element(By.ID, "stats-total-recovered").text)
    assert updated_recovered == initial_recovered + 1, "Total recovered count should increase by 1"

    save_screenshot(driver, "11_mark_item_as_recovered")


def test_13_data_persistence_after_page_refresh(live_page):
    """
    Test Case 13: Verify data persists via localStorage after browser refresh.
    """
    driver = live_page
    persistent_item_name = "Persistent Test Item - Campus Pass"

    # Submit a new item
    driver.find_element(By.ID, "item-name").send_keys(persistent_item_name)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("ID Cards")
    driver.find_element(By.ID, "item-location").send_keys("Hostel Block 4")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-24")
    driver.find_element(By.ID, "contact-name").send_keys("Amit Patel")
    driver.find_element(By.ID, "contact-email").send_keys("amit.patel@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Green RFID room key card.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)

    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )

    # Refresh browser page
    driver.refresh()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "navbar"))
    )
    time.sleep(0.5)

    # Verify item is still present in the directory
    item_titles = [el.text for el in driver.find_elements(By.CLASS_NAME, "item-title")]
    assert any(persistent_item_name in title for title in item_titles), "Persistent item must survive page refresh"

    save_screenshot(driver, "13_data_persistence_after_refresh")


def test_14_remove_item(live_page):
    """
    Test Case 14: Verify removing an item report deletes it from the directory and updates counts.
    """
    driver = live_page

    initial_items = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    initial_count = len(initial_items)
    assert initial_count > 0, "Catalog should have items before deletion"

    # Identify first item to delete
    first_card = initial_items[0]
    item_id = first_card.get_attribute("data-item-id")
    item_title = first_card.find_element(By.CLASS_NAME, "item-title").text

    delete_btn = driver.find_element(By.ID, f"delete-item-{item_id}")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", delete_btn)

    # Verify confirmation modal opens
    modal = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "delete-modal"))
    )
    assert modal.is_displayed(), "Delete confirmation modal should be visible"

    # Confirm deletion
    confirm_btn = driver.find_element(By.ID, "confirm-delete-btn")
    confirm_btn.click()

    # Wait for modal to dismiss and success message
    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.ID, "delete-modal"))
    )
    time.sleep(0.3)

    # Verify item is removed from catalog
    remaining_titles = [el.text for el in driver.find_elements(By.CLASS_NAME, "item-title")]
    assert item_title not in remaining_titles, f"'{item_title}' should no longer exist in catalog"

    remaining_count = len(driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card"))
    assert remaining_count == initial_count - 1, f"Expected {initial_count - 1} items remaining, got {remaining_count}"

    save_screenshot(driver, "14_remove_item_confirmed")
