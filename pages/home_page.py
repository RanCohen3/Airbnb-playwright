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

    def open_page(self):
        self.page.goto(self.URL)

    def wait_page_load(self):
        self.page.wait_for_load_state('domcontentloaded')
    def switch_he_to_en(self):
        if "he." in self.page.url:
            # If not on the US site, look for the language/currency button
            language_currency_button = self.page.locator(
                "button[aria-label='בחירת שפה ומטבע']")  # Modify this selector if needed
            language_currency_button.click()  # Click to open the dropdown

            # Wait for the dropdown to open and select the US option (you'll need to find the exact selector for US)
            # us_option = page.locator("lang=en-US)")  # Change this selector if needed
            us_option = self.page.locator('a[lang="en-US"]')
            us_option.click()  # Click on English (US)


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

    def handle_popup_if_exists(self):
        try:
            logging.info(f"Looking for popups")
            has_pop_up = self.page\
                .wait_for_selector('div[data-testid="modal-container"]', state='visible', timeout=1000 * 10)
            if has_pop_up:
                self.page.query_selector('button:is([aria-label="Close"], [aria-label="סגירה"])').click()
                # self.page.locator("button[aria-label='סגירה']").click()
        except Exception:
            logging.error(f"Was not able to find a popup")
