import pytest
import logging
from pages.home_page import AirBnbHomePage
from pages.search_results_page import SearchResultsPage

logger = logging.getLogger("airbnb_tests")

@pytest.mark.playwright
def test_case_one(page, check_airbnb_us):
    home = AirBnbHomePage(page)
    # home.goto()
    home.accept_cookies()
    home.search("Tel Aviv-Yafo", "2025-08-1", "2025-08-05", adults=2)

    results = SearchResultsPage(page)
    results.validate_parameters(adults=2, children=0)

    listings = results.extract_details()
    highest_rating = results.get_highest_rated(listings)
    cheapest_price = results.get_cheapest(listings)

    logger.info(f"These are the highest rated listings: {highest_rating}")

    logger.info(f"This is the cheapest listing: {cheapest_price}")
