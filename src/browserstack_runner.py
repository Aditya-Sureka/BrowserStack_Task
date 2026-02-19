from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

from src.scraper import scrape_articles
from src.translator import translate_titles
from src.text_analyzer import analyze_words
from src.config import USERNAME, ACCESS_KEY

import threading
import traceback


BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub.browserstack.com/wd/hub"


def create_driver(capabilities):
    browser_name = capabilities["browserName"].lower()

    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    elif browser_name == "edge":
        options = EdgeOptions()
    elif browser_name == "safari":
        options = SafariOptions()
    else:
        options = ChromeOptions()

    # Set all capabilities
    for key, value in capabilities.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options
    )

    return driver


def run_test(capabilities, test_name):
    driver = None
    try:
        print(f"[{test_name}] Starting test")

        driver = create_driver(capabilities)

        titles = scrape_articles(driver, test_name)
        translated = translate_titles(titles)
        analyze_words(translated)

        # Mark session as passed
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "All articles scraped and translated successfully"}}'
        )

        print(f"[{test_name}] Completed successfully")

    except Exception as e:
        print(f"[{test_name}] Error occurred: {e}")
        traceback.print_exc()

        if driver:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed","reason": "Test encountered an exception"}}'
            )

    finally:
        if driver:
            driver.quit()


def execute_parallel():

    common_bstack_options = {
        "buildName": "BrowserStack CE Assignment",
        "projectName": "Opinion Scraper",
        "sessionName": ""
    }

    browsers = [

        # Chrome - Windows
        {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "bstack:options": {
                **common_bstack_options,
                "sessionName": "Chrome - Windows 11",
                "os": "Windows",
                "osVersion": "11"
            }
        },

        # Firefox - Windows
        {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "bstack:options": {
                **common_bstack_options,
                "sessionName": "Firefox - Windows 11",
                "os": "Windows",
                "osVersion": "11"
            }
        },

        # Edge - Windows
        {
            "browserName": "Edge",
            "browserVersion": "latest",
            "bstack:options": {
                **common_bstack_options,
                "sessionName": "Edge - Windows 11",
                "os": "Windows",
                "osVersion": "11"
            }
        },

        # Safari - macOS
        {
            "browserName": "Safari",
            "browserVersion": "latest",
            "bstack:options": {
                **common_bstack_options,
                "sessionName": "Safari - macOS Ventura",
                "os": "OS X",
                "osVersion": "Ventura"
            }
        },

        # Chrome - Android
        {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "bstack:options": {
                **common_bstack_options,
                "sessionName": "Chrome - Samsung Galaxy S23",
                "deviceName": "Samsung Galaxy S23",
                "osVersion": "13.0"
            }
        },
    ]

    threads = []

    for idx, caps in enumerate(browsers):
        thread = threading.Thread(
            target=run_test,
            args=(caps, f"Test-{idx+1}")
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All parallel tests completed.")
