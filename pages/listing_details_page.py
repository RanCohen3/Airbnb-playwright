from datetime import datetime
from .base_page import BasePage
from playwright.sync_api import Page
import logging
import re
from typing import Dict


class ListingDetailsPage(BasePage):
    """
    Page object for the Airbnb listing details page
    """
    # locators
    RESERVE_BUTTON = 'button[data-testid="homes-pdp-cta-btn"]'
    PHONE_NUMBER_INPUT = 'input[data-testid="login-signup-phonenumber"]'
    CONTINUE_BUTTON = "button[data-testid='homes-pdp-cta-btn']"
    CHECK_IN_FROM_CARD = "div[data-testid='change-dates-checkIn']"
    CHECK_OUT_FROM_CARD = "div[data-testid='change-dates-checkOut']"
    PRICE_FROM_CARD = 'div[data-section-id="BOOK_IT_SIDEBAR"] span:has-text("per night")'
    NEXT_TO_BOOK = 'button span:has-text("Next")'

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def get_reservation_details(self) -> Dict:
        """
        Get details from the reservation card
        """
        self.logger.info("Getting reservation details")

        price_per_night_raw = self.page.query_selector(self.PRICE_FROM_CARD).text_content()
        match = re.search(r'[£$€¥₪](\d+,)?\d+ per night', price_per_night_raw)
        price_per_night_with_sign = match.group()

        checkin_from_card = self.page.locator(self.CHECK_IN_FROM_CARD).text_content()
        checkout_from_card = self.page.locator(self.CHECK_OUT_FROM_CARD).text_content()

        formatted_date_checkin = datetime.strptime(checkin_from_card, "%m/%d/%Y").strftime("%Y-%m-%d")
        formatted_date_checkout = datetime.strptime(checkout_from_card, "%m/%d/%Y").strftime("%Y-%m-%d")

        details = {
            "price_per_night": price_per_night_with_sign,
            "check-in": formatted_date_checkin,
            "check-out": formatted_date_checkout
                   }

        return details

    def click_reserve_button(self):
        """
        Click the reserve button
        """
        self.logger.info("Trying clicking reserve button")
        self.page.locator(self.RESERVE_BUTTON).nth(1).click()

    def enter_phone_number(self, phone_number: str):
        """
        Enter a phone number in the reservation form
        :param phone_number: Phone number
        """
        self.logger.info(f"Entering phone number: {phone_number}")
        self.page.locator(self.PHONE_NUMBER_INPUT).fill(phone_number)

    def request_to_book_next(self):
        """
        Click next in request to book
        :return:
        """
        self.page.locator(self.NEXT_TO_BOOK).click()
