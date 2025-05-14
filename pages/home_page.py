import logging

from playwright.sync_api import expect

from pages.base_page import BasePage


class AirBnbHomePage(BasePage):
    URL = "https://www.airbnb.com/"
    SEARCH_BUTTON = "[data-testid='structured-search-input-field-query']"
    NEXT_MONTH_BUTTON = '[aria-label="Next"]'
    CALENDAR_DAY_SELECTOR = "[data-testid^='calendar-day-']"

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def get_url(self):
        return self.page.url

    def select_date(self, target_date: str):
        """Navigates calendar to select a date like '2025-08-01'"""
        selector = f"[data-testid='calendar-day-{target_date}']"
        max_tries = 12  # Limit month scrolling to avoid infinite loop

        for _ in range(max_tries):
            if self.page.locator(selector).is_visible():
                self.page.locator(selector).click()
                return
            self.page.locator(self.NEXT_MONTH_BUTTON).click()
            self.page.wait_for_timeout(300)

        raise Exception(f"Date {target_date} not found or not selectable")

    def search(self, location, checkin, checkout, adults, children=0):
        # Search for location
        self.page.locator('span[data-title="Homes"]').click()
        self.page.wait_for_selector(self.SEARCH_BUTTON).click()
        self.page.wait_for_selector("input[id='bigsearch-query-location-input']")
        self.page.fill("input[id='bigsearch-query-location-input']", location)
        self.page.keyboard.press("Enter")

        # select dates
        self.select_dates(checkin, checkout)

        # Add guests
        who_button = self.page.get_by_text("Who", exact=True)
        who_button.click()

        # All plus selector has the same identifier, hence going by their indexes
        for _ in range(adults):
            self.page.get_by_role("button", name="increase value").nth(0).click()

        for _ in range(children):
            self.page.get_by_role("button", name="increase value").nth(1).click()

        self.page.locator('[data-testid="structured-search-input-search-button"]').click()

    def select_dates(self, checkin: str, checkout: str):
        checked_in = False
        """Selects check-in and check-out dates, scrolling months if needed"""
        next_month_button = "button[aria-label='Move forward to switch to the next month.']"
        for _ in range(12):  # Try up to 12 months ahead
            checkin_locator = self.page.locator(f"button[data-state--date-string='{checkin}']")
            checkout_locator = self.page.locator(f"button[data-state--date-string='{checkout}']")

            if checkin_locator.is_visible():
                checkin_locator.click()
                checked_in = True
            if checkout_locator.is_visible() and checked_in:
                checkout_locator.click()
                return

            self.page.get_by_role("button", name="Move forward to switch to the next month.").click()

        raise Exception(f"Could not find check-in/check-out dates: {checkin} - {checkout}")
