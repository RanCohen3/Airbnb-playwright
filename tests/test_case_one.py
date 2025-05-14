import pytest
import logging
from pages.home_page import AirBnbHomePage
from pages.search_results_page import SearchResultsPage

logger = logging.getLogger("airbnb_tests")


@pytest.mark.playwright
def test_case_one(page):
    logger.info("starting test case one")

    # 1. Navigate to airbnb homepage
    home = AirBnbHomePage(page)
    home.open_page()
    home.wait_page_load()

    # switching to english in case of hebrew
    home.handle_popup_if_exists()
    home.switch_he_to_en()
    home.wait_page_load()

    # 2. Search for apartments
    home.handle_popup_if_exists()
    # TODO the
    home.search(location="Tel Aviv-Yafo", checkin="2025-08-01", checkout="2025-08-05", adults=2)

    # 3. Validate parameters of results
    results = SearchResultsPage(page)
    # TODO should this be asserted like that?
    assert results.validate_guests(adults=2, children=0)
    assert results.validate_dates(checkin="2025-08-01", checkout="2025-08-05")

    # 4. Analyze results
    listings = results.extract_details()
    highest_rating = results.get_highest_rated(listings)
    cheapest_price = results.get_cheapest(listings)

    # Log results to console
    logger.info(f"This is the highest rated listing: {highest_rating}")

    logger.info(f"This is the cheapest listing: {cheapest_price}")
