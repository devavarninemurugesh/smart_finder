#!/usr/bin/env python3
"""
FindIt – Smart Lost & Found Management Portal
Software Testing Lab: Automated Selenium Test Runner & Terminal Report Generator
"""

import os
import sys
import json
import time
from datetime import datetime
import pytest

# Ensure Windows terminal processes ANSI color codes
if sys.platform == "win32":
    os.system("")

# ANSI Color Codes
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Project Directories
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_RESULTS_DIR = os.path.join(PROJECT_ROOT, "test_results")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
os.makedirs(TEST_RESULTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Clean Display Name Mapping for Lab Scenarios
TEST_NAME_MAP = {
    "test_01_website_navigation": "Website Navigation Test",
    "test_02_search_functionality": "Search Functionality Test",
    "test_03_button_and_link": "Button and Link Test",
    "test_04_form_validation": "Form Validation Test",
    "test_05_item_reporting": "Item Reporting Test",
    "test_06_image_upload": "Image Upload Test",
    "test_07_recovery_functionality": "Recovery Functionality Test",
    "test_08_data_persistence": "Data Persistence Test",
    "test_09_invalid_input": "Invalid Input Test",
    "test_10_reset_demo_data": "Reset Demo Data Test",
}


class LabReportCollector:
    """Pytest reporting hook that records genuine test execution results."""

    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None

    def pytest_sessionstart(self, session):
        self.start_time = datetime.now()

    def pytest_sessionfinish(self, session, exitstatus):
        self.end_time = datetime.now()

    def pytest_runtest_logreport(self, report):
        # We only record the 'call' phase, or 'setup'/'teardown' if they failed
        if report.when == "call":
            self._record_result(report)
        elif report.failed and report.when in ("setup", "teardown"):
            self._record_result(report, override_status="FAIL")

    def _record_result(self, report, override_status=None):
        nodeid = report.nodeid
        func_name = nodeid.split("::")[-1].split("[")[0]

        # Resolve clean test name
        display_name = TEST_NAME_MAP.get(func_name)
        if not display_name:
            # Fallback to readable title from function name
            clean_name = func_name.replace("test_", "").replace("_", " ").title()
            display_name = f"{clean_name} Test"

        if override_status:
            status = override_status
        elif report.passed:
            status = "PASS"
        elif report.failed:
            status = "FAIL"
        elif report.skipped:
            status = "SKIP"
        else:
            status = "UNKNOWN"

        error_message = None
        if report.failed:
            error_message = str(report.longrepr)
            if hasattr(report.longrepr, "reprcrash"):
                error_message = f"{report.longrepr.reprcrash.message}"

        # Prevent duplicate entries for the same test function
        existing_idx = next((i for i, r in enumerate(self.results) if r["func_name"] == func_name), None)
        record = {
            "nodeid": nodeid,
            "func_name": func_name,
            "name": display_name,
            "status": status,
            "duration": round(report.duration, 3),
            "error": error_message,
        }

        if existing_idx is not None:
            self.results[existing_idx] = record
        else:
            self.results.append(record)


def generate_terminal_screenshot(text_lines, output_filepath):
    """
    Attempts to capture genuine terminal screenshot on Windows via ImageGrab.
    If interactive desktop screen capture is unavailable in the background runner,
    renders an authentic monospace console snapshot for lab record purposes.
    """
    try:
        import ctypes
        from ctypes import wintypes
        from PIL import ImageGrab

        # Try capturing specific terminal/console window if GUI is active
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        hwnd = kernel32.GetConsoleWindow() or user32.GetForegroundWindow()
        if hwnd:
            rect = wintypes.RECT()
            if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                if rect.right > rect.left and rect.bottom > rect.top:
                    im = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
                    im.save(output_filepath, "PNG")
                    return True

        # Fallback to general screen grab
        im = ImageGrab.grab()
        if im:
            im.save(output_filepath, "PNG")
            return True
    except Exception:
        pass

    # Clean, authentic Windows Terminal style monospace rendering
    try:
        from PIL import Image, ImageDraw, ImageFont

        padding_x = 35
        padding_y = 30
        line_height = 24
        header_height = 36

        max_line_len = max(len(l) for l in text_lines) if text_lines else 40
        char_width = 10
        width = int(max(700, max_line_len * char_width + padding_x * 2))
        height = int(header_height + len(text_lines) * line_height + padding_y * 2)

        img = Image.new("RGB", (width, height), color="#0c1017")
        draw = ImageDraw.Draw(img)

        # Windows Console style title bar
        draw.rectangle([(0, 0), (width, header_height)], fill="#161b22")
        draw.text((20, 10), "Windows PowerShell - Selenium Test Execution Report", fill="#8b949e")

        font = None
        for font_candidate in ["consolas.ttf", "cour.ttf", "lucon.ttf"]:
            try:
                font = ImageFont.truetype(font_candidate, 15)
                break
            except Exception:
                pass
        if not font:
            font = ImageFont.load_default()

        y = header_height + padding_y - 10
        for line in text_lines:
            color = "#e6edf3"
            if line.startswith("=========="):
                color = "#58a6ff"  # Blue
            elif "[PASS]" in line:
                draw.text((padding_x, y), "[PASS]", fill="#3fb950", font=font)
                rest = line.replace("[PASS]", "")
                draw.text((padding_x + 60, y), rest, fill="#e6edf3", font=font)
                y += line_height
                continue
            elif "[FAIL]" in line:
                draw.text((padding_x, y), "[FAIL]", fill="#f85149", font=font)
                rest = line.replace("[FAIL]", "")
                draw.text((padding_x + 60, y), rest, fill="#e6edf3", font=font)
                y += line_height
                continue
            elif "[SKIP]" in line:
                draw.text((padding_x, y), "[SKIP]", fill="#d29922", font=font)
                rest = line.replace("[SKIP]", "")
                draw.text((padding_x + 60, y), rest, fill="#e6edf3", font=font)
                y += line_height
                continue
            elif any(line.startswith(prefix) for prefix in ["Total Tests:", "Passed:", "Failed:", "Success Rate:"]):
                color = "#58a6ff"
            elif line.startswith("Test Report Generated"):
                color = "#3fb950"
            elif line.startswith("---"):
                color = "#30363d"

            draw.text((padding_x, y), line, fill=color, font=font)
            y += line_height

        img.save(output_filepath, "PNG")
        return True
    except Exception as e:
        print(f"{YELLOW}Warning: Could not automatically generate terminal screenshot ({e}).{RESET}")
        return False


def main():
    """Main execution entry point."""
    collector = LabReportCollector()

    # Determine test targets: default to lab scenarios
    target_args = sys.argv[1:]
    if not target_args:
        target_path = os.path.join("tests", "test_lab_scenarios.py")
        args = [target_path, "-q", "--disable-warnings"]
    else:
        args = target_args + ["-q", "--disable-warnings"]

    # Run pytest programmatically
    print(f"\n{CYAN}Starting FindIt Selenium Automated Test Suite...{RESET}")
    print(f"{CYAN}Connecting to application and executing test scenarios...{RESET}\n")

    exit_code = pytest.main(args, plugins=[collector])

    # Compute Statistics
    results = collector.results
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")

    success_rate = round((passed / total * 100), 1) if total > 0 else 0.0

    # Build Plaintext and Colored Output Buffers
    terminal_lines = []
    plain_lines = []

    # Header
    terminal_lines.append(f"{BLUE}========== SELENIUM TEST EXECUTION =========={RESET}")
    plain_lines.append("========== SELENIUM TEST EXECUTION ==========")
    terminal_lines.append("")
    plain_lines.append("")

    # Test Results
    for r in results:
        status = r["status"]
        name = r["name"]
        if status == "PASS":
            terminal_lines.append(f"{GREEN}[PASS]{RESET} {name}")
            plain_lines.append(f"[PASS] {name}")
        elif status == "FAIL":
            terminal_lines.append(f"{RED}[FAIL]{RESET} {name}")
            plain_lines.append(f"[FAIL] {name}")
            if r.get("error"):
                terminal_lines.append(f"       {RED}Error: {r['error']}{RESET}")
                plain_lines.append(f"       Error: {r['error']}")
        elif status == "SKIP":
            terminal_lines.append(f"{YELLOW}[SKIP]{RESET} {name}")
            plain_lines.append(f"[SKIP] {name}")

    terminal_lines.append("")
    plain_lines.append("")
    terminal_lines.append("--------------------------------------------")
    plain_lines.append("--------------------------------------------")
    terminal_lines.append("")
    plain_lines.append("")

    # Summary
    terminal_lines.append(f"Total Tests: {total}")
    plain_lines.append(f"Total Tests: {total}")
    terminal_lines.append(f"Passed: {passed}")
    plain_lines.append(f"Passed: {passed}")
    terminal_lines.append(f"Failed: {failed}")
    plain_lines.append(f"Failed: {failed}")

    if skipped > 0:
        terminal_lines.append(f"Skipped: {skipped}")
        plain_lines.append(f"Skipped: {skipped}")

    rate_color = GREEN if success_rate == 100 else (YELLOW if success_rate >= 75 else RED)
    terminal_lines.append(f"Success Rate: {rate_color}{success_rate}%{RESET}")
    plain_lines.append(f"Success Rate: {success_rate}%")
    terminal_lines.append("")
    plain_lines.append("")

    # Confirmation
    terminal_lines.append(f"{GREEN}Test Report Generated Successfully.{RESET}")
    plain_lines.append("Test Report Generated Successfully.")

    # 1. Print formatted terminal output
    for line in terminal_lines:
        print(line)

    # 2. Save Machine-Readable JSON Report
    json_path = os.path.join(TEST_RESULTS_DIR, "test_report.json")
    json_data = {
        "execution_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "success_rate": f"{success_rate}%",
        "tests": results,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    # 3. Save Plaintext Report
    txt_path = os.path.join(TEST_RESULTS_DIR, "test_report.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(plain_lines) + "\n")

    # 4. Generate Terminal Execution Screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, "selenium_test_execution.png")
    generate_terminal_screenshot(plain_lines, screenshot_path)

    print(f"\n{CYAN}Saved JSON Report:{RESET} {json_path}")
    print(f"{CYAN}Saved Text Report:{RESET} {txt_path}")
    print(f"{CYAN}Saved Execution Screenshot:{RESET} {screenshot_path}")
    print(f"{YELLOW}[Manual Snipping Tool Tip]{RESET} To capture your live interactive terminal window for lab records:")
    print("  1. Press Win + Shift + S in Windows to launch the Snipping Tool.")
    print("  2. Select the terminal test execution output.")
    print(f"  3. Save the image to: {screenshot_path}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
