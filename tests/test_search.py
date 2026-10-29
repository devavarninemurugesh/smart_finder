import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot


def test_08_search_existing_item(live_page):
    """
    Test Case 8: Verify search functionality returns existing items matching query keyword.
    """
    driver = live_page
    search_keyword = "Casio Scientific Calculator"

    search_input = driver.find_element(By.ID, "search-input")
    driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
    search_input.clear()
    search_input.send_keys(search_keyword)
    time.sleep(0.4)

    # Verify only matching items are displayed
    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) >= 1, "Should show at least one result for existing item"

    for card in visible_cards:
        assert "Casio" in card.text or "Calculator" in card.text, "Displayed card must match search term"

    save_screenshot(driver, "08_search_existing_item")


def test_09_search_nonexistent_item(live_page):
    """
    Test Case 9: Verify helpful empty state message is shown when searching for a non-existent item.
    """
    driver = live_page
    dummy_query = "XYZNonExistentCampusItem999"

    search_input = driver.find_element(By.ID, "search-input")
    driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
    search_input.clear()
    search_input.send_keys(dummy_query)
    time.sleep(0.4)

    # Verify empty state becomes visible
    empty_state = driver.find_element(By.ID, "empty-state")
    assert empty_state.is_displayed(), "Empty state container must be visible"

    empty_title = driver.find_element(By.ID, "empty-title").text
    assert "No Matching Items Found" in empty_title, "Should display helpful empty title"

    # Verify 0 items in list
    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) == 0, "No item cards should be rendered"

    save_screenshot(driver, "09_search_nonexistent_item")


def test_10_filter_by_category(live_page):
    """
    Test Case 10: Verify filtering items by category restricts results to the chosen category.
    """
    driver = live_page

    category_select = Select(driver.find_element(By.ID, "category-filter"))
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, "category-filter"))
    
    # Filter by Laptops
    category_select.select_by_value("Laptops")
    time.sleep(0.4)

    visible_cards = driver.find_elements(By.CSS_SELECTOR, "#item-list .item-card")
    assert len(visible_cards) > 0, "There should be laptops in demo data"

    for card in visible_cards:
        category_tag = card.find_element(By.CLASS_NAME, "item-category-tag").text
        assert category_tag == "Laptops", f"Expected category 'Laptops', found '{category_tag}'"

    save_screenshot(driver, "10_filter_by_category")
