import logging

from pages.base_page import BasePage


class AirBnbHomePage(BasePage):
    URL = "https://www.airbnb.com/"
    SEARCH_BUTTON = "[data-testid='structured-search-input-field-query']"
    NEXT_MONTH_BUTTON = "Move forward to switch to the next month."
    PRESS_SEARCH = '[data-testid="structured-search-input-search-button"]'

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def get_url(self):
        """
        Get url
        """
        return self.page.url

    def search(self, location, checkin, checkout, adults, children=0):
        """
        This method in charge of entering all the data to the search.
        :param location: The location to search for.
        :param checkin: Check in date
        :param checkout: Check in date
        :param adults: Number of adults
        :param children: Number of children
        """
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

        self.page.locator(self.PRESS_SEARCH).click()

    def select_dates(self, checkin, checkout):
        """
        This method selects the dates in the calendar.
        :param checkin: Check in date
        :param checkout: Check out date
        """
        checked_in = False
        for _ in range(12):
            # Try up to 12 months ahead
            checkin_locator = self.page.locator(f"button[data-state--date-string='{checkin}']")
            checkout_locator = self.page.locator(f"button[data-state--date-string='{checkout}']")

            if checkin_locator.is_visible():
                checkin_locator.click()
                checked_in = True
            if checkout_locator.is_visible() and checked_in:
                checkout_locator.click()
                return

            self.page.get_by_role("button", name=self.NEXT_MONTH_BUTTON).click()

        raise Exception(f"Could not find check-in/check-out dates: {checkin} - {checkout}")
