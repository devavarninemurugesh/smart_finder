import os
import sys
import uuid
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = os.environ.get("FINDIT_URL", "http://127.0.0.1:5000/")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
WAIT_SECONDS = 12

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
USE_COLOR = sys.stdout.isatty()

results = []
driver = None
test_item_name = None
test_item_id = None


def colored(text, color):
    if USE_COLOR:
        return f"{color}{text}{RESET}"
    return text


def print_info(message):
    print(f"[INFO] {message}")


def print_success(message):
    print(colored(f"[SUCCESS] {message}", GREEN))


def print_failure(name, error):
    print(colored(f"[FAIL] {name}", RED))
    explanation = str(error).strip() or error.__class__.__name__
    print(colored(f"[ERROR] {explanation.splitlines()[0][:220]}", RED))


def save_screenshot(filename):
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOTS_DIR, filename)
    if not driver.save_screenshot(path):
        raise RuntimeError(f"Chrome could not save screenshot: {filename}")


def click_element(locator):
    element = driver.find_element(*locator)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest', behavior: 'instant'});",
        element,
    )
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda browser: browser.execute_script(
            "const rect = arguments[0].getBoundingClientRect(); "
            "return rect.top >= 0 && rect.bottom <= window.innerHeight;",
            element,
        )
    )
    WebDriverWait(driver, WAIT_SECONDS).until(EC.element_to_be_clickable(locator)).click()


def run_test(name, action, success_message):
    try:
        action()
    except Exception as error:
        results.append((name, False))
        print_failure(name, error)
        return False

    results.append((name, True))
    print_success(success_message)
    return True


def open_browser():
    global driver

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 900)


def open_website():
    if driver is None:
        raise RuntimeError("Chrome WebDriver is not available.")

    driver.get(BASE_URL)
    WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.ID, "navbar"))
    )
    if "localhost" not in driver.current_url and "127.0.0.1" not in driver.current_url:
        raise AssertionError(f"Expected a local FindIt URL, opened {driver.current_url}")
    save_screenshot("selenium_homepage.png")


def verify_page_title():
    title = driver.title.strip()
    assert "findit" in title.casefold(), f"Page title does not identify FindIt: {title!r}"


def verify_dashboard():
    wait = WebDriverWait(driver, WAIT_SECONDS)
    heading = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#dashboard .section-title"))
    )
    assert "Dashboard Overview" in heading.text, "Dashboard heading was not displayed."

    wait.until(EC.visibility_of_element_located((By.ID, "stats-grid")))
    statistics = driver.find_elements(By.CSS_SELECTOR, "#stats-grid .stat-value")
    assert len(statistics) >= 4, "Expected dashboard statistics were not found."
    for statistic in statistics:
        assert statistic.is_displayed(), "A dashboard statistic is not visible."
        assert statistic.text.strip().isdigit(), (
            f"Dashboard statistic is not a number: {statistic.text!r}"
        )

    save_screenshot("selenium_dashboard_statistics.png")


def test_navigation():
    click_element((By.ID, "nav-items-link"))
    wait = WebDriverWait(driver, WAIT_SECONDS)
    wait.until(EC.url_contains("#catalog-section"))
    catalog_heading = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#catalog-section .section-title"))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
        catalog_heading,
    )
    assert "Campus Item Directory" in catalog_heading.text
    save_screenshot("selenium_browse_items.png")


def test_search():
    click_element((By.ID, "clear-filters-btn"))
    search_input = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.ID, "search-input"))
    )
    search_input.clear()
    search_input.send_keys("Casio Scientific Calculator")

    def matching_item_is_visible(browser):
        for card in browser.find_elements(By.CSS_SELECTOR, "#item-list .item-card"):
            title = card.find_element(By.CLASS_NAME, "item-title")
            if title.is_displayed() and "Casio" in title.text:
                return card
        return False

    card = WebDriverWait(driver, WAIT_SECONDS).until(matching_item_is_visible)
    assert "Casio" in card.find_element(By.CLASS_NAME, "item-title").text
    save_screenshot("selenium_search_results.png")


def test_form_validation():
    click_element((By.ID, "clear-filters-btn"))
    click_element((By.ID, "nav-report-link"))
    wait = WebDriverWait(driver, WAIT_SECONDS)
    wait.until(EC.visibility_of_element_located((By.ID, "lost-item-form")))

    click_element((By.ID, "submit-report"))
    error_message = wait.until(EC.visibility_of_element_located((By.ID, "error-message")))
    assert error_message.text.strip(), "The empty form did not show a validation message."
    assert "visible" in driver.find_element(By.ID, "name-error").get_attribute("class"), (
        "The required item-name field did not show its validation error."
    )
    assert "visible" in driver.find_element(By.ID, "category-error").get_attribute("class"), (
        "The required category field did not show its validation error."
    )
    save_screenshot("selenium_empty_form_validation.png")


def find_test_item_card(browser):
    if not test_item_name:
        return False

    for card in browser.find_elements(By.CSS_SELECTOR, "#item-list .item-card"):
        title = card.find_element(By.CLASS_NAME, "item-title")
        if title.text.strip() == test_item_name:
            return card
    return False


