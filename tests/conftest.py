import os
import socket
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

# Directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
WEBSITE_DIR = os.path.join(PROJECT_ROOT, "website")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class QuietHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBSITE_DIR, **kwargs)

    def log_message(self, format, *args):
        # Suppress routine HTTP log messages during tests
        pass

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError):
            pass


@pytest.fixture(scope="session")
def server():
    """Detects running website (port 5000 or 8000) or starts a local HTTP server."""
    for test_port in (5000, 8000):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex(("127.0.0.1", test_port)) == 0:
                    yield f"http://127.0.0.1:{test_port}/index.html"
                    return
        except Exception:
            pass

    port = get_free_port()
    httpd = ThreadingHTTPServer(("127.0.0.1", port), QuietHTTPHandler)

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    base_url = f"http://127.0.0.1:{port}/index.html"
    yield base_url

    httpd.shutdown()
    httpd.server_close()


@pytest.fixture(scope="function")
def driver():
    """Initializes a clean Chrome WebDriver instance for each test."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-software-rasterizer")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(4)

    yield driver

    try:
        driver.quit()
    except Exception:
        pass


@pytest.fixture(scope="function")
def live_page(driver, server):
    """Navigates to the portal and resets localStorage to clean demo state."""
    driver.get(server)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "navbar"))
    )
    # Reset localStorage to default sample items before test execution
    driver.execute_script("localStorage.clear(); window.FindItApp.resetDemo();")
    time.sleep(0.3)
    return driver


def save_screenshot(driver, name):
    """Helper utility to capture genuine test screenshots."""
    filepath = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
    driver.save_screenshot(filepath)
    return filepath
