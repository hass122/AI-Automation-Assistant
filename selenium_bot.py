import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def run_selenium_demo(keyword):
    """Run the local HTML automation demo in headless Chrome/Chromium."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    page = os.path.join(project_root, "automation", "demo_page.html")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")

    # Selenium Manager handles the browser/driver lookup when available.
    # An optional CHROME_BINARY environment variable can be supplied by a
    # hosting environment that provides a custom Chromium binary.
    chrome_binary = os.getenv("CHROME_BINARY")
    if chrome_binary and os.path.exists(chrome_binary):
        options.binary_location = chrome_binary

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("file:///" + page.replace("\\", "/"))
        box = driver.find_element(By.ID, "search")
        box.send_keys(keyword)

        button = driver.find_element(By.ID, "searchBtn")
        button.click()

        time.sleep(0.4)
        result = driver.find_element(By.ID, "result").text

        return {
            "status": "Success",
            "action": "Opened page → entered keyword → clicked Search → read result",
            "result": result,
        }
    finally:
        driver.quit()
