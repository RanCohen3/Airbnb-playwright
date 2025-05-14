import logging

from playwright.sync_api import expect

from pages.base_page import BasePage


class AirBnbHomePage(BasePage):
    URL = "https://www.airbnb.com/"
    # URL = "https://www.airbnb.com/s/Tel-Aviv~Yafo/homes?refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&place_id=ChIJH3w7GaZMHRURkD-WwKJy-8E&location_bb=QgCWIUILaGxCAB30Qgr4Vg%3D%3D&acp_id=4c8ed6e0-b6ab-4266-9b2c-6fbf97df7c7a&checkin=2025-08-01&checkout=2025-08-05&adults=2&children=1&source=structured_search_input_header&search_type=autocomplete_click"
    SEARCH_BUTTON = "[data-testid='structured-search-input-field-query']"
    NEXT_MONTH_BUTTON = '[aria-label="Next"]'
    CALENDAR_DAY_SELECTOR = "[data-testid^='calendar-day-']"

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def goto(self):
        self.page.goto(self.URL)

    def accept_cookies(self):
        if self.page.locator("button:has-text('Accept')").is_visible():
            self.page.click("button:has-text('Accept')")

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
        self.try_close_popup()
        homes_span_class = 'span[data-title="Homes"]'
        self.page.locator('span[data-title="Homes"]').click()        # span_locator.click()

        self.page.wait_for_selector(self.SEARCH_BUTTON).click()
        # self.page.click("[data-testid='structured-search-input-field-query']")
        self.page.wait_for_selector("input[id='bigsearch-query-location-input']")
        self.page.fill("input[id='bigsearch-query-location-input']", location)
        self.page.keyboard.press("Enter")

        # select dates
        self.try_close_popup()
        self.select_dates(checkin, checkout)

        #Add guests
        who_button = self.page.get_by_text("Who", exact=True)
        who_button.click()

        for _ in range(adults):
            # self.page.click('[data-testid=""stepper-adults-increase-button""]')
            self.page.get_by_role("button", name="increase value").first.click()

        for _ in range(children):
            # self.page.get_by_test_id("stepper-children-increase-button").click()
            self.page.get_by_role("button", name="increase value").nth(1).click()

        self.page.locator('[data-testid="structured-search-input-search-button"]').click()

    def select_dates(self, checkin: str, checkout: str):
        checked_in = False
        """Selects check-in and check-out dates, scrolling months if needed"""
        next_month_button = "button[aria-label='Move forward to switch to the next month.']"
        for _ in range(12):  # Try up to 12 months ahead
            # checkin_locator = self.page.locator(f"[data-state--date-string='{checkin}']")
            checkin_locator = self.page.get_by_role("button", name="1, Friday, August 2025. Available. Select as check-in date.")
            # checkout_locator = self.page.locator(f"[data-state--date-string='{checkout}']")
            checkout_locator = self.page.get_by_role("button", name="5, Tuesday, August 2025. Available. Select as checkout date.")



            # self.try_close_popup()
            # checkin_locator.wait_for(state="visible", timeout=5000)
            # self.try_close_popup()

            if checkin_locator.is_visible():
                checkin_locator.click()
                checked_in = True
            if checkout_locator.is_visible() and checked_in:
                checkout_locator.click()
                return


            self.page.get_by_role("button", name="Move forward to switch to the next month.").click()
            # next_button = self.page.locator(next_month_button)
            # next_button.wait_for(state="visible", timeout=5000)
            # next_button.click()
            #
            # # Wait for the "next month" button to exist and be visible
            # self.page.wait_for_selector(next_month_button, timeout=10000)
            #
            # # Click it using force just in case it's overlapped
            # self.page.locator(next_month_button).click(force=True)

        raise Exception(f"Could not find check-in/check-out dates: {checkin} - {checkout}")

    def try_close_popup(self):
        try:
            close_button = self.page.locator("button[aria-label='Close']")
            if close_button.is_visible(timeout=2000):
                close_button.click()
                self.page.wait_for_timeout(500)  # give it time to disappear
                return True
        except Exception:
            pass
        return False