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

        # self.page.pause()

        self.page.locator("button[data-testid='book-it-default']").first.text_content()

        price_selector = 'span[class*="u1dgw2qm"]'
        self.page.wait_for_selector(price_selector)
        price_per_night_with_sign = self.page.locator(price_selector).first.text_content()
        price_per_night = re.sub(r'[^\d.]', '', price_per_night_with_sign)

        checkin_from_card = self.page.locator("div[data-testid='change-dates-checkIn']").text_content()
        checkout_from_card = self.page.locator("div[data-testid='change-dates-checkOut']").text_content()

        formatted_date_checkin = datetime.strptime(checkin_from_card, "%m/%d/%Y").strftime("%Y-%m-%d")
        formatted_date_checkout = datetime.strptime(checkout_from_card, "%m/%d/%Y").strftime("%Y-%m-%d")

        # Extract check-in and check-out dates
        # checkin_selector = '[data-testid="change-dates-checkIn"]'
        # checkout_selector = '[data-testid="change-dates-checkOut"]'
        # checkin_date = self.page.locator('[data-testid="change-dates-checkIn"]')
        #
        # checkout_date = self.page.locator(checkout_selector).text_content()

        # Extract number of guests
        # guests_selector = 'span._j1kt73'  # May need adjustment
        # guests = self.page.locator(guests_selector).first.text_content()


        # sidebar = self.page.locator('[data-plugin-in-point-id="BOOK_IT_SIDEBAR"]')
        # text = sidebar.inner_text()

        # # Wait for reservation card to be visible
        # self.page.wait_for_selector(self.RESERVATION_CARD)
        #
        # # Get listing title
        # # title = self.page.get_text(self.LISTING_TITLE)
        # title = self.page.locator(self.LISTING_TITLE).get_attribute("content")
        #
        # # Get price per night
        # price_text = self.page.get_text(self.PRICE_ELEMENT)
        # price_match = re.search(r"\$([0-9,]+)", price_text)
        # price = price_match.group(1).replace(",", "") if price_match else "N/A"
        #
        # # Get total price if available
        # total_price = "N/A"
        # if self.page.is_visible(self.TOTAL_PRICE_ELEMENT):
        #     total_price_text = self.page.get_text(self.TOTAL_PRICE_ELEMENT)
        #     total_price_match = re.search(r"\$([0-9,]+)", total_price_text)
        #     total_price = total_price_match.group(1).replace(",", "") if total_price_match else "N/A"
        #
        # # Collect all reservation details
        details = {
            # "title": title,
            "price_per_night": price_per_night,
        #     "total_price": total_price
        }
        #
        # self.logger.info(f"Reservation details: {details}")
        # return details
        return details

    def click_reserve_button(self):
        """Click the reserve button"""
        self.logger.info("Clicking reserve button")
        self.page.click(self.RESERVE_BUTTON)
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

    def validate_reservation_details(self, original_details: Dict):
        """Validate that reservation details match the original details

        Args:
            original_details: Dictionary containing original reservation details
        """
        self.logger.info("Validating reservation details")

        # Get current reservation details
        current_details = self.get_reservation_details()

        # Validate title
        assert current_details["title"] == original_details["title"], \
            f"Title mismatch: {current_details['title']} != {original_details['title']}"

        # Validate price per night
        assert current_details["price_per_night"] == original_details["price_per_night"], \
            f"Price mismatch: {current_details['price_per_night']} != {original_details['price_per_night']}"

        self.logger.info("Reservation details validated successfully")
        return self