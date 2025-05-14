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
    home.handle_popup_if_exists()

    # 2. Search for apartments
    location = "Tel Aviv-Yafo"
    checkin = "2025-08-01"
    checkout = "2025-08-05"
    adults = 2

    home.search(location=location, checkin=checkin, checkout=checkout, adults=adults)
    home.wait_page_load()

    # 3. Validate parameters of results
    current_url = home.get_url()
    # replaced characters to match the url syntax
    assert f"airbnb.com/s/{location}".replace('-', "~").replace(" ", "-") in current_url
    assert "checkin=2025-08-01" in current_url
    assert "checkout=2025-08-05" in current_url
    assert "adults=2" in current_url

    # 4. Analyze results
    results = SearchResultsPage(page)
    listings = results.extract_details()
    highest_rating = results.get_highest_rated(listings)
    cheapest_price = results.get_cheapest(listings)

    # Log results to console
    logger.info(f"This is the highest rated listing: {highest_rating}")

    logger.info(f"This is the cheapest listing: {cheapest_price}")
