import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import save_screenshot


def test_01_home_page_loading(live_page):
    """
    Test Case 1: Verify the Home Page loads successfully with all major sections.
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

    footer = driver.find_element(By.ID, "footer")
    assert footer.is_displayed(), "Footer should be visible"

    save_screenshot(driver, "01_home_page_loaded")


def test_02_page_title_verification(live_page):
    """
    Test Case 2: Verify the page title matches the expected application branding.
    """
    driver = live_page
    expected_title = "FindIt – Smart Lost & Found Management Portal"
    assert driver.title == expected_title, f"Expected title '{expected_title}', but got '{driver.title}'"


def test_03_dashboard_statistics(live_page):
    """
    Test Case 3: Verify initial dashboard statistics reflect the sample campus dataset.
    Default dataset: 3 Lost, 3 Found, 2 Recovered.
    """
    driver = live_page

    total_lost = driver.find_element(By.ID, "stats-total-lost").text
    total_found = driver.find_element(By.ID, "stats-total-found").text
    total_recovered = driver.find_element(By.ID, "stats-total-recovered").text

    assert int(total_lost) == 4, f"Expected 4 initial lost items, got {total_lost}"
    assert int(total_found) == 4, f"Expected 4 initial found items, got {total_found}"
    assert int(total_recovered) == 2, f"Expected 2 initial recovered items, got {total_recovered}"

    save_screenshot(driver, "03_dashboard_statistics")


def test_12_verify_updated_dashboard_statistics(live_page):
    """
    Test Case 12: Verify dashboard statistics dynamically increment upon submitting a report.
    """
    driver = live_page

    initial_lost = int(driver.find_element(By.ID, "stats-total-lost").text)

    # Fill lost item form
    driver.find_element(By.ID, "item-name").send_keys("Automated Stat Test Item")
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Laptops")
    driver.find_element(By.ID, "item-location").send_keys("Testing Block A")
    driver.find_element(By.ID, "item-date").send_keys("2026-10-25")
    driver.find_element(By.ID, "contact-name").send_keys("Tester Bot")
    driver.find_element(By.ID, "contact-email").send_keys("tester@campus.edu")
    driver.find_element(By.ID, "item-description").send_keys("Test description for statistics check.")

    submit_btn = driver.find_element(By.ID, "submit-report")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", submit_btn)

    # Wait for success message
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )

    # Verify stat incremented by 1
    updated_lost = int(driver.find_element(By.ID, "stats-total-lost").text)
    assert updated_lost == initial_lost + 1, f"Expected lost count {initial_lost + 1}, got {updated_lost}"

    save_screenshot(driver, "12_dashboard_statistics_updated")


def test_15_responsive_layout_checks(live_page):
    """
    Test Case 15: Verify layout responsiveness at Mobile (375x667), Tablet (768x1024), and Desktop (1280x800).
    """
    driver = live_page

    viewports = [
        ("mobile", 375, 667),
        ("tablet", 768, 1024),
        ("desktop", 1280, 800)
    ]

    for name, width, height in viewports:
        driver.set_window_size(width, height)
        time.sleep(0.4)

        # Verify key elements are visible and do not break
        navbar = driver.find_element(By.ID, "navbar")
        assert navbar.is_displayed(), f"Navbar should be visible at {width}x{height}"

        search_input = driver.find_element(By.ID, "search-input")
        assert search_input.is_displayed(), f"Search input should be visible at {width}x{height}"

        item_list = driver.find_element(By.ID, "item-list")
        assert item_list.is_displayed(), f"Item list should be visible at {width}x{height}"

        # Check there is no horizontal body scroll overflow
        scroll_width = driver.execute_script("return document.body.scrollWidth")
        client_width = driver.execute_script("return document.documentElement.clientWidth")
        assert scroll_width <= client_width + 5, f"Horizontal overflow detected at {width}x{height}: scrollWidth={scroll_width}, clientWidth={client_width}"

        save_screenshot(driver, f"15_responsive_{name}_{width}x{height}")
