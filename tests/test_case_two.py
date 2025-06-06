import logging
import pytest
from pages.home_page import AirBnbHomePage
from pages.listing_details_page import ListingDetailsPage
from pages.search_results_page import SearchResultsPage
from test_config import case_two_conf
from utils.helpers import get_highest_rated

logger = logging.getLogger("airbnb_tests")

@pytest.mark.playwright
def test_case_two(page):
    location = case_two_conf["location"]
    checkin = case_two_conf["checkin"]
    checkout = case_two_conf["checkout"]
    adults_count = case_two_conf["adults_count"]
    children_count = case_two_conf["children_count"]
    phone_number = case_two_conf["phone_number"]
    logger.info("starting test case two")

    # 1. Navigate to airbnb homepage
    home = AirBnbHomePage(page)
    home.open_page()
    home.wait_page_load()

    # switching to english in case of hebrew
    home.handle_popup_if_exists()
    home.switch_he_to_en()
    home.wait_page_load()
    home.handle_popup_if_exists()

    # 2. Search for apartments
    home.search(location=location, checkin=checkin, checkout=checkout, adults=adults_count,
                children=children_count)
    home.wait_page_load()

    # 3. Validate parameters of results
    current_url = home.get_url()
    # replaced characters to match the url syntax
    assert f"airbnb.com/s/{location}".replace('-', "~").replace(" ", "-") in current_url
    assert f"checkin={checkin}" in current_url
    assert f"checkout={checkout}" in current_url
    assert f"adults={adults_count}" in current_url
    assert f"adults={adults_count}" in current_url
    logger.info("Arguments assertions done")

    # 4. Analyze results
    results = SearchResultsPage(home.page)
    listings = results.extract_details()
    highest_rating = get_highest_rated(listings)
    logger.info("Navigating to the highest rated listing")
    with results.page.expect_popup() as popup_info:
        highest_rating['listing'].click()
        raw_details_page = popup_info.value

    listing_details = ListingDetailsPage(raw_details_page)
    listing_details.wait_page_load()
    listing_details.handle_popup_if_exists()
    listing_details.switch_he_to_en()
    listing_details.wait_page_load()
    listing_details.handle_popup_if_exists()

    listing_details.wait_page_load()
    details = listing_details.get_reservation_details()

    logger.info(f"price per night {details['price_per_night']}")
    logger.info(f"check in on {details['check-in']}")
    logger.info(f"check out on {details['check-out']}")

    listing_details.click_reserve_button()
    listing_details.wait_page_load()

    trip_details = listing_details.extract_trip_details_from_reservation()

    assert trip_details["checkin"] == checkin
    assert trip_details["checkout"] == checkout
    assert trip_details["adults"] == adults_count
    assert trip_details["children"] == children_count

    listing_details.request_to_book_next()
    listing_details.wait_page_load()

    listing_details.enter_phone_number(phone_number=phone_number)

    logger.info("Finished TEST CASE TWO")
