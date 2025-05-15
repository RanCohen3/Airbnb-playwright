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
    PRODUCT_DETAILS = 'div[data-section-id="PRODUCT_DETAILS"]'

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

    def extract_trip_details_from_reservation(self):
        """
        This methis extracts the trip details from the reservation page right before the user reserves.
        :return:
        """
        trip_info = {}
        trip_details = self.page.query_selector(self.PRODUCT_DETAILS).text_content()
        adults, children = self.extract_number_of_guests(trip_details)
        start_date, end_date = self.extract_trip_dates(trip_details)

        trip_info["checkin"] = start_date
        trip_info["checkout"] = end_date
        trip_info["adults"] = adults
        trip_info["children"] = children

        return trip_info

    def extract_number_of_guests(self, trip_details):
        """
        This method extract the number of adults and children reserved.
        :param trip_details: Details from the reservation.
        """
        adults, children = 0, 0
        adults_match = re.search(r'(\d+)\s*adults?', trip_details, re.IGNORECASE)
        if adults_match:
            adults = int(adults_match.group(1)) % 10
        children_match = re.search(r'(\d+)\s*child?', trip_details, re.IGNORECASE)
        if children_match:
            children = int(children_match.group(1))

        return adults, children

    def extract_trip_dates(self, trip_details):
        match = re.search(r'([A-Za-z]+)\s+(\d+)\s*–\s*(\d+),\s*(\d{4})', trip_details)
        if not match:
            print("hi")

        month_string, start_day, end_day, year = match.groups()
        month_str = month_string.replace('details', "")
        start_date = datetime.strptime(f"{month_str} {start_day} {year}", "%b %d %Y").date()
        end_date = datetime.strptime(f"{month_str} {end_day} {year}", "%b %d %Y").date()

        return start_date.isoformat(), end_date.isoformat()
