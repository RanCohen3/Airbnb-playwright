import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import logging


@pytest.fixture(scope="function")
def check_airbnb_us(page: Page):
    # Navigate to Airbnb (or any URL you expect to be the homepage)
    page.goto("https://www.airbnb.com")

    # Check if we're on the US site by looking for a specific element (e.g., currency or language indicator)
    if "he." in page.url:
        # If not on the US site, look for the language/currency button
        language_currency_button = page.locator("button[aria-label='בחירת שפה ומטבע']")  # Modify this selector if needed
        language_currency_button.click()  # Click to open the dropdown

        # Wait for the dropdown to open and select the US option (you'll need to find the exact selector for US)
        # us_option = page.locator("lang=en-US)")  # Change this selector if needed
        us_option = page.locator('a._5af8mpi[lang="en-US"]')
        us_option.click()  # Click on English (US)

        # Ensure the page is now on the US version (check URL or any other indicator)
        assert "airbnb.com" in page.url, "Failed to load the US Airbnb site."


@pytest.fixture(scope="session")
def test_data():
    """Fixture for providing test data"""
    return {
        "destination": "Tel Aviv, Israel",
        "adults": 2,
        "children": 0,
        "child_age": 8,  # For test case #2
        "phone_prefix": "+972"  # Israel country code
    }