def create_test_report():
    global test_item_name, test_item_id

    test_item_name = f"Selenium Lab Test Item {uuid.uuid4().hex[:8]}"
    driver.find_element(By.ID, "item-name").send_keys(test_item_name)
    Select(driver.find_element(By.ID, "item-category")).select_by_value("Other")
    driver.find_element(By.ID, "item-location").send_keys("Selenium Test Location")
    driver.find_element(By.ID, "item-date").send_keys(date.today().isoformat())
    driver.find_element(By.ID, "contact-name").send_keys("Selenium Test User")
    driver.find_element(By.ID, "contact-email").send_keys("selenium.test@example.com")
    driver.find_element(By.ID, "item-description").send_keys(
        f"Temporary test report created by website_test.py ({test_item_name})."
    )
    click_element((By.ID, "submit-report"))

    wait = WebDriverWait(driver, WAIT_SECONDS)
    success_message = wait.until(
        EC.visibility_of_element_located((By.ID, "success-message"))
    )
    assert test_item_name in success_message.text, (
        f"Report success message did not identify {test_item_name!r}."
    )
    card = wait.until(find_test_item_card)
    test_item_id = card.get_attribute("data-item-id")
    assert test_item_id, "The created test report has no item ID."
    save_screenshot("selenium_test_report_submitted.png")


def recover_test_report():
    if not test_item_name:
        raise RuntimeError("No test report was created to verify recovery.")

    wait = WebDriverWait(driver, WAIT_SECONDS)
    card = wait.until(find_test_item_card)
    item_id = card.get_attribute("data-item-id")
    click_element((By.ID, f"mark-recovered-{item_id}"))

    def report_is_recovered(browser):
        current_card = browser.find_element(By.ID, f"item-card-{item_id}")
        badge = current_card.find_element(By.CLASS_NAME, "recovery-status")
        return (
            "recovered" in badge.text.casefold()
            and "badge-recovered" in badge.get_attribute("class")
        )

    wait.until(report_is_recovered)
    assert item_id == test_item_id, "Recovery targeted a different report than the test report."
    save_screenshot("selenium_test_item_recovered.png")


def cleanup_test_report():
    if not test_item_name:
        print_info("Test report cleanup not needed; no report was created.")
        return

    wait = WebDriverWait(driver, WAIT_SECONDS)
    card = wait.until(find_test_item_card)
    item_id = card.get_attribute("data-item-id")
    assert item_id == test_item_id, "Refusing to delete a report that was not created by this test."

    click_element((By.ID, f"delete-item-{item_id}"))
    wait.until(EC.visibility_of_element_located((By.ID, "delete-modal")))
    click_element((By.ID, "confirm-delete-btn"))
    wait.until(EC.invisibility_of_element_located((By.ID, "delete-modal")))
    wait.until(EC.staleness_of(card))
    assert not driver.find_elements(By.ID, f"item-card-{item_id}"), (
        "The test report remained in the catalog after cleanup."
    )
    save_screenshot("selenium_test_report_cleanup.png")


def print_report():
    total = len(results)
    passed = sum(1 for _, success in results if success)
    failed = total - passed
    rate = (passed / total * 100) if total else 0

    print()
    print(colored("========== TEST EXECUTION SUMMARY ==========", BLUE))
    print(f"Total tests executed: {total}")
    print(f"Passed tests: {passed}")
    print(f"Failed tests: {failed}")
    print(f"Success rate: {rate:.1f}%")
    status = "PASSED" if failed == 0 and total > 0 else "FAILED"
    print(f"Overall test execution status: {colored(status, GREEN if status == 'PASSED' else RED)}")


def main():
    global driver

    print(colored("========== SELENIUM TEST EXECUTION ==========", BLUE))
    print()

    print_info("Opening Chrome Browser...")
    browser_opened = run_test(
        "Chrome WebDriver initialization",
        open_browser,
        "Chrome browser opened successfully.",
    )

    if browser_opened:
        print()
        print_info("Navigating to the FindIt website...")
        run_test("Website navigation", open_website, "Website opened successfully.")

        print()
        print_info("Verifying page title...")
        run_test(
            "Page title verification",
            verify_page_title,
            "Page title verified successfully.",
        )

        print()
        print_info("Checking dashboard statistics...")
        run_test(
            "Dashboard statistics",
            verify_dashboard,
            "Dashboard statistics verified successfully.",
        )

        print()
        print_info("Testing website navigation...")
        run_test("Browse Items navigation", test_navigation, "Navigation test passed.")

        print()
        print_info("Testing search functionality...")
        run_test("Item search", test_search, "Search test passed.")

        print()
        print_info("Testing form validation...")
        run_test("Empty form validation", test_form_validation, "Form validation test passed.")

        print()
        print_info("Testing valid item reporting...")
        report_created = run_test(
            "Valid item report",
            create_test_report,
            "Valid test report appeared in the website.",
        )

        print()
        print_info("Testing item recovery...")
        if report_created:
            run_test(
                "Item recovery",
                recover_test_report,
                "Test item status changed to Recovered.",
            )
        else:
            print_info("Item recovery skipped because the test report was not created.")

        print()
        if test_item_name:
            print_info("Cleaning up the test report...")
            run_test(
                "Test report cleanup",
                cleanup_test_report,
                "Test report was removed without affecting demo records.",
            )

    try:
        if driver is not None:
            driver.quit()
    except WebDriverException as error:
        results.append(("Chrome WebDriver shutdown", False))
        print_failure("Chrome WebDriver shutdown", error)

    print_report()
    return 0 if results and all(success for _, success in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
