from datetime import datetime

from .base_page import BasePage
from playwright.sync_api import Page, expect
import logging
import re
from typing import Dict


class ListingDetailsPage(BasePage):
    """Page object for the Airbnb listing details page"""

    # Locators
    LISTING_TITLE = "h1[data-testid='listing-title']"
    RESERVE_BUTTON = "button[data-testid='homes-pdp-cta-btn']"
    RESERVATION_CARD = "div[aria-label='Book']"
    PRICE_ELEMENT = "div[data-section-id='BOOK_IT_SIDEBAR'] span[data-testid='price-element']"
    TOTAL_PRICE_ELEMENT = "div[data-section-id='BOOK_IT_SIDEBAR'] span:has-text('total')"
    PHONE_NUMBER_INPUT = "input[type='tel']"
    CONTINUE_BUTTON = "button[data-testid='homes-pdp-cta-btn']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def get_reservation_details(self) -> Dict:
        """
        Get details from the reservation card
        """
        self.logger.info("Getting reservation details")

        price_per_night_raw = self.page.query_selector(
            'div[data-section-id="BOOK_IT_SIDEBAR"] span:has-text("per night")').text_content()
        match = re.search(r'[£$€¥₪]\d+ per night', price_per_night_raw)
        price_per_night_with_sign = match.group()

        checkin_from_card = self.page.locator("div[data-testid='change-dates-checkIn']").text_content()
        checkout_from_card = self.page.locator("div[data-testid='change-dates-checkOut']").text_content()

        formatted_date_checkin = datetime.strptime(checkin_from_card, "%m/%d/%Y").strftime("%Y-%m-%d")
        formatted_date_checkout = datetime.strptime(checkout_from_card, "%m/%d/%Y").strftime("%Y-%m-%d")

        details = {
            "price_per_night": price_per_night_with_sign,
            "check-in": formatted_date_checkin,
            "check-out": formatted_date_checkout
                   }

        return details

    def click_reserve_button(self):
        """Click the reserve button"""
        self.logger.info("Clicking reserve button")
        self.page.click('button[data-testid="homes-pdp-cta-btn"]')
        return self

    def enter_phone_number(self, phone_number: str):
        """
        Enter a phone number in the reservation form
        :param phone_number: Phone number
        """
        self.logger.info(f"Entering phone number: {phone_number}")

        # Wait for the phone number input to be visible
        self.page.wait_for_selector(self.PHONE_NUMBER_INPUT)

        # Fill the phone number input
        self.page.fill(self.PHONE_NUMBER_INPUT, phone_number)
        return self
