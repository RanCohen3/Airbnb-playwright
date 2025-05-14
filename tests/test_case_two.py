import logging
import pytest
from pages.home_page import AirBnbHomePage
from pages.listing_details_page import ListingDetailsPage
from pages.search_results_page import SearchResultsPage
from test_config import location, checkin, checkout, adults_count


logger = logging.getLogger("airbnb_tests")

@pytest.mark.playwright
def test_case_two(page):
    logger.info("starting test case one")

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
    home.search(location=location, checkin=checkin, checkout=checkout, adults=adults_count)
    home.wait_page_load()

    # 3. Validate parameters of results
    current_url = home.get_url()
    # replaced characters to match the url syntax
    assert f"airbnb.com/s/{location}".replace('-', "~").replace(" ", "-") in current_url
    assert f"checkin={checkin}" in current_url
    assert f"checkout={checkout}" in current_url
    assert f"adults={adults_count}" in current_url
    logger.info("Arguments assertions done")

    # 4. Analyze results
    results = SearchResultsPage(home.page)
    listings = results.extract_details()
    highest_rating = results.get_highest_rated(listings)
    logger.info("Navigating to the highest rated listing")
    # highest_rating['listing'].click()
    with results.page.expect_popup() as popup_info:
        highest_rating['listing'].click()
        raw_details_page = popup_info.value

    listing_details = ListingDetailsPage(raw_details_page)
    listing_details.wait_page_load()
    listing_details.handle_popup_if_exists()
    listing_details.switch_he_to_en()
    listing_details.wait_page_load()
    listing_details.handle_popup_if_exists()


